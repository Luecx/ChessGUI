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
        if 'args' in kwargs:
            kwargs = kwargs['args']

        self.settings = kwargs
        self.information = {'name': '', 'author': ''}
        self.search_result = []
        self.is_running = False
        self.is_searching = False
        self.listener = None

        if 'bin' not in self.settings or self.settings['bin'] is None:
            self.settings['bin'] = ''
        if 'proto' not in self.settings or self.settings['proto'] is None:
            self.settings['proto'] = Protocol.UCI
        if 'options' not in self.settings or self.settings['options'] is None:
            self.settings['options'] = {}

    def create_dict(self):
        return self.settings

    def start(self):
        self._update_state()
        if self.is_running:
            return False
        self.is_running = True
        self.is_searching = False
        try:
            self.process = subprocess.Popen([self.settings['bin']], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                            bufsize=1, encoding="utf8")
            self.queue = Queue(maxsize=1024)
            self.thread = Thread(target=self._enqueue_output, args=(self.process.stdout, self.queue))
            self.thread.daemon = True  # thread dies with the program
            self.thread.start()
        except:
            self.process = None
            self.is_running = False
            updateStatusBar(f"Error starting process{self.settings['bin']}")
            return False
        self._retrieve_information()
        return True

    def send_line(self, line):
        self._update_state()
        if not self.is_running:
            return False
        self.process.stdin.write(line + "\n")
        self.process.stdin.flush()
        return True

    def exit(self):
        self._update_state()
        if not self.is_running:
            return False

        self.stop_search()
        self.send_line('exit')
        self.process.terminate()
        self.is_running = False
        return True

    def search(self, fen, moves=''):
        self._update_state()
        if not self.is_running:
            return False

        if self.is_searching:
            self.stop_search()

        if moves:
            self.send_line(f"position fen {fen} moves {moves}")
        else:
            self.send_line(f"position fen {fen}")

        self.send_line(f"go infinite")

    def search_poll(self):
        self._update_state()
        if not self.is_searching:
            return False

        while True:
            try:
                line = self.queue.get_nowait()
            except Empty:
                break
            print(line)

        # line = self.read_line()
        # while 'bestmove' not in line:
        #     print(line)
        #     line = self.read_line()

    def stop_search(self):
        self._update_state()
        if not self.is_searching:
            return False

        self.is_searching = False
        self.send_line("stop")

    def _enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            if line:
                queue.put(line)
                if self.listener is not None:
                    self.listener(line)
        out.close()

    def listen(self, func):
        self.listener = func

    def _update_state(self):
        if self.is_running:
            if self.process.poll() is not None:
                self.is_running = False
                self.is_searching = False

    def _retrieve_information(self):
        self._update_state()
        if not self.is_running:
            return

        self.send_line("uci" if self.settings['proto'] is Protocol.UCI else 'uci')

        new_options = {}

        start_time = time.perf_counter()

        while True:

            # check if retrieving information took longer than a full second -> crash or invalid
            if time.perf_counter() - start_time > 1:
                updateStatusBar("Error retrieving options. Using this engine can lead to potential crashes since it does not implement the Protocol correctly")
                break

            try:
                line = self.queue.get_nowait()
            except Empty:
                time.sleep(0.01)
                continue
            line = line.strip()
            if 'uciok' in line:
                break
            if 'id name' in line:
                self.information['name'] = line[7:].strip()
            if 'id author' in line:
                self.information['author'] = line[9:].strip()
            if 'option' in line:
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
        self.engines = {}

        tree = ElementTree.parse(file)
        root = tree.getroot()
        xmldict = XmlDictConfig(root)

        for key in xmldict:
            self.engines[key] = Engine(args=xmldict[key])

    def write_xml(self, file):
        out_dict = {}
        for i in self.engines:
            out_dict[i] = self.engines[i].create_dict()
        xml = dicttoxml(out_dict, attr_type=False)
        dom = parseString(xml)
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
