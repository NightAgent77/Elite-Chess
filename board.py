from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtCore import Qt

class ChessBoardWidget(QWidget):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the outer layer with rounded corners
        outer_path = QPainterPath()
        corner_radius = 20
        outer_path.addRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)
        painter.fillPath(outer_path, QColor(200, 200, 200))  # Light grey for the outer layer

        # Clip painter to the outer layer region
        painter.save()
        painter.setClipPath(outer_path)

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

        # Draw the chessboard squares
        for row in range(8):
            for col in range(8):
                color = QColor(240, 217, 181) if (row + col) % 2 == 0 else QColor(181, 136, 99)
                square_x = board_x + col * square_size
                square_y = board_y + row * square_size
                painter.fillRect(square_x, square_y, square_size, square_size, color)

        painter.restore()  # Restore painter state after clipping

        # Draw the labels for the x-axis (letters)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(Qt.black)
        letters = "ABCDEFGH"
        for i, letter in enumerate(letters):
            x = board_x + i * square_size + square_size // 2 - 2  # Slightly adjust to the left
            y = board_y + board_size + (self.height() - (board_y + board_size)) // 2 + 4  # Move slightly lower
            painter.drawText(x - 5, y, letter)

        # Draw the labels for the x-axis (letters) on the top side
        for i, letter in enumerate(letters):
            x = board_x + i * square_size + square_size // 2 - 2  # Slightly adjust to the left
            y = board_y - 6  # Move closer to the top edge of the outer layer
            painter.drawText(x - 5, y, letter)

        # Draw the labels for the y-axis (numbers)
        for i in range(8):
            x = board_x - (board_x // 2) - 3  # Move slightly more to the left
            y = board_y + i * square_size + square_size // 2 + 5
            painter.drawText(x, y, str(8 - i))

        # Draw the labels for the y-axis (numbers) on the right side
        for i in range(8):
            x = board_x + board_size + (self.width() - (board_x + board_size)) // 2 - 3  # Adjust to fit inside the outer layer
            y = board_y + i * square_size + square_size // 2 + 5
            painter.drawText(x, y, str(8 - i))

        painter.restore()  # Restore painter state after outer layer
