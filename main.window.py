import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPainterPath, QRegion, QPainter
from board import ChessBoardWidget

class BorderlessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_widget_width = 400  # Increased the default width for the left widget
        self.init_ui()

    def init_ui(self):
        # Remove the window title and borders
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set the background color to white
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # RGB for white
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

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
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
        # Set the background color to very light grey
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # RGB for very light grey
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

class LeftWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Set the background color to very light grey
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # Same color as SquareWidget
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BorderlessWindow()
    window.show()
    sys.exit(app.exec_())
