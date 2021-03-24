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
        self.board_widget.listen(lambda x:self._board_changed())

        self.gridLayout.addWidget(self.board_widget, 0, 0)
        self.boardroot_frame.setMinimumWidth(self.boardroot_frame.height())
        self.boardroot_frame.setMaximumWidth(self.boardroot_frame.height())
        self.boardpage_button.clicked.connect(lambda x: self._change_page(0))
        self.enginepage_button.clicked.connect(lambda x: self._change_page(1))
        self.otherpage_button.clicked.connect(lambda x: self._change_page(2))

        self.tab_stack.setCurrentIndex(0)
        self.boardpage_button.setChecked(True)

        self.analysetoggle_button.clicked.connect(lambda x: self.start_analysis() if x else self.stop_analysis())

        self.setpiece_buttons = [
            self.setnone_button,
            self.setpawn_button,
            self.setknight_button,
            self.setbishop_button,
            self.setrook_button,
            self.setqueen_button,
            self.setking_button]
        for i in range(7):
            self.setpiece_buttons[i].clicked.connect(lambda x,i=i:self._set_piece_button_pressed(i,x))

        self.fen_edit.editingFinished.connect(lambda:self._set_fen(self.fen_edit.text()))


        self.undomove_button.clicked.connect(lambda x:self.board_widget.undo_move())
        self. undoall_button.clicked.connect(lambda x:self.board_widget.undo_all())
        self.redomove_button.clicked.connect(lambda x:self.board_widget.redo_move())
        self. redoall_button.clicked.connect(lambda x:self.board_widget.redo_all())

        self._update_board_widgets()

    def _current_engine(self):
        # returns the current engine used
        # poll the dict of engines
        engines = getMainWindow().getEngineConfigWidget().engines.engines

        # check if the current selected engine is inside engines (this should always be true)
        if self.engine_combo.currentText() in engines:
            return engines[self.engine_combo.currentText()]
        else:
            return None

    def _process_engine_line(self, line):
        # we assume that all engines only follow the uci protocol. This is checked when selecting the engine

        # create a function to fill the label with the correct value
        func = lambda label, split, value: label.setText(
            split[split.index(value) + 1] if value in split and len(split) > split.index(value) + 1 else label.text())

        # split the string
        split = line.lower().split()

        # write all the labels
        func(self.   nodes_label, split, 'nodes')
        func(self.     nps_label, split, 'nps')
        func(self.   depth_label, split, 'depth')
        func(self.seldepth_label, split, 'seldepth')
        func(self.    time_label, split, 'time')
        func(self.  tbhits_label, split, 'tbhits')


        # update the score
        if 'mate' in split and len(split) > split.index('mate') + 1:
            self._update_score(mate=split[split.index('mate')+1])
        elif 'score' in split and len(split) > split.index('score') + 1:
            self._update_score(mate=split[split.index('score')+1])

        # processing the pv
        pv_index = 0
        if 'multipv' in split and split.index('multipv')+1 < len(split):
            pv_index = int(split[split.index('multipv')+1])

        # ignore more than 5 pvs
        if pv_index >= 5:
            return

        # return if there is no pv or the pv is empty
        if 'pv' not in split or split[-1] == 'pv':
            return

        # get the pv
        pv = split[split.index('pv') + 1:]

        # if the pv is empty, dont do anything
        if len(pv) == 0:
            return

        # make sure there are enough arrows in the board widget
        if len(self.board_widget.arrows) < 5:
            self.board_widget.arrows += [BoardArrow(0,0,0)] * (5 - len(self.board_widget.arrows))

        # get the first move and display that as an arrow
        move = chess.Move.from_uci(pv[0])
        self.board_widget.arrows[pv_index] = BoardArrow(25 - pv_index * 3, move.from_square, move.to_square)


    def _change_page(self, index):
        # disable piece setting
        self._set_piece_button_pressed(0,False)
        self.tab_stack.setCurrentIndex(index)

    def _retrieve_search_fen_and_moves(self):
        # retrieves the fen and moves which will be given to the engine in the format
        # setposition fen {fen} moves {moves}
        return self.board_widget.board.fen(), None

    def _update_search(self):
        # update the search if a move has happened or the board state changed
        if self._current_engine() is not None:
            fen,moves=self._retrieve_search_fen_and_moves()
            # send the search command
            self._current_engine().search(fen,moves)

    def _update_score(self, score=None, mate=None):
        # update the score display
        pass

    def _set_piece_button_pressed(self, piece, state):
        if state:
            self.stop_analysis()
            for i in range(7):
                if i is not piece:
                    self.setpiece_buttons[i].setChecked(False)
            self.board_widget.set_piece_placed(piece)
        else:
            for i in range(7):
                self.setpiece_buttons[i].setChecked(False)
            self.board_widget.set_piece_placed(None)
    def _castling_rights_change(self):
        pass
    def _update_board_widgets(self):
        self.fen_edit.setText(self.board_widget.board.fen())
    def _set_fen(self, fen):
        try:
            self.board_widget.board.set_fen(fen)
        except:
            pass
        self._update_board_widgets()
        self._board_changed()
        self.board_widget.refresh_board()
    def _board_changed(self):
        self._update_search()
        self._update_board_widgets()


    def stop_analysis(self):
        # stop the analysis
        # make sure the toggle button is toggle OFF
        self.analysetoggle_button.setChecked(False)

        # we can select other engines
        self.engine_combo.setEnabled(True)

        # if there is no engine available, no need to exit
        if self._current_engine() is None:
            return

        # exit the current engine. the function checks if the engine is running
        self._current_engine().exit()

    def start_analysis(self):
        # cannot start analysis if no engine is selected
        if self._current_engine() is None:
            return
        # listen to the output and wait 0.1 seconds
        self._current_engine().listen(self._process_engine_line)
        time.sleep(0.1)
        # try to start the engine
        if self._current_engine().start():
            # make sure the toggle button is toggle ON
            self.analysetoggle_button.setChecked(True)
            # make sure we cannot select other engines
            self.engine_combo.setEnabled(False)
            # send the options
            self._current_engine().send_options()
            # sleep a bit so that the engine can start
            time.sleep(0.2)
            # update the search and give the search command on the current position
            self._update_search()

    def reload_engines(self):
        # reloads the engines list from the engineconfigwidget

        # if we have some engines stored, remove those
        while self.engine_combo.count() > 0:
            self.engine_combo.removeItem(0)

        # get the engines from the engine config widget
        engines = getMainWindow().getEngineConfigWidget().engines.engines

        # loop through them
        for key in engines:
            # only support uci engines for now
            if engines[key].settings['bin'] != '' and int(engines[key].settings['proto']) == Protocol.UCI:
                # add the engine to the list
                self.engine_combo.addItem(key)

        # enable the start of the analysis if we got atleast 1 engine
        self.analysetoggle_button.setEnabled(self.engine_combo.count() > 0)

        # clear the pvs
        self.pv1_button.setText("")
        self.pv2_button.setText("")
        self.pv3_button.setText("")
        self.pv4_button.setText("")
        self.pv5_button.setText("")

    def resizeEvent(self, e):
        self.boardroot_frame.setMinimumWidth(self.boardroot_frame.height())
        self.boardroot_frame.setMaximumWidth(self.boardroot_frame.height())

        for i in range(6):
            width = self.setpiece_buttons[i].width()
            self.setpiece_buttons[i].setMinimumHeight(width)
            self.setpiece_buttons[i].setMaximumHeight(width)
