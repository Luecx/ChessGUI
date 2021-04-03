# This Python file uses the following encoding: utf-8
import sys
import os
import res
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent, QPoint
from PyQt5.QtGui import QCursor
from PyQt5 import uic
from analysewidget import AnalyseWidget
from engineconfigwidget import EngineConfigWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.setup_central_widgets()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "main_form.ui")
        uic.loadUi(path, self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.menuopen_button.clicked.connect(lambda x: self._menu_animation(x))
        self.minimise_button.clicked.connect(lambda x:self._menu_buttons('minimise'))
        self.maximise_button.clicked.connect(lambda x:self._menu_buttons('maximise'))
        self.close_button.clicked.connect(lambda x:self._menu_buttons('close'))
        self.title_frame.installEventFilter(self)
        self.installEventFilter(self)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet(
            "background-color:#272935;"
            "color: rgb(210, 210, 210); "
            "font-size: 10px; "
            "font-family: 'Segoe UI'; "
            "font-weight:400;")
        self.title_frame.setMouseTracking(True)
        self.drag_root_position = QPoint()

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

        # binding a change of the current page
        self.content_stack.currentChanged.connect(lambda x:self._current_page_changed(x))

    def _menu_buttons(self, event):
        if event == 'maximise':
            self.previousWidth = self.width()
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        if event == 'close':
            self.close()
        if event == 'minimise':
            self.showMinimized()

    def _menu_animation(self, mode):
        self.open_menu_anim = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.open_menu_anim.setDuration(300)
        if mode:
            self.open_menu_anim.setEndValue(230)
        else:
            self.open_menu_anim.setEndValue(70)

        self.open_menu_anim.start()

    def _current_page_changed(self, new_index):
        self.getAnalyseWidget().stop_analysis()
        self.getAnalyseWidget().reload_engines()


    def eventFilter(self, source, event):
        if source == self.title_frame:
            # check if lmb is pressed
            if app.mouseButtons() & Qt.LeftButton:
                # check if the mouse is moving
                if event.type() == QEvent.MouseMove:
                    if self.ignore_movement:
                        return QMainWindow.eventFilter(self, source, event)
                    if self.isMaximized():
                        max_width       = self.width()
                        cursor_position = QCursor.pos().x()
                        self.showNormal()
                        new_width       = self.previousWidth
                        new_x           = cursor_position - new_width // 2
                        new_x           = max(+70,new_x)
                        new_x           = min(new_x, max_width - new_width + 70)
                        self.drag_root_position.setX(cursor_position - new_x)
                        self.move(new_x,0)
                    else:
                        if QCursor.pos().y() < 3:
                            self._menu_buttons('maximise')
                            self.ignore_movement = True
                        else:
                            self.move(event.pos() + self.title_frame.mapToGlobal(self.title_frame.pos()) - self.drag_root_position)
                elif event.type() == 2:
                    # init root position
                    self.drag_root_position = self.title_frame.mapToGlobal(event.pos()) - self.pos()
            else:
                self.ignore_movement = False
        return QMainWindow.eventFilter(self, source, event)

    def getAnalyseWidget(self):
        return self.analyse_widget

    def getEngineConfigWidget(self):
        return self.engineconfig_widget

if __name__ == "__main__":

    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
