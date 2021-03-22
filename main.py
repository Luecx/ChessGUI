# This Python file uses the following encoding: utf-8
import sys
import os
import res
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic
from analysewidget import *
from engineconfigwidget import *


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.setup_central_widgets()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "main_form.ui")
        uic.loadUi(path, self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.menuopen_button.clicked.connect(lambda x: self.menu_animation(x))
        self.minimise_button.clicked.connect(lambda x:self.menu_buttons('minimise'))
        self.maximise_button.clicked.connect(lambda x:self.menu_buttons('maximise'))
        self.close_button.clicked.connect(lambda x:self.menu_buttons('close'))
        self.title_frame.installEventFilter(self)
        self.installEventFilter(self)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background-color:#272935;")
        self.title_frame.setMouseTracking(True)

    def setup_central_widgets(self):

        # it is not possible to create an empty stack inside the ui file so we need to delete those two child widgets first
        self.analyse_widget.deleteLater()
        self.analyse_widget = None
        self.engineconfig_widget.deleteLater()
        self.engineconfig_widget = None

        # recreating the relevant widgets (add new widgets below)
        self.analyse_widget = AnalyseWidget()
        self.engineconfig_widget = EngineConfigWidget()

        # adding them to the stack
        self.content_stack.addWidget(self.analyse_widget)
        self.content_stack.addWidget(self.engineconfig_widget)

        # binding the buttons
        self.analyse_button.clicked.connect(lambda x:self.content_stack.setCurrentIndex(0))
        self.engineconfig_button.clicked.connect(lambda x:self.content_stack.setCurrentIndex(1))
        pass

    def menu_buttons(self, event):
        if event == 'maximise':
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        if event == 'close':
            self.close()
        if event == 'minimise':
            self.showMinimized()

    def menu_animation(self, mode):
        self.open_menu_anim = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.open_menu_anim.setDuration(300)
        if mode:
            self.open_menu_anim.setEndValue(230)
        else:
            self.open_menu_anim.setEndValue(70)

        self.open_menu_anim.start()

    def eventFilter(self, source, event):
        if source == self.title_frame:
            # check if lmb is pressed
            if app.mouseButtons() & Qt.LeftButton:
                # check if the mouse is moving
                if event.type() == QEvent.MouseMove:
                    if self.isMaximized():
                        self.showNormal()
                    self.move(event.pos() + self.title_frame.mapToGlobal(self.title_frame.pos()) - self.drag_root_position)
                elif event.type() == 2:
                    # init root position
                    self.drag_root_position = self.title_frame.mapToGlobal(event.pos()) - self.pos()
        return QMainWindow.eventFilter(self, source, event)

if __name__ == "__main__":

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
