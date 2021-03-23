# global function to display a message in the status bar
import typing

from PyQt5.QtWidgets import QApplication, QMainWindow


def updateStatusBar(text) -> typing.Union[QMainWindow, None]:
    # Global function to find the (open) QMainWindow in application
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            widget.statusBar.showMessage(text)
    return None

# global function to retrieve the main window
def getMainWindow():
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None
