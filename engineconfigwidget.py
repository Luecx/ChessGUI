import sys
import os
import res
import time
import math

from engines import Engines, Protocol
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar, QHBoxLayout, QSlider, QLabel, QLineEdit, \
    QPushButton, QFileDialog
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic


class SpinOptionWidget(QWidget):
    def __init__(self, min=0, max=100, default=50, logarithmic=False, log_base=2):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()

        self.default = default
        self.min = min
        self.max = max
        self.logarithmic = logarithmic
        self.log_base = log_base
        self.log_factor = 100.0 / math.log(max - min + 1, log_base)

        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setRange(min if not self.logarithmic else 0,max if not self.logarithmic else 100)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setPageStep(5)
        self.slider.valueChanged.connect(self.change_value if not self.logarithmic else lambda x:self.change_value(self.value_from_range(x)))

        self.label = QLineEdit('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMaximumWidth(80)
        self.label.editingFinished.connect(lambda:self.change_value(str(self.label.text())))

        hbox.addWidget(self.slider)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

    def value_from_range(self, range):
        if not self.logarithmic:
            return range
        return round(math.pow(self.log_base, range / self.log_factor)+self.min-1)

    def range_from_value(self, value):
        if not self.logarithmic:
            return value
        return round(self.log_factor * math.log(value - self.min + 1, self.log_base))

    def change_value(self, value):
        if value == '':
            value = self.default
        try:
            value = int(value)
        except:
            value = self.default
        value = min(self.max, value)
        value = max(self.min, value)

        self.slider.setValue(self.range_from_value(int(value)))
        self.label.setText(str(value))

class StringOptionWidget(QWidget):
    def __init__(self, default=''):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()

        entry = QLineEdit(self)
        entry.setText(default)
        entry.textChanged.connect(self.change_value)
        hbox.addWidget(entry)

        self.setLayout(hbox)

    def change_value(self, value):
        pass
        #self.label.setText(str(value))

class PathOptionWidget(QWidget):
    def __init__(self, default=''):
        super(QWidget, self).__init__()
        hbox = QHBoxLayout()

        entry = QLineEdit(self)
        entry.setText(default)
        entry.textChanged.connect(self.change_value)
        self.btn = QPushButton('Browse', self)
        self.btn.setMinimumWidth(80)

        hbox.addWidget(entry)
        hbox.addSpacing(15)
        hbox.addWidget(self.btn)

        self.setLayout(hbox)

    def change_value(self, value):
        pass
        #self.label.setText(str(value))

class EngineConfigWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.engines = Engines()
        self.engines.read_xml("engines.xml")
        self.load_ui()

    def selected_engine(self):
        return self.engine_combo.currentText()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "engineconfigwidget_form.ui")
        uic.loadUi(path, self)
        for i in range(20):
            self.verticalLayout_7.addWidget(SpinOptionWidget(logarithmic=True))

        # load the engine names into the combo box
        for key in self.engines.engines:
            self.engine_combo.addItems([key])

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
        self.loadoption_button.clicked.connect(lambda x:self._detect_engine_options())

    def _update_proto(self, proto):
        if self.selected_engine() in self.engines.engines:
            self.engines.engines[self.selected_engine()].settings['proto'] = proto

    def _update_exe(self, exe):
        if self.exe_edit.text() != exe:
            self.exe_edit.setText(exe)

        if self.selected_engine() in self.engines.engines:
            self.engines.engines[self.selected_engine()].settings['bin'] = exe

    def _open_exe_file_dialog(self):
        pass
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
            print(engine.settings['bin'])

            if not engine.start():
                return
            else:
                engine.exit()
            self._update_option_widgets()



    def _update_option_widgets(self):

        # make sure to delete previous widgets
        for i in reversed(range(self.verticalLayout_7.count())):
            self.verticalLayout_7.itemAt(i).widget().setParent(None)

        # dont do anything if no engine is selected
        if self.selected_engine() not in self.engines.engines:
            return

        for option in self.engines.engines[self.selected_engine()].settings['options']:
            info = self.engines.engines[self.selected_engine()].settings['options'][option]
            print(info)





