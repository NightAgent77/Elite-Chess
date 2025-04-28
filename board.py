from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor

class ChessBoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pieces = {
            (0, 0): "rook_black.png", (0, 1): "knight_black.png", (0, 2): "bishop_black.png", (0, 3): "queen_black.png",
            (0, 4): "king_black.png", (0, 5): "bishop_black.png", (0, 6): "knight_black.png", (0, 7): "rook_black.png",
            (1, 0): "pawn_black.png", (1, 1): "pawn_black.png", (1, 2): "pawn_black.png", (1, 3): "pawn_black.png",
            (1, 4): "pawn_black.png", (1, 5): "pawn_black.png", (1, 6): "pawn_black.png", (1, 7): "pawn_black.png",
            (6, 0): "pawn_white.png", (6, 1): "pawn_white.png", (6, 2): "pawn_white.png", (6, 3): "pawn_white.png",
            (6, 4): "pawn_white.png", (6, 5): "pawn_white.png", (6, 6): "pawn_white.png", (6, 7): "pawn_white.png",
            (7, 0): "rook_white.png", (7, 1): "knight_white.png", (7, 2): "bishop_white.png", (7, 3): "queen_white.png",
            (7, 4): "king_white.png", (7, 5): "bishop_white.png", (7, 6): "knight_white.png", (7, 7): "rook_white.png",
        }

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Remove the black border and keep only the grey outer layer
        # Draw the outer layer with rounded corners
        outer_path = QPainterPath()
        corner_radius = 20
        outer_path.addRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)
        painter.fillPath(outer_path, QColor(85, 85, 85))  # Darker grey outer layer

        # Adjust the board size to include the outer layer
        board_size = min(self.width(), self.height()) - 40  # Add padding for the outer layer
        square_size = board_size // 8
        board_x = (self.width() - board_size) // 2
        board_y = (self.height() - board_size) // 2

        # Draw the chessboard background with rounded corners
        board_path = QPainterPath()
        board_path.addRoundedRect(board_x, board_y, board_size, board_size, corner_radius, corner_radius)
        painter.fillPath(board_path, Qt.white)

        # Clip painter to the chessboard region
        painter.save()
        painter.setClipPath(board_path)

        # Draw the board squares
        for row in range(8):
            for col in range(8):
                x = board_x + col * square_size
                y = board_y + row * square_size
                is_white = (row + col) % 2 == 0
                color = QColor(240, 217, 181) if is_white else QColor(181, 136, 99)
                painter.fillRect(QRect(x, y, square_size, square_size), color)

        # Restore painter state
        painter.restore()

        # Draw the numbers on the y-axis and letters on the x-axis
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # White text for clarity

        # Draw numbers (y-axis) on the left side
        for i in range(8):
            number = str(8 - i)
            text_x = board_x - 14  # Position to the left of the board
            text_y = board_y + i * square_size + (square_size + font.pointSize()) // 2  # Center vertically in the square
            painter.drawText(text_x, text_y, number)

        # Draw numbers (y-axis) on the right side
        for i in range(8):
            number = str(8 - i)
            text_x = board_x + board_size + 7  # Position to the right of the board
            text_y = board_y + i * square_size + (square_size + font.pointSize()) // 2  # Center vertically in the square
            painter.drawText(text_x, text_y, number)

        # Draw letters (x-axis) on the bottom side
        for i in range(8):
            letter = chr(ord('a') + i)
            text_x = board_x + i * square_size + (square_size - font.pointSize()) // 2  # Center horizontally in the square
            text_y = board_y + board_size + 14  # Position below the board
            painter.drawText(text_x, text_y, letter)

        # Draw letters (x-axis) on the upper side
        for i in range(8):
            letter = chr(ord('a') + i)
            text_x = board_x + i * square_size + (square_size - font.pointSize()) // 2  # Center horizontally in the square
            text_y = board_y - 7  # Position above the board
            painter.drawText(text_x, text_y, letter)

        # Ensure balanced save/restore calls
        painter.save()
        # Draw the pieces
        for (row, col), image_name in self.pieces.items():
            piece_image = QPixmap(f"src/assets/{image_name}")
            piece_margin = square_size * 0.1  # Add a margin to make the pieces slightly smaller
            x = int(board_x + col * square_size + piece_margin)
            y = int(board_y + row * square_size + piece_margin)
            piece_size = int(square_size - 2 * piece_margin)
            painter.drawPixmap(x, y, piece_size, piece_size, piece_image)

        painter.restore()  # Restore after drawing pieces
        painter.restore()  # Final restore for the outer layer
