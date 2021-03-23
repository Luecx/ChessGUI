import sys
import os
import res
import time
import math
import psutil

from engines import Engines, Protocol, Engine
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar, QHBoxLayout, QSlider, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic


class SpinOptionWidget(QWidget):
    def __init__(self, name, listener, init, min=0, max=100, default=50, logarithmic=False, log_base=2):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()
        self.listener = listener
        self.name     = name

        self.default = default
        self.min = min
        self.max = max
        self.logarithmic = logarithmic
        self.log_base = log_base
        self.log_factor = 100.0 / math.log(max - min + 1, log_base)

        self.name_label = QLabel(name,self)
        self.name_label.setMaximumWidth(100)
        self.name_label.setMinimumWidth(100)

        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setRange(min if not self.logarithmic else 0,max if not self.logarithmic else 100)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setPageStep(5)
        self.slider.valueChanged.connect(self._change_value if not self.logarithmic else lambda x:self._change_value(self._value_from_range(x)))

        self.label = QLineEdit('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMaximumWidth(80)
        self.label.editingFinished.connect(lambda:self._change_value(str(self.label.text())))

        hbox.addWidget(self.name_label)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.label)
        hbox.addSpacing(15)

        self.setLayout(hbox)
        self._change_value(init)

    def reset(self):
        self._change_value(self.default)

    def _value_from_range(self, range):
        if not self.logarithmic:
            return range
        return round(math.pow(self.log_base, range / self.log_factor)+self.min-1)

    def _range_from_value(self, value):
        if not self.logarithmic:
            return value
        return round(self.log_factor * math.log(value - self.min + 1, self.log_base))

    def _change_value(self, value):
        if value == '':
            value = self.default
        try:
            value = int(value)
        except:
            value = self.default
        value = min(self.max, value)
        value = max(self.min, value)

        self.slider.setValue(self._range_from_value(int(value)))
        self.label.setText(str(value))
        self.listener(self.name, int(value))

class StringOptionWidget(QWidget):
    def __init__(self, name, listener, init, default=''):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()
        self.listener = listener
        self.name     = name
        self.default  = default

        self.name_label = QLabel(name,self)
        self.name_label.setMaximumWidth(100)
        self.name_label.setMinimumWidth(100)

        entry = QLineEdit(self)
        entry.setText(default)
        entry.textChanged.connect(self._change_value)
        hbox.addWidget(self.name_label)
        hbox.addWidget(entry)

        self.setLayout(hbox)
        self._change_value(init)

    def reset(self):
        self._change_value(self.default)

    def _change_value(self, value):
        self.label.setText(str(value))
        self.listener(self.name, str(value))

class PathOptionWidget(QWidget):
    def __init__(self, name, listener,init, default=''):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()
        self.listener = listener
        self.name     = name
        self.default  = default

        self.name_label = QLabel(name,self)
        self.name_label.setMaximumWidth(100)
        self.name_label.setMinimumWidth(100)

        self.entry = QLineEdit(self)
        self.entry.setText(default)
        self.entry.textChanged.connect(self._change_value)
        self.btn = QPushButton('Browse', self)
        self.btn.setMinimumWidth(80)
        self.btn.clicked.connect(lambda x:self._open_file_dialog())

        hbox.addWidget(self.name_label)
        hbox.addWidget(self.entry)
        hbox.addSpacing(15)
        hbox.addWidget(self.btn)

        self.setLayout(hbox)
        self._change_value(init)

    def reset(self):
        self._change_value(self.default)

    def _open_file_dialog(self):
        dlg = QFileDialog(self)
        if 'Path' in self.name:
            dlg.setFileMode(QFileDialog.Directory)
        if 'File' in self.name:
            dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) == 1:
                self._change_value(filenames[0])

    def _change_value(self, value):
        self.entry.setText(str(value))
        self.listener(self.name, value)

class EngineConfigWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.engines = Engines()
        self.engines.read_xml("engines.xml")
        self._load_ui()

    def selected_engine(self):
        return self.engine_combo.currentText()

    def _load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "engineconfigwidget_form.ui")
        uic.loadUi(path, self)

        # load the engine names into the combo box
        for key in self.engines.engines:
            self.engine_combo.addItems([key])

        self.engine_combo.currentIndexChanged.connect(lambda x: self._edit_engine_name(x))
        self.engine_combo_index = 0 if len(self.engines.engines) > 0 else -1

        # bind a change on the protocol
        self.     protouci_radio.clicked.connect(lambda x: self._update_proto(Protocol.UCI))
        self.protowinboard_radio.clicked.connect(lambda x: self._update_proto(Protocol.WINBOARD))

        # bind a change on the exe name
        self.exe_edit.textChanged.connect(lambda x:self._update_exe(x))

        # bind a change on the exe browse button
        self.browseexe_button.clicked.connect(lambda x:self._open_exe_file_dialog())

        # load the initial widgets
        self._update_option_widgets()

        # bind a reload of the current options which detects changes
        self. loadoption_button.clicked.connect(lambda x:self._detect_engine_options())
        self.resetoption_button.clicked.connect(lambda x:self._reset_options())

        # bin the buttons for creating and deleting new engines
        self.newengine_button.clicked.connect(lambda x: self._add_engine())
        self.delengine_button.clicked.connect(lambda x: self._del_engine())

    def update_option(self, key, value):
        if self.selected_engine() in self.engines.engines:
            self.engines.engines[self.selected_engine()].settings['options'][key]['value'] = value
        self.engines.write_xml('engines.xml')

    def _update_proto(self, proto):

        if proto == Protocol.UCI:
            self.protouci_radio.setChecked(True)
        elif proto == Protocol.WINBOARD:
            self.protowinboard_radio.setChecked(True)

        if self.selected_engine() in self.engines.engines:
            self.engines.engines[self.selected_engine()].settings['proto'] = proto
        self.engines.write_xml('engines.xml')

    def _edit_engine_name(self, new_index):

        # detect if we try to manually adjust the name
        # if so, we need to reset the current index, overwrite the name and remove the new element
        # make sure to not do this when we created the first element this way
        if new_index >= len(self.engines.engines) and new_index >= 1:
            new_text = self.engine_combo.currentText()
            old_text = self.engine_combo.itemText(self.engine_combo_index)
            self.engine_combo.setItemText(self.engine_combo_index, new_text)
            self.engine_combo.setCurrentIndex(self.engine_combo_index)
            self.engine_combo.removeItem(new_index)

            # also adjusting the name in the config
            self.engines.engines[new_text] = self.engines.engines[old_text]
            del self.engines.engines[old_text]

        elif new_index >= len(self.engines.engines) and new_index == 0:
            new_text = self.engine_combo.currentText()
            self.engines.engines[new_text] = Engine()
            self.engine_combo_index = self.engine_combo.currentIndex()
        else:
            self.engine_combo_index = self.engine_combo.currentIndex()


        # print(self.engines.engines[self.selected_engine()].settings)
        self._update_option_widgets()

    def _add_engine(self, name=None):

        new_name = f"NewEngine{len(self.engines.engines)}" if name is None else name

        self.engines.engines[new_name] = Engine()
        self.engine_combo.addItem(new_name)
        self.engine_combo.setCurrentIndex(self.engine_combo.count()-1)
        self.engine_combo_index = self.engine_combo.count()-1

    def _del_engine(self):

        if self.engine_combo.count() == 0:
            return

        del self.engines.engines[self.engine_combo.currentText()]
        self.engine_combo.removeItem(self.engine_combo.currentIndex())
        self.engine_combo_index = self.engine_combo.count()-1

    def _update_exe(self, exe):
        if self.exe_edit.text() != exe:
            self.exe_edit.setText(exe)

        if self.selected_engine() in self.engines.engines:
            self.engines.engines[self.selected_engine()].settings['bin'] = exe
        self.engines.write_xml('engines.xml')

    def _open_exe_file_dialog(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Executables (*.exe)"])
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) == 1:
                self._update_exe(filenames[0])

    def _detect_engine_options(self):
        if self.selected_engine() in self.engines.engines:
            engine = self.engines.engines[self.selected_engine()]

            if not engine.start():
                return
            else:
                engine.exit()
            self._update_option_widgets()

    def _reset_options(self):
        for i in range(self.verticalLayout_7.count()):
            self.verticalLayout_7.itemAt(i).widget().reset()

    def _update_option_widgets(self):

        # set the text inside the exe text field and the protocol
        if self.selected_engine() in self.engines.engines:
            engine = self.engines.engines[self.selected_engine()]
            self._update_exe(engine.settings['bin'])
            self._update_proto(engine.settings['proto'])

        # make sure to delete previous widgets
        for i in reversed(range(self.verticalLayout_7.count())):
            self.verticalLayout_7.itemAt(i).widget().setParent(None)

        # dont do anything if no engine is selected
        if self.selected_engine() not in self.engines.engines:
            return

        # add all the option widgets
        for option in self.engines.engines[self.selected_engine()].settings['options']:
            info = self.engines.engines[self.selected_engine()].settings['options'][option]
            # adding spin widgets
            # detects if its hash, threads or something else
            # will check for cpu counts / max memory
            if info['type'] == 'spin':
                if 'Hash' in option:

                    widg = SpinOptionWidget(option,
                                            listener=self.update_option,
                                            init=int(info['value'] if 'value' in info else int(info['default'])),
                                            min=int(info['min']),
                                            max=min(int(info['max']),psutil.virtual_memory().total // 1024 // 1024),
                                            default=int(info['default']),
                                            logarithmic=True)
                elif 'Threads' in option:
                    widg = SpinOptionWidget(option,
                                            listener=self.update_option,
                                            init=int(info['value'] if 'value' in info else int(info['default'])),
                                            min=int(info['min']),
                                            max=min(int(info['max']), psutil.cpu_count()),
                                            default=int(info['default']),
                                            logarithmic=False)
                else:
                    pass
                    widg = SpinOptionWidget(option,
                                            listener=self.update_option,
                                            init=int(info['value'] if 'value' in info else int(info['default'])),
                                            min=int(info['min']),
                                            max=int(info['max']),
                                            default=int(info['default']),
                                            logarithmic=False)
                self.verticalLayout_7.addWidget(widg)

            # checks for a string entry
            # will check for a path. If a path is required, a dialog button will be added
            if info['type'] == 'string':

                # it can happen that the xml outputs None instead of an empty string
                if info['default'] is None:
                    info['default'] = ''
                if info['value'] is None:
                    info['value'] = ''
                if 'Path' in option:
                    self.verticalLayout_7.addWidget(PathOptionWidget(
                        name=option,
                        listener=self.update_option,
                        init=str(info['value'] if 'value' in info else str(info['default']))))
                else:
                    self.verticalLayout_7.addWidget(StringOptionWidget(
                        name=option,
                        listener=self.update_option,
                        init=str(info['value'] if 'value' in info else str(info['default']))))

