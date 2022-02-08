import sys
import os
from os import path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPixmap

from PIL import Image
from binvis.converter import convert_to_image
import string
import random


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Antivirus")
        self.setFixedSize(1200, 720)
        self.initUI()

        if os.name == 'posix':
            self.__home_path = path.expanduser('~')
        else:
            self.__home_path = os.environ['USERPROFILE']

    def initUI(self):
        title_font = QFont("Arial", 48)
        title_font.setBold(True)

        self.title = QLabel("Antivirus", self)
        self.title.setFont(title_font)
        self.title.setGeometry(495, 40, 210, 55)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(525, 165, 400, 400)

        self.file_button = QPushButton("Select File", self)
        self.file_button.setGeometry(500, 330, 200, 30)
        self.file_button.clicked.connect(self.launchFileDialog)

        self.confrim_button = QPushButton("Analyze", self)
        self.confrim_button.setGeometry(450, 630, 300, 40)
        self.confrim_button.clicked.connect(self.confirm_clicked)

        self.confrim_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                background-color: #000000;
                color: white;
                font-size: 20pt;
                border-radius: 10px;
            }
            
            QPushButton:disabled {
                background-color: #444444;
                color: #eeeeee;
            }
            """
        )

    def launchFileDialog(self):
        files_filter = "Executables (*.exe)"
        file_path, file_type = QFileDialog.getOpenFileName(self, caption="Select a .exe file", directory=os.path.join(
            os.path.join(self.__home_path, "Desktop")), filter=files_filter, initialFilter='Executables (*.exe)')

        malware_file_path = ''.join(random.choices(string.ascii_letters, k=16)) + ".png"
        self.malware_image = convert_to_image(256, file_path, malware_file_path)

        self.file_button.setGeometry(500, 120, 200, 30)

        image_pixmap = QPixmap(malware_file_path)
        self.image_label.setPixmap(image_pixmap)
        self.image_label.resize(image_pixmap.width(), image_pixmap.height())

        os.remove(malware_file_path)

    def confirm_clicked(self):
        self.confrim_button.setEnabled(False)
        msg = QMessageBox()
        msg.setWindowTitle("Analyzer")
        msg.setText("Analyzing...")
        msg.exec_()
        self.confrim_button.setEnabled(True)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
