import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QRectF  # Ensure QRectF is imported
from PyQt5.QtGui import QPalette, QColor, QPainterPath, QRegion, QPixmap
from PyQt5.QtWidgets import QLabel
from board import ChessBoardWidget

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BorderlessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_widget_width = 100  # Increased the default width for the left widget
        self.init_ui()

    def init_ui(self):
        # Remove the window title and borders
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set the background color to dark grey
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(50, 50, 50))  # RGB for dark grey
        self.setPalette(palette)

        # Set the window size
        self.setGeometry(100, 100, 1300, 850)  # x, y, width, height

        # Add widgets to the main window
        self.init_widgets()

    def init_widgets(self):
        # Initialize and add the LeftWidget
        self.left_widget = LeftWidget(self)
        self.adjust_left_widget()

        # Initialize and add the ChessBoardWidget
        self.chessboard_widget = ChessBoardWidget(self)
        self.adjust_chessboard_widget()

        # Initialize and add the ThemeIconWidget
        self.theme_icon_widget = ThemeIconWidget(self.left_widget)
        self.adjust_theme_icon_widget()

        # Initialize and add the ChessGameIconWidget
        self.chess_game_icon_widget = ChessGameIconWidget(self.left_widget)
        self.adjust_chess_game_icon_widget()

    def adjust_left_widget(self):
        # Adjust the LeftWidget position and size to fill the left portion
        self.left_widget.setGeometry(0, 0, self.left_widget_width, self.height())

    def adjust_chessboard_widget(self):
        # Adjust the ChessBoardWidget position and size to fit inside the right portion of the window
        chessboard_size = 720  # Set the chessboard size to 640
        self.chessboard_widget.setGeometry(
            self.left_widget_width + (self.width() - self.left_widget_width - chessboard_size) // 2,  # Center horizontally in the right area
            (self.height() - chessboard_size) // 2,  # Center vertically
            chessboard_size,
            chessboard_size
        )

    def adjust_theme_icon_widget(self):
        # Adjust the ThemeIconWidget position and size to be in the middle of the LeftWidget
        icon_size = min(self.left_widget.width(), self.left_widget.height()) // 3  # Adjust size relative to the LeftWidget
        self.theme_icon_widget.setGeometry(
            (self.left_widget.width() - icon_size) // 2,  # Center horizontally
            (self.left_widget.height() - icon_size) // 2,  # Center vertically
            icon_size,
            icon_size
        )

    def adjust_chess_game_icon_widget(self):
        # Adjust the ChessGameIconWidget position and size to place it a bit higher
        icon_size = min(self.left_widget.width(), self.left_widget.height()) // 2  # Keep size relative to the LeftWidget
        self.chess_game_icon_widget.setGeometry(
            (self.left_widget.width() - icon_size) // 2,  # Center horizontally
            (self.left_widget.height() - icon_size) // 2 - 70,  # Move higher by adjusting the vertical position
            icon_size,
            icon_size
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_left_widget()
        self.adjust_chessboard_widget()
        self.adjust_theme_icon_widget()
        self.adjust_chess_game_icon_widget()
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

class LeftWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set the background color to darker grey for the LeftWidget
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))  # RGB for darker grey
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def set_rounded_corners(self):
        radius = 0  # Adjust the radius for rounded corners
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_rounded_corners()

    def set_width(self, width):
        """Set the width of the LeftWidget and adjust its geometry."""
        self.setGeometry(0, 0, width, self.parent().height())

class ThemeIconWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set up the theme icon
        self.icon_label = QLabel(self)
        self.default_icon = QPixmap("src/assets/Theme Icons/white_theme_icon.png")
        self.hover_icon = QPixmap("src/assets/Theme Icons/red_theme_icon.png")
        self.icon_label.setPixmap(self.default_icon)
        self.icon_label.setScaledContents(True)

    def enterEvent(self, event):
        # Change to hover icon when the mouse enters the widget
        self.icon_label.setPixmap(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Revert to default icon when the mouse leaves the widget
        self.icon_label.setPixmap(self.default_icon)
        super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Center the icon within the widget and make it slightly bigger
        icon_size = int(min(self.width(), self.height()) * 1)  # Adjust size to 60% of the widget's dimensions
        self.icon_label.setGeometry(
            (self.width() - icon_size) // 2,  # Center horizontally
            (self.height() - icon_size) // 2,  # Center vertically
            icon_size,
            icon_size
        )

class ChessGameIconWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set up the chess game icon
        self.icon_label = QLabel(self)
        self.default_icon = QPixmap("src/assets/Play icon/white_chess_game.png")
        self.hover_icon = QPixmap("src/assets/Play icon/red_chess_game.png")
        self.icon_label.setPixmap(self.default_icon)
        self.icon_label.setScaledContents(True)

    def enterEvent(self, event):
        # Change to hover icon when the mouse enters the widget
        self.icon_label.setPixmap(self.hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Revert to default icon when the mouse leaves the widget
        self.icon_label.setPixmap(self.default_icon)
        super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Center the icon within the widget and ensure it fits without cropping
        icon_size = int(min(self.width(), self.height()) * 0.8)  # Reduce size to 90% of the widget's dimensions
        self.icon_label.setGeometry(
            (self.width() - icon_size) // 2,  # Center horizontally
            (self.height() - icon_size) // 2,  # Center vertically
            icon_size,
            icon_size
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BorderlessWindow()
    window.show()
    sys.exit(app.exec_())
