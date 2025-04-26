from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, QRect
from pieces import ChessGame
import chess
import logging

# Ensure logging is configured
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ChessBoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chess_game = ChessGame()  # Initialize the chess game logic
        self.piece_images = self.load_piece_images()
        self.board_state = self.initialize_board_state()

    def load_piece_images(self):
        # Load piece images manually from the assets folder
        assets_path = "src/assets/"  # Adjusted path to match the workspace structure
        return {
            "P": QPixmap(assets_path + "pawn_white.png"),
            "p": QPixmap(assets_path + "pawn_black.png"),
            "R": QPixmap(assets_path + "rook_white.png"),
            "r": QPixmap(assets_path + "rook_black.png"),
            "N": QPixmap(assets_path + "knight_white.png"),
            "n": QPixmap(assets_path + "knight_black.png"),
            "B": QPixmap(assets_path + "bishop_white.png"),
            "b": QPixmap(assets_path + "bishop_black.png"),
            "Q": QPixmap(assets_path + "queen_white.png"),
            "q": QPixmap(assets_path + "queen_black.png"),
            "K": QPixmap(assets_path + "king_white.png"),
            "k": QPixmap(assets_path + "king_black.png"),
        }

    def initialize_board_state(self):
        # Initialize the board state using FEN notation
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

    def move_piece(self, move):
        if self.chess_game.move_piece(move):
            logging.debug(f"Move successful: {move}")
            self.update_board_state()
            self.update()  # Redraw the board
            # Check if the king is in check and log it
            if self.chess_game.board.is_check():
                logging.debug("The king is in check.")
            # Check for checkmate after a move
            if self.chess_game.board.is_checkmate():
                logging.debug("Checkmate detected.")
                self.show_checkmate_popup()
            return True  # Indicate the move was successful
        else:
            logging.debug(f"Move failed: {move}")
            return False  # Indicate the move failed

    def show_checkmate_popup(self):
        from PyQt5.QtWidgets import QLabel

        # Create a popup widget
        self.checkmate_popup = QLabel("Checkmate, You win!", self)
        self.checkmate_popup.setStyleSheet(
            "QLabel { background-color: rgba(0, 0, 0, 150); color: white; font-size: 24px; border-radius: 15px; padding: 20px; }"
        )
        self.checkmate_popup.setAlignment(Qt.AlignCenter)

        # Add a Gaussian blur effect to the background
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 150))
        shadow_effect.setOffset(0, 0)
        self.checkmate_popup.setGraphicsEffect(shadow_effect)

        # Set the size and position of the popup
        popup_width = self.width() // 2
        popup_height = self.height() // 4
        self.checkmate_popup.setFixedSize(popup_width, popup_height)
        self.checkmate_popup.move(
            (self.width() - popup_width) // 2,  # Center horizontally
            (self.height() - popup_height) // 2  # Center vertically
        )
        self.checkmate_popup.show()

    def update_board_state(self):
        # Update the board state based on the chess game's current state
        self.board_state = [[None for _ in range(8)] for _ in range(8)]
        for square, piece in self.chess_game.board.piece_map().items():
            row = 7 - (square // 8)
            col = square % 8
            self.board_state[row][col] = piece.symbol()

    def get_piece_at(self, uci_square):
        # Convert UCI square to board coordinates
        square = chess.parse_square(uci_square)
        piece = self.chess_game.board.piece_at(square)
        return piece

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the outer layer with rounded corners
        outer_path = QPainterPath()
        corner_radius = 20
        outer_path.addRoundedRect(0, 0, self.width(), self.height(), corner_radius, corner_radius)
        painter.fillPath(outer_path, QColor(85, 85, 85))  # Darker grey but lighter than the square widget

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

        # Draw the chess pieces
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece:
                    piece_image = self.piece_images[piece]
                    # Adjust the piece size to be slightly smaller than the square
                    piece_rect = QRect(
                        board_x + col * square_size + square_size // 10,  # Add padding
                        board_y + row * square_size + square_size // 10,  # Add padding
                        square_size - square_size // 5,  # Reduce size
                        square_size - square_size // 5   # Reduce size
                    )
                    painter.drawPixmap(piece_rect, piece_image)

        painter.restore()  # Restore painter state after clipping

        # Draw the labels for the x-axis (letters)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        # Set the pen color to white for labels
        painter.setPen(Qt.white)
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
