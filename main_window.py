import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPainterPath, QRegion, QPainter
from board import ChessBoardWidget
from pieces import ChessGame

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BorderlessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_widget_width = 400  # Increased the default width for the left widget
        self.init_ui()

    def init_ui(self):
        # Remove the window title and borders
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set the background color to dark grey
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(50, 50, 50))  # RGB for dark grey
        self.setPalette(palette)

        # Set the window size
        self.setGeometry(100, 100, 1300, 800)  # x, y, width, height

        # Add widgets to the main window
        self.init_widgets()

    def init_widgets(self):
        # Initialize and add the SquareWidget
        self.square_widget = SquareWidget(self)
        self.adjust_square_widget()

        # Initialize and add the LeftWidget
        self.left_widget = LeftWidget(self)
        self.adjust_left_widget()

    def adjust_square_widget(self):
        # Adjust the SquareWidget position and size to centralize it horizontally and make it bigger
        window_width = self.width()
        window_height = self.height()
        square_size = 750  # New size for the square widget
        x_position = (window_width - square_size) // 2 + 250  # Shift to the right
        y_position = (window_height - square_size) // 2
        self.square_widget.setGeometry(x_position, y_position, square_size, square_size)

    def adjust_left_widget(self):
        # Adjust the LeftWidget position and size to fill the left portion
        self.left_widget.setGeometry(0, 0, self.left_widget_width, self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_square_widget()
        self.adjust_left_widget()
        self.set_rounded_corners()

    def set_rounded_corners(self):
        radius = 20  # Adjust the radius for rounded corners
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        else:
            self.dragging = False  # Ensure dragging is False if no valid drag starts

    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragging') and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

class SquareWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set the background color to lighter grey for the SquareWidget
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(70, 70, 70))  # RGB for lighter grey
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Create a layout for the chessboard
        self.chessboard_widget = ChessBoardWidget(self)
        self.chessboard_widget.setFixedSize(640, 640)  # Set chessboard size

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Center the chessboard widget within the square widget
        self.chessboard_widget.move((self.width() - self.chessboard_widget.width()) // 2, (self.height() - self.chessboard_widget.height()) // 2)
        self.set_rounded_corners()

    def set_rounded_corners(self):
        radius = 20  # Adjust the radius for rounded corners
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Convert mouse click to board coordinates
            square_size = self.chessboard_widget.width() // 8
            board_x = (event.x() - self.chessboard_widget.x()) // square_size
            board_y = (event.y() - self.chessboard_widget.y()) // square_size

            if 0 <= board_x < 8 and 0 <= board_y < 8:
                # Convert to UCI format (e.g., 'e2')
                uci_square = f"{chr(board_x + 97)}{8 - board_y}"

                # Delegate move logic to the ChessBoardWidget
                piece = self.chessboard_widget.get_piece_at(uci_square)  # Assuming a method to get the piece at a square
                if piece:
                    logging.debug(f"Clicked on piece: {piece.symbol()} at square: {uci_square}")

                # Check if the same piece is clicked again to deselect
                if hasattr(self, 'selected_square') and self.selected_square == uci_square:
                    logging.debug(f"Deselected piece at square: {uci_square}")
                    self.selected_square = None  # Deselect the piece
                    self.update()  # Redraw the board to reflect deselection
                    return

                if hasattr(self, 'selected_square') and self.selected_square:
                    move = f"{self.selected_square}{uci_square}"
                    logging.debug(f"Attempting to move piece from {self.selected_square} to {uci_square}")
                    if self.chessboard_widget.move_piece(move):
                        logging.debug(f"Move successful: {move}")
                    else:
                        logging.debug(f"Move failed: {move}")
                    self.selected_square = None  # Clear selection after a valid move
                    self.update()  # Redraw the board
                else:
                    self.selected_square = uci_square  # Select a piece
                    logging.debug(f"Selected square: {uci_square}")

class LeftWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set the background color to lighter grey for the LeftWidget
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(70, 70, 70))  # RGB for lighter grey
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Add a New Game button to the center of the LeftWidget
        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.setStyleSheet(
            "QPushButton { background-color: #CC5C5C; color: white; border-radius: 10px; padding: 10px; }"
            "QPushButton:hover { background-color: #FF4C4C; }"
            "QPushButton:pressed { background-color: #AA3C3C; }"
        )
        self.new_game_button.setFixedSize(100, 50)  # Set button size
        # Adjust button position dynamically to center it in the LeftWidget
        self.new_game_button.move(
            (self.width() - self.new_game_button.width()) // 2,  # Center horizontally
            (self.height() - self.new_game_button.height()) // 2  # Center vertically
        )
        self.new_game_button.clicked.connect(self.new_game)

    def new_game(self):
        # Logic to start a new game
        self.parent().square_widget.chessboard_widget.chess_game = ChessGame()
        self.parent().square_widget.chessboard_widget.update_board_state()
        self.parent().square_widget.chessboard_widget.update()  # Redraw the board

        # Remove the checkmate popup if it exists
        if hasattr(self.parent().square_widget.chessboard_widget, 'checkmate_popup'):
            self.parent().square_widget.chessboard_widget.checkmate_popup.deleteLater()
            del self.parent().square_widget.chessboard_widget.checkmate_popup

    def set_rounded_corners(self):
        radius = 0  # Adjust the radius for rounded corners
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_rounded_corners()
        # Re-center the button when the widget is resized
        self.new_game_button.move(
            (self.width() - self.new_game_button.width()) // 2,  # Center horizontally
            (self.height() - self.new_game_button.height()) // 2  # Center vertically
        )

    def set_width(self, width):
        """Set the width of the LeftWidget and adjust its geometry."""
        self.setGeometry(0, 0, width, self.parent().height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BorderlessWindow()
    window.show()
    sys.exit(app.exec_())
