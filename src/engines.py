import subprocess
import time
from util import *
from enum import Enum, IntEnum
from queue import Queue, Empty
from threading import Thread
from xml.etree import cElementTree as ElementTree
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):

    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


class Protocol(IntEnum):
    UCI = 1
    WINBOARD = 2


class Engine:

    def __init__(self, **kwargs):
        # if 'args' is contained in kwargs, read the args dictionary instead of kwargs
        if 'args' in kwargs:
            kwargs = kwargs['args']

        # set the settings
        self.settings = kwargs
        # set the name and author information
        self.information = {'name': '', 'author': ''}
        # remember nothing is running
        self.is_running = False
        self.is_searching = False
        # store a potential listener which receives the lines the engine sends
        self.listener = None

        # make sure that 'bin' is contained and is not None
        if 'bin' not in self.settings or self.settings['bin'] is None:
            self.settings['bin'] = ''
        # make sure the protocol is set default to UCI
        if 'proto' not in self.settings or self.settings['proto'] is None:
            self.settings['proto'] = Protocol.UCI
        # make sure the options are contained
        if 'options' not in self.settings or self.settings['options'] is None:
            self.settings['options'] = {}

    def create_dict(self):
        # make sure we store the mapped integer of the protocol
        if 'proto' in self.settings:
            self.settings['proto'] = int(self.settings['proto'])
        return self.settings

    def start(self):
        # make sure we are not in an invalid state
        self._update_state()

        # do not start if an instance is already running
        if self.is_running:
            # did not start successfully
            return False

        # remember the engine is running and no search has started
        self.is_running = True
        self.is_searching = False

        # try to start the process
        try:
            self.process = subprocess.Popen([self.settings['bin']], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                            bufsize=1, encoding="utf8")

            # have a queue to write previous entries
            self.queue = Queue(maxsize=1024)

            # have a thread which awaits lines from the engine
            self.thread = Thread(target=self._enqueue_output, args=(self.process.stdout, self.queue))

            # thread dies with the program
            self.thread.daemon = True

            # start the thread
            self.thread.start()
        except:
            # some error happened, set the process to None
            self.process = None

            # remember no process is running
            self.is_running = False

            # update the status bar if one exists
            updateStatusBar(f"Error starting process{self.settings['bin']}")

            # did not start successfully
            return False

        # retrieve options which can be set
        self._retrieve_information()

        # started successfully
        return True

    def send_line(self, line):
        # make sure the state is valid
        self._update_state()

        # do not send anything if the engine is not running
        if not self.is_running:

            # line sending was not successfully
            return False

        # write the line to the stdin
        self.process.stdin.write(line + "\n")

        # flush the output
        self.process.stdin.flush()

        # line sending was successfully
        return True

    def send_options(self):
        # sends the options to the engine
        if int(self.settings['proto']) == Protocol.UCI:
            for option in self.settings['options']:
                self.send_line(f'setoption name {option} value {self.settings["options"][option]["value"]}')
        elif int(self.settings['proto']) == Protocol.WINBOARD:
            pass

    def exit(self):
        # update the state to make sure the engine did not crash
        self._update_state()

        # do not exit if we havent even started
        if not self.is_running:
            # stopping was not successful
            return False

        # make sure no search is running
        self.stop_search()

        # send the exit command
        if int(self.settings['proto']) == Protocol.UCI:
            self.send_line('exit')
        elif int(self.settings['proto']) == Protocol.WINBOARD:
            pass

        # terminate the actual process
        self.process.terminate()

        # remember no process is running
        self.is_running = False

        # successfully stopped
        return True

    def search(self, fen, moves=''):
        # update the state to make sure the engine did not crash
        self._update_state()

        # do not search if we are not running
        if not self.is_running:
            return False

        # if we already search, stop the previous search
        if self.is_searching:
            self.stop_search()

        # sending the position to the engine
        if int(self.settings['proto']) == Protocol.UCI:
            if moves:
                self.send_line(f"position fen {fen} moves {moves}")
            else:
                self.send_line(f"position fen {fen}")
        elif int(self.settings['proto']) == Protocol.WINBOARD:
            pass

        # marking the flag for searching
        self.is_searching = True

        # starting the search
        if int(self.settings['proto']) == Protocol.UCI:
            self.send_line(f"go infinite")
        elif int(self.settings['proto']) == Protocol.WINBOARD:
            pass

    def stop_search(self):
        # make sure the state is valid
        self._update_state()

        # do not stop the search if no search has started or the engine is not even running
        if not self.is_searching or not self.is_running:
            return False

        # remember we stopped searching
        self.is_searching = False

        # send the stop command
        if int(self.settings['proto']) == Protocol.UCI:
            self.send_line("stop")
        elif int(self.settings['proto']) == Protocol.WINBOARD:
            pass

        # need to sleep before sending a few commands
        time.sleep(0.05)

    def _enqueue_output(self, out, queue):
        # thread awaits outputs from the engine
        for line in iter(out.readline, b''):
            # do not process empty lines
            if line:
                # add it to the queue
                queue.put(line)
                # if someone is listening, notify him
                if self.listener is not None:
                    self.listener(line)
        # close the output
        out.close()

    def listen(self, func):
        # add a listener
        self.listener = func

    def _update_state(self):
        # if we are running but the process died, make sure we stopped
        if self.is_running:
            if self.process.poll() is not None:
                self.is_running = False
                self.is_searching = False

    def _retrieve_information(self):
        # make sure we are in a valid state
        self._update_state()

        # do not retrieve information if we are not running
        if not self.is_running:
            return

        # send the command to poll for options
        self.send_line("uci" if int(self.settings['proto']) == Protocol.UCI else 'uci')

        # since the options may change if the exe changes, we need to overwrite previous entries but keep existing
        # values
        new_options = {}

        # measure the time it takes. If the engine does not properly handle the protocols, we will notify the user
        start_time = time.perf_counter()

        while True:

            # check if retrieving information took longer than a full second -> crash or invalid
            if time.perf_counter() - start_time > 1:
                updateStatusBar("Error retrieving options. Using this engine can lead to potential crashes "
                                "since it does not implement the Protocol correctly")
                return
            # poll from the queue to read the buffer
            try:
                line = self.queue.get_nowait()
            except Empty:
                # if nothing new has been received, sleep for a bit
                time.sleep(0.01)

                # continue to the next iteration
                continue

            # strip white spaces and line breaks
            line = line.strip()

            # check if all options have been read
            if 'uciok' in line and int(self.settings['proto']) == Protocol.UCI or \
               'uciok' in line and int(self.settings['proto']) == Protocol.WINBOARD:
                break

            # read the engine name
            if 'id name' in line and int(self.settings['proto']) == Protocol.UCI or \
               'id name' in line and int(self.settings['proto']) == Protocol.WINBOARD:
                self.information['name'] = line[7:].strip()

            # read the author name
            if 'id author' in line and int(self.settings['proto']) == Protocol.UCI or \
               'id author' in line and int(self.settings['proto']) == Protocol.WINBOARD:
                self.information['author'] = line[9:].strip()

            # read options (only supported for uci so far
            if 'option' in line and int(self.settings['proto']) == Protocol.UCI:
                option = {}
                split = line.split(' ')
                if not 'name' in line:
                    continue
                name = split[split.index('name') + 1]
                if 'type' in line:
                    option['type'] = split[split.index('type') + 1]
                    if 'min' in line:
                        option['min'] = int(split[split.index('min') + 1])
                    if 'max' in line:
                        option['max'] = int(split[split.index('max') + 1])
                    if option['type'] == 'string':
                        if 'default' in line:
                            try:
                                option['default'] = str(split[split.index('default') + 1])
                            except:
                                option['default'] = ''
                    else:
                        if 'default' in line:
                            try:
                                option['default'] = int(split[split.index('default') + 1])
                            except:
                                option['default'] = ''
                    if option['type'] == 'combo':
                        vals = []
                        for i in range(split.index('var') + 1, len(split)):
                            if split[i] in ['min', 'max', 'default']:
                                break
                            vals += [split[i]]
                        option['vals'] = vals

                # make sure to still use the correct value
                if name in self.settings['options']:
                    if 'value' in self.settings['options'][name]:
                        option['value'] = self.settings['options'][name]['value']
                    else:
                        try:
                            option['value'] = option['default']
                        except:
                            pass 
                else:
                    try:
                        option['value'] = option['default']
                    except:
                        pass 

                # place in new options list
                new_options[name] = option

        # use new options list
        self.settings['options'] = new_options


class Engines:

    def __init__(self):
        self.engines = {}

    def read_xml(self, file):
        # reads some xml to parse the engines
        self.engines = {}

        # create the xml tree
        tree = ElementTree.parse(file)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)

        # creates the engine with the given xml information
        for key in xmldict:
            self.engines[key] = Engine(args=xmldict[key])

    def write_xml(self, file):
        # writes the engines to a xml file
        out_dict = {}

        # write a dictionary for each engine
        for i in self.engines:
            out_dict[i] = self.engines[i].create_dict()

        # write the xml
        xml = dicttoxml(out_dict, attr_type=False)
        dom = parseString(xml)

        # make it pretty
        f = open(file, "w")
        f.write(dom.toprettyxml())
        f.close()


if __name__ == '__main__':
    # e = Engine(proto=Protocol.UCI)
    # dict = e.create_dict()
    # xml = dicttoxml(array, custom_root='test', attr_type=False)

    eng = Engines()
    eng.read_xml("engines.xml")
    print(eng.engines['Koivisto'].settings['options'])
