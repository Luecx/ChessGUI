# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5 import uic

import res

class TitleFrame(QWidget):
    def mousePressEvent(self, event):

        if event.buttons() == Qt.RightButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.RightButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

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

        self.title_frame.mouseMoveEvent = lambda x: self.window_move_event(x)
        self.title_frame.setMouseTracking(True)
#        self.title_frame.setMouseTracking(True)
#        self.mouse_tracker = MouseTracker(self.window.title_frame)
#        self.mouse_tracker.positionChanged.connect(self.window_move_event)

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
        self.open_menu_anim.setDuration(200)
        if mode:
            self.open_menu_anim.setEndValue(230)
        else:
            self.open_menu_anim.setEndValue(70)

        self.open_menu_anim.start()

    def window_move_event(self, event):
        if not hasattr(self, 'old_position'):
            self.old_position = event.pos()
            print(self.old_position)
            return
        print(event)
#        print(event.type)
#        print(event.pos())
#        self.window.move(self.pos() + event)
#        self.move(self.pos() + event)
#        event.accept()




if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
