import sys
import os
import res
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PyQt5.QtCore import QPropertyAnimation, Qt, QEvent
from PyQt5 import uic
from board import *

class AnalyseWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.load_ui()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "analysewidget_form.ui")
        uic.loadUi(path, self)
        self.gridLayout.addWidget(Board(), 0, 0)
