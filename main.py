# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic

import res
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
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

#        elif event.type() == 129:
#            if abs(event.x() - self.width()) < 3:
#                print(time.time())

        return QMainWindow.eventFilter(self, source, event)

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
