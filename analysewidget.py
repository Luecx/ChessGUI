import sys
import os
import res
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic
from boardwidget import *
from engines import *
from util import getMainWindow


class AnalyseWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self._load_ui()

    def _load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "analysewidget_form.ui")
        uic.loadUi(path, self)

        self.board_widget = BoardWidget()

        self.gridLayout.addWidget(self.board_widget, 0, 0)
        self.boardroot_frame.setMinimumWidth(self.boardroot_frame.height())
        self.boardroot_frame.setMaximumWidth(self.boardroot_frame.height())
        self.boardpage_button.clicked.connect(lambda x: self.tab_stack.setCurrentIndex(0))
        self.enginepage_button.clicked.connect(lambda x: self.tab_stack.setCurrentIndex(1))
        self.otherpage_button.clicked.connect(lambda x: self.tab_stack.setCurrentIndex(2))

        self.tab_stack.setCurrentIndex(0)
        self.boardpage_button.setChecked(True)

        self.analysetoggle_button.clicked.connect(lambda x: self.start_analysis() if x else self.stop_analysis())

    def _current_engine(self):
        engines = getMainWindow().getEngineConfigWidget().engines.engines
        if self.engine_combo.currentText() in engines:
            return engines[self.engine_combo.currentText()]
        else:
            return None

    def _process_engine_line(self, line):

        func = lambda label,split,value: label.setText(split[split.index(value)+1] if value in split else '')

        split = line.split()
        print(split)
        func(self.   nodes_label, split, 'nodes')
        func(self.     nps_label, split, 'nps')
        func(self.   depth_label, split, 'depth')
        func(self.seldepth_label, split, 'seldepth')
        func(self.    time_label, split, 'time')
        func(self.  tbhits_label, split, 'tbhits')

        if 'mate' in split:
            self._update_score(mate=split[split.index('mate')+1])
        elif 'score' in split:
            self._update_score(mate=split[split.index('score')+2])

    def _retrieve_search_fen_and_moves(self):
        return self.board_widget.board.fen(), None

    def _update_search(self):
        if self._current_engine() is not None:
            fen,moves=self._retrieve_search_fen_and_moves()
            self._current_engine().search(fen,moves)

    def _update_score(self, score=None, mate=None):
        pass

    def stop_analysis(self):
        self.analysetoggle_button.setChecked(False)
        self.engine_combo.setEnabled(True)
        if self._current_engine() is None:
            return
        self._current_engine().exit()
        pass

    def start_analysis(self):
        if self._current_engine() is None:
            return
        # listen to the output and wait 0.1 seconds
        self._current_engine().listen(self._process_engine_line)
        time.sleep(0.1)
        # try to start the engine
        if self._current_engine().start():
            self.analysetoggle_button.setChecked(True)
            self.engine_combo.setEnabled(False)
            time.sleep(0.1)
            self._update_search()

    def reload_engines(self):
        while self.engine_combo.count() > 0:
            self.engine_combo.removeItem(0)

        engines = getMainWindow().getEngineConfigWidget().engines.engines
        for key in engines:
            if engines[key].settings['bin'] != '':
                self.engine_combo.addItem(key)

        self.analysetoggle_button.setEnabled(self.engine_combo.count() > 0)

        self.pv1_button.setText("")
        self.pv2_button.setText("")
        self.pv3_button.setText("")
        self.pv4_button.setText("")
        self.pv5_button.setText("")



    def resizeEvent(self, e):
        self.boardroot_frame.setMinimumWidth(self.boardroot_frame.height())
        self.boardroot_frame.setMaximumWidth(self.boardroot_frame.height())
