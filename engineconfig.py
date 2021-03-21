# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtQuick


class engineconfig(QtWidgets.QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.load_ui()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "engineconfig_form.ui")
        uic.loadUi(path, self)
