import math

from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QDialog, QGridLayout, QPushButton
from PyQt5.QtGui import QColor, QPixmap, QIcon, QColor, QBrush, QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QSize
import chess
import res
import time

class BoardArrow:
    width = 30
    sq_from = 0
    sq_to = 0

    def __init__(self, width, sq_from, sq_to):
        self.width = width
        self.sq_to = sq_to
        self.sq_from = sq_from

class BoardWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self._config()

    def _config(self):
        self.cellSize  = self.width() // 8
        self.lightCell = QColor(0xecdab9)
        self.darkCell  = QColor(0xae8a68)
        self.board     = chess.Board()
        self.arrow_panel = QLabel(self)
        self.boardPixmap = QPixmap(":/boards/images/board.png")
        self.clickedAt = None
        self._create_pieces()
        self.listener  = None
        self.piece_type_placing = None
        self.move_memory = []
        self.arrows      = []
        self.refresh_board()

        self.paintEvent             = lambda e : self._paint_background()
        self.arrow_panel.paintEvent = lambda e : self._paint_arrows()

    def _next_color(self, color):
        if color == self.darkCell:
            return self.lightCell
        else:
            return self.darkCell

    def resizeEvent(self, e):
        x, y = e.size().height(), e.size().width()
        self.cellSize = min(x, y) // 8
        self.refresh_board()
        self.arrow_panel.resize(self.width(), self.height())

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

    def _paint_background(self):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.boardPixmap)

    def _paint_arrows(self):

        def transform(x, y, r, x0, y0):
            return QPoint(x0 + math.cos(r) * x - math.sin(r) * y, y0 + math.sin(r) * x + math.cos(r) * y)

        self.arrow_panel.setStyleSheet("background-color:transparent;")
        self.arrow_panel.raise_()

        painter = QPainter(self.arrow_panel)
        # drawing the arrows

        # setting the brush for arrows
        brush = QBrush(QColor(100, 100, 100, 200))
        painter.setBrush(brush)

        # enable antialising
        painter.setRenderHint(QPainter.Antialiasing)

        # remove the border
        painter.setPen(QPen(QColor(0,0,0,0)))


        for arrow in self.arrows:
            if arrow.width <= 0:
                continue

            arrow_head_width = arrow.width * 3
            arrow_head_length = arrow_head_width

            x_from  , y_from = self._get_coordinate(arrow.sq_from)
            x_to    , y_to   = self._get_coordinate(arrow.sq_to)

            distance = math.sqrt((y_from - y_to) ** 2 + (x_from - x_to) ** 2)
            width    = arrow.width
            angle    = math.atan2(y_to - y_from, x_to - x_from) - math.pi / 2
            x0 = x_from + self.cellSize // 2
            y0 = y_from + self.cellSize // 2

            # draw an arrow. first create a polygon which will receive some points
            polygon = QPolygon()
            polygon.append(transform( width             / 2, 0                              ,angle,x0,y0))
            polygon.append(transform( width             / 2, distance - arrow_head_length   ,angle,x0,y0))
            polygon.append(transform( arrow_head_width  / 2, distance - arrow_head_length   ,angle,x0,y0))
            polygon.append(transform(                     0, distance                       ,angle,x0,y0))
            polygon.append(transform(-arrow_head_width  / 2, distance - arrow_head_length   ,angle,x0,y0))
            polygon.append(transform(-width             / 2, distance - arrow_head_length   ,angle,x0,y0))
            polygon.append(transform(-width             / 2, 0                              ,angle,x0,y0))

            painter.drawPolygon(polygon)

    def _create_pieces(self):
        self.pieces = []
        for square in range(64):
            x, y = self._get_coordinate(square)
            label = QLabel(self)
            label.move(x,y)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color:transparent")
            self.pieces.append(label)

    def refresh_board(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            x, y = self._get_coordinate(square)

            self.pieces[square].move(x, y)

            if piece is None:
                self.pieces[square].clear()
                continue

            self.pieces[square].resize(self.cellSize, self.cellSize)
            self.pieces[square].setPixmap(
                QPixmap(self._piece_path(piece)).scaled(self.cellSize, self.cellSize, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation))

    def set_piece_placed(self, piece_type=None):
        self.piece_type_placing = piece_type

    def mousePressEvent(self, e):

        # for placing a piece on the board
        if self.piece_type_placing is not None:
            square = self._get_square(e.x(), e.y())
            if self.piece_type_placing == 0:
                self.board.remove_piece_at(square)
            else:
                if e.button() == Qt.LeftButton:
                    self.board.set_piece_at(square, chess.Piece(self.piece_type_placing, chess.WHITE))
                elif e.button() == Qt.RightButton:
                    self.board.set_piece_at(square, chess.Piece(self.piece_type_placing, chess.BLACK))

            self.notify_listener()
            self.refresh_board()

        # for normal move recognition
        elif e.button() == Qt.LeftButton:
            square = self._get_square(e.x(), e.y())
            if self.clickedAt is None:
                # check if there is only a single valid move to this specific square (does consider promotions)
                if len(set(x.from_square + 64 * x.to_square for x in self.board.legal_moves if x.to_square == square)) == 1:
                    move = [x for x in self.board.legal_moves if x.to_square == square][0]
                    self.move_from_to(move.from_square, move.to_square)
                    self.notify_listener()
                    return

                # dont select the square if there is no piece on it of the correct color
                if self.board.piece_at(square) is None or self.board.turn != self.board.piece_at(square).color:
                    return

                # get the moves from that square
                moves           = [x for x in self.board.legal_moves if x.from_square == square]

                # if there is no legal move, do not select it
                if len(moves) == 0:
                    return

                # if there is only a single move, do it
                if len(moves) == 1:
                    self.move_move(moves[0])
                    self.notify_listener()
                    return

                # if there are multiple promotions, still do the move and request the promo piece
                if len(set(x.from_square + 64 * x.to_square for x in moves if x.from_square == square)) == 1:
                    self.move_from_to(moves[0].from_square, moves[0].to_square)
                    self.notify_listener()
                    return

                # otherwise select the square
                self.clickedAt = square
                self.pieces[self.clickedAt].setStyleSheet('border: 5px solid gray; border-radius:5px; background-color:transparent;')
                return
            else:
                self.pieces[self.clickedAt].setStyleSheet('border: 0px; background-color:transparent;')
                self.move_from_to(self.clickedAt, square)
                self.notify_listener()
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
        pieces = [  chess.Piece(chess.KNIGHT    ,turn),
                    chess.Piece(chess.BISHOP    ,turn),
                    chess.Piece(chess.ROOK      ,turn),
                    chess.Piece(chess.QUEEN     ,turn)]

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
        self.move_move(move)

    def move_move(self, move):
        if move not in self.board.legal_moves:
            return

        self.board.push(move)

        x_from,y_from = self._get_coordinate(move.from_square)
        x_to  ,y_to   = self._get_coordinate(move.to_square)

        self.refresh_board()
        label = self.pieces[move.to_square]
        self.anim = QPropertyAnimation(label, b"pos")
        self.anim.setDuration(200)
        self.anim.setStartValue(QPoint(x_from, y_from))
        self.anim.setEndValue(QPoint(x_to, y_to))
        self.anim.start()
        # self.anim.finished.connect(self.notify_listener)

        self.move_memory = []

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.move_memory = [self.board.pop()] + self.move_memory
        self.refresh_board()
        self.notify_listener()

    def undo_all(self):

        while len(self.board.move_stack) > 0:
            self.move_memory = [self.board.pop()] + self.move_memory

        self.board.clear_stack()
        self.refresh_board()
        self.notify_listener()

    def redo_move(self, refresh=True):
        if len(self.move_memory) > 0:
            self.board.push(self.move_memory[0])
            self.move_memory = self.move_memory[1:]
        if refresh:
            self.refresh_board()
            self.notify_listener()

    def redo_all(self):
        while len(self.move_memory) > 0:
            self.redo_move(refresh=False)
        self.refresh_board()
        self.notify_listener()

    def notify_listener(self):
        if self.listener is not None:
            self.listener(self.board.fen())

    def listen(self, func):
        self.listener = func
