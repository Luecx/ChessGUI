from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QDialog, QGridLayout, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QSize
import chess
import res
import time

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

    def _get_coordinate(self, square):
        i, j = self._get_index(square)
        return round(j * self.cellSize), round((7-i) * self.cellSize)

    def _get_square(self, x, y):
        return x // self.cellSize + (7 - y // self.cellSize) * 8

    def _get_color_label(self, piece):
        return 'w' if piece.color == chess.WHITE else 'b'
       
    def _piece_path(self, piece):
        return f'://pieces//images//{self._get_color_label(piece) + piece.symbol().lower()}.png'

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

            x, y = self._get_coordinate(square)

            self.pieces[square].resize(self.cellSize,self.cellSize)
            self.pieces[square].move(x,y)
            self.pieces[square].setPixmap(QPixmap(self._piece_path(piece)).scaled(self.cellSize, self.cellSize, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
           square = self._get_square(e.x(), e.y())
           
           if self.clickedAt is None:
               if self.board.piece_at(square) is not None and self.board.turn == self.board.piece_at(square).color:
                   self.clickedAt = square
                   self.pieces[self.clickedAt].setStyleSheet('border: 2px solid red; background-color:transparent;')
           else:
               self.pieces[self.clickedAt].setStyleSheet('border: 0px; background-color:transparent;')
               self.move_from_to(self.clickedAt, square)
               self.clickedAt = None

    def show_promotion_dialog(self):
        # creates a promotion dialog to select a piece and return that
        # (0 for knight, 1 for bishop, 2 for rook, 3 for queen)
        d = QDialog()
        # no dialog bar
        d.setWindowFlags(Qt.FramelessWindowHint)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        layout.setSpacing(0)
        # set default size
        d.resize(400,400)
        d.move(self.x(), self.y())

        promotionPiece = 0

        def clickEvent(promoPiece):
            nonlocal promotionPiece
            promotionPiece = promoPiece
            d.close()

        turn = self.board.turn
        pieces = [  chess.Piece(chess.KNIGHT,turn),
                    chess.Piece(chess.BISHOP,turn),
                    chess.Piece(chess.ROOK,turn),
                    chess.Piece(chess.QUEEN,turn)]

        for i in range(4):
            # add some chess board style
            squareType      = (i // 2 + i % 2 + 1) % 2
            squareColor     = ['#F0D9B7', '#B48866'][squareType]
            squareColorH    = ['#F8E2BF', '#BB9F6D'][squareType]
            button = QPushButton()
            # select the icon + icon size
            button.setIcon(QIcon(self._piece_path(pieces[i])))
            button.setIconSize(QSize(160,160))
            # fit the buttons
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda state, i=i: clickEvent(i))
            # background color
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {squareColor};
                    border: 0;
                }}

                QPushButton:hover {{
                    background-color: {squareColorH};
                }}
                """)
            # adding to the grid layout
            layout.addWidget(button, i // 2, i % 2)

        d.setLayout(layout)
        # make sure it cannot be closed without selection
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

        return promotionPiece

    def move_from_to(self, sq_from, sq_to):
        available_moves = [x for x in self.board.legal_moves if x.from_square == sq_from and x.to_square == sq_to]

        if len(available_moves) > 1:
            promo_piece = self.show_promotion_dialog() + 2
            for k in available_moves:
                if k.promotion == promo_piece:
                    available_moves[0] = k
            # handle promotion
        if len(available_moves) < 1:
            # no legal move
            return

        move = available_moves[0]
        self.board.push(move)

        x_from,y_from = self._get_coordinate(move.from_square)
        x_to  ,y_to   = self._get_coordinate(move.to_square)

        self.refresh_pieces()
        label = self.pieces[move.to_square]
        self.anim = QPropertyAnimation(label, b"pos")
        self.anim.setDuration(200)
        self.anim.setStartValue(QPoint(x_from, y_from))
        self.anim.setEndValue(QPoint(x_to,y_to))
        self.anim.start()

    def move_move(self, move):
        if move not in self.board.legal_moves:
            return

        self.board.push(move)

        x_from,y_from = self._get_coordinate(move.from_square)
        x_to  ,y_to   = self._get_coordinate(move.to_square)

        self.refresh_pieces()
        label = self.pieces[move.to_square]
        self.anim = QPropertyAnimation(label, b"pos")
        self.anim.setDuration(200)
        self.anim.setStartValue(QPoint(x_from, y_from))
        self.anim.setEndValue(QPoint(x_to,y_to))
        self.anim.start()

    def board_state_changed(self):
        if self.listener is not None:
            self.listener(self.board.fen())

    def listen(self, func):
        self.listener = func

    def _create_board(self):
        self.boardLabel  = QLabel(self)
        self.boardPixmap = QPixmap(":/boards/images/board.png")
        self.boardPixmap = self.boardPixmap.scaled(self.cellSize * 8, self.cellSize * 8)
        self.boardLabel.setPixmap(self.boardPixmap)
        self.boardLabel.move(0, 0)
        self.boardLabel.setStyleSheet("background-color: black;")

    def _create_pieces(self):
        self.pieces = []
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            x, y = self._get_coordinate(square)

            label = QLabel(self)
            label.move(x,y)
            label.setStyleSheet("background-color:transparent")
            self.pieces.append(label)
