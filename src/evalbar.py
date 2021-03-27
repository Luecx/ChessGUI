import math
import time

from PyQt5.QtWidgets import QWidget, QLabel, QMainWindow, QDialog, QGridLayout, QPushButton, QApplication, QSizePolicy, \
    QFrame
from PyQt5.QtGui import QColor, QPixmap, QIcon, QColor, QBrush, QPainter, QPen, QPolygon, QResizeEvent
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QSize

class EvalBar(QFrame):

    def __init__(self, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self._config()
        self._init_base_label()
        self._init_anim_label()
        self.set_eval(3)


    def _config(self):
        self._eval = 0
        self._last_change = time.time()
        self._mate = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_eval(self, cp):
        if abs(cp) > 100000:
            self._mate = (abs(cp) - 100000) * 1 if cp > 0 else -1
        else:
            self._mate = None
        self._eval   = round(cp / 100, 2)
        self._change()

    def _eval_to_height(self):
        # uses a sigmoid function
        return int(1.0 / (1.0 + math.exp(self._eval / 1.5)) * self.height())

    def _change(self, duration=600):

        self._base_label.setText(str(self._eval) if self._mate is None else 'M'+str(self._mate))

        if time.time() - self._last_change < 1:
            return
        else:
            self._last_change = time.time()

        self.anim = QPropertyAnimation(self._anim_label, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(0,0,40,40))
        self.anim.setEndValue(QRect(1000,0,40,40))
        self.anim.start()
        # self._anim_label.setMinimumHeight(QSize(40,self._eval_to_height()))
        # self._anim_label.setMaximumHeight(self._eval_to_height())
        # self._anim_label.setFixedHeight(self._eval_to_height())

    def _init_anim_label(self):
        self._anim_label = QLabel(self)
        # self._anim_label.resize(self.width(), self.height() - self._eval_to_height())
        self._anim_label.setStyleSheet(""
                                       "background-color:black;"
                                       "border-top-left-radius:5px;"
                                       "border-top-right-radius:5px;")
        # self._anim_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._anim_label.setMinimumWidth(40)


    def _init_base_label(self):
        pass
        self._base_label = QLabel(self)
        self._base_label.resize(self.width(), self.height())
        self._base_label.setStyleSheet("background-color:white;border-radius:5px; font-size:18px; color: gray;")
        self._base_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self._base_label.setText(str(self._eval))


    def resizeEvent(self, a0: QResizeEvent) -> None:
        pass
        # self._base_label.resize(self.width(), self.height())
        # self._anim_label.resize(self.width(), self.height() - self._eval_to_height())

