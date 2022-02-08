from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton
from PyQt5.QtGui import QPixmap
import sys
from constants import WIN_WIDTH, WIN_HEIGHT, MARGIN


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self._init_UI()
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle("DL5 Music Detector")

    def _init_UI(self):
        self._create_buttons()

        self.image_label = QtWidgets.QLabel(self)
        img = QPixmap(r'data\jonathan.jpg')
        img = QPixmap.scaledToWidth(img, WIN_WIDTH//3)
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()
        
        self.image_label.move(img.width(), MARGIN)

    def _create_buttons(self):
        self.file_button = QPushButton("Upload Image", self)

        file_button_width, file_button_height = 200, 30
        self.file_button.setGeometry(WIN_WIDTH//2 - file_button_width//2, 4*WIN_HEIGHT//5 - file_button_height//2,
                                     file_button_width, file_button_height)
        self.file_button.clicked.connect(self._open_image_file)

    def _open_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Image File', "", "Image files (*.jpg *.jpeg *.gif)")  # Path
        # Remember to handle null strings if canceled midway
        #img = QPixmap(file_name)
        #img = QPixmap.scaledToHeight(img, 800)
        # self.label.setPixmap(img)
        # self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec_())


window()
