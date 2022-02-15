from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
import utils as u
import cv2
import sys
from constants import WIN_WIDTH, WIN_HEIGHT, MARGIN, TEMPLATE_PATH


class GUI(QMainWindow):
    def __init__(self):
        self.img = cv2.imread(TEMPLATE_PATH)

        super(GUI, self).__init__()
        self._init_UI()
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle("DL5 Music Detector")

    def _init_UI(self):
        self.image_label = QLabel(self)

        img = QPixmap(u.convert_nparray_to_QPixmap(self.img))
        img = QPixmap.scaledToWidth(img, WIN_WIDTH//3 - 2 * MARGIN)
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()
        self.image_label.move(WIN_WIDTH//2 - self.image_label.width()//2, MARGIN)

        self._create_buttons()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
 
        painter.drawRect(self.image_label.x(), self.image_label.y(), self.image_label.width(), self.image_label.height())

    def _create_buttons(self):
        self.file_button = QPushButton("Upload Image", self)

        file_button_width, file_button_height = 200, 30
        self.file_button.setGeometry(WIN_WIDTH//2 - file_button_width//2, (self.image_label.height() + WIN_HEIGHT)//2 - MARGIN,
                                     file_button_width, file_button_height)
        self.file_button.clicked.connect(self._open_image_file)

    def _open_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Image File', "", "Image files (*.jpg *.jpeg *.png)")  # Path
        # Remember to handle null strings if canceled midway
        self.img = u.paste_on_template(cv2.imread(file_name))
        img = u.convert_nparray_to_QPixmap(self.img)
        img = QPixmap.scaledToWidth(img, WIN_WIDTH//3 - 2 * MARGIN)
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec_())


window()
