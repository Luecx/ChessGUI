# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QPropertyAnimation, QFile
from PySide2.QtUiTools import QUiLoader

import res


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
#        window.setWindowFlag(Qt.FramelessWindowHint)
        self.window.menuopen_button.clicked.connect(lambda x: self.menu_animation(x))
        self.window.show()
        ui_file.close()

    def menu_animation(self, mode):
        self.open_menu_anim = QPropertyAnimation(self.window.menu_frame, b"minimumWidth")
        self.open_menu_anim.setDuration(300)
        if mode:
            self.open_menu_anim.setEndValue(230)
        else:
            self.open_menu_anim.setEndValue(70)

        self.open_menu_anim.start()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    sys.exit(app.exec_())
