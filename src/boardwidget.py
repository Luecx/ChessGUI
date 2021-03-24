from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import chess


class BoardWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self._config()

    def _config(self):
        self.cellSize  = 100
        self.lightCell = QColor(0xecdab9)
        self.darkCell  = QColor(0xae8a68)
        self.board     = chess.Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 1")
        self.clickedAt = None
        self._create_board()
        self._create_pieces()
        self.listener  = None

    def _next_color(self, color):
        if color == self.darkCell:
            return self.lightCell
        else:
            return self.darkCell

    def resizeEvent(self, e):
        x, y = e.size().height(), e.size().width()
        self.cellSize = min(x, y) // 8
        self.refresh_pieces()
        self._refresh_board()
          
    def _get_index(self, square):
        return square // 8, square % 8

    def _get_color_label(self, piece):
        return 'w' if piece.color == chess.WHITE else 'b'
       
    def _piece_path(self, piece):
        return f'..//assets//images//{self._get_color_label(piece) + piece.symbol()}.png'

    def _refresh_board(self):
        self.boardPixmap = self.boardPixmap.scaled(self.cellSize * 8, self.cellSize * 8)
        self.boardLabel.setPixmap(self.boardPixmap)
        self.boardLabel.resize(self.cellSize * 8, self.cellSize * 8)

    def refresh_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece is None: 
                self.pieces[square].clear()
                continue
 

            i, j = self._get_index(chess.square_mirror(square))

            self.pieces[square].resize(self.cellSize,self.cellSize)
            self.pieces[square].move(j * self.cellSize, i * self.cellSize)
            self.pieces[square].setPixmap(QPixmap(self._piece_path(piece)).scaled(self.cellSize, self.cellSize, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
           i, j = e.y() // self.cellSize, e.x() // self.cellSize
           square = chess.square_mirror(i * 8 + j)
           
           if self.clickedAt is None:
               self.clickedAt = square 
               self.clickedAti = i 
               self.clickedAtj = j

           else:
               move = chess.Move(self.clickedAt, square)
               if move in self.board.legal_moves:
                   self.board.push(move)
                   self.refresh_pieces()
                   self.board_state_changed()
               self.clickedAt = None 

    def board_state_changed(self):
        if self.listener is not None:
            self.listener(self.board.fen())

    def listen(self, func):
        self.listener = func

    def _create_board(self):
        self.boardLabel  = QLabel(self)
        self.boardPixmap = QPixmap('../assets/images/board.png')
        self.boardPixmap = self.boardPixmap.scaled(self.cellSize * 8, self.cellSize * 8)
        self.boardLabel.setPixmap(self.boardPixmap)
        self.boardLabel.move(0, 0)
        self.boardLabel.setStyleSheet("background-color: black;")

    def _create_pieces(self):
        self.pieces = []
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            i, j = self._get_index(chess.square_mirror(square))

            label = QLabel(self)
            label.move(j * self.cellSize, i * self.cellSize)
            label.setStyleSheet("background-color:transparent")
            self.pieces.append(label)
