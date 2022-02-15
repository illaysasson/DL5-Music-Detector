from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import utils as u
import cv2
import os
from constants import WIN_WIDTH, WIN_HEIGHT, MARGIN, TEMPLATE_PATH, BLOCKS_MARGIN
from midi2audio import FluidSynth


from music_piece import MusicPiece


class GUI(QMainWindow):
    def __init__(self, model):
        self.img = cv2.imread(TEMPLATE_PATH)
        self.model = model

        self.note_deviation = 15
        self.mode = 0
        self.bpm = 120

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

        self.player = QMediaPlayer()

        self._create_buttons()
        self._create_settings_window()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 6, Qt.SolidLine))
        painter.drawRect(self.image_label.x(), self.image_label.y(), self.image_label.width(), self.image_label.height()) # Main Square

        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawRect(self.image_label.x() + self.image_label.width() + BLOCKS_MARGIN, self.image_label.y(), BLOCKS_MARGIN*2, self.image_label.height()) # Settings Square

    def _create_buttons(self):
        self.file_button = QPushButton("Upload Image", self)

        file_button_width, file_button_height = 200, 30
        self.file_button.setGeometry(WIN_WIDTH//2 - file_button_width//2, (self.image_label.height() + WIN_HEIGHT)//2 - MARGIN,
                                     file_button_width, file_button_height)
        self.file_button.setFont(QFont('Arial', 12))
        self.file_button.clicked.connect(self._open_image_file)

    def _create_settings_window(self):
        settings_x = self.image_label.x() + self.image_label.width() + BLOCKS_MARGIN + MARGIN
        settings_y = self.image_label.y() + MARGIN
        settings_width = BLOCKS_MARGIN*2 - MARGIN*2
        settings_height = 30

        self.settings_label = QLabel("Settings", self)
        self.settings_label.setGeometry(settings_x, settings_y, settings_width, settings_height)
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_label.setFont(QFont('Arial', 16))
        # For other settings: add +margin+height everytime to y

        self.play_button = QPushButton("Play", self)
        self.play_button.setGeometry(settings_x, self.image_label.height() - MARGIN - settings_height, settings_width, settings_height)
        self.play_button.setFont(QFont('Arial', 12))
        self.play_button.clicked.connect(self._play_midi_file)

        self.analyze_button = QPushButton("Analzye", self)
        self.analyze_button.setGeometry(settings_x, self.image_label.height() - MARGIN*2 - settings_height*2, settings_width, settings_height)
        self.analyze_button.setFont(QFont('Arial', 12))
        self.analyze_button.clicked.connect(self._analyze_image)

    def _analyze_image(self):
        piece = MusicPiece(self.img, self.model, self.mode, self.note_deviation)
        piece.create_midi(100, 120)

        analyzed_img = self.img
        piece.draw(analyzed_img)
        img = u.convert_nparray_to_QPixmap(analyzed_img)
        img = QPixmap.scaledToWidth(img, WIN_WIDTH//3 - 2 * MARGIN)
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()


    def _play_midi_file(self):
        full_file_path = os.path.join(os.getcwd(), 'song.wav')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.player.play()

    def _open_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Image File', "", "Image files (*.jpg *.jpeg *.png)")  # Path
        # Remember to handle null strings if canceled midway
        self.img = u.paste_on_template(cv2.imread(file_name))
        img = u.convert_nparray_to_QPixmap(self.img)
        img = QPixmap.scaledToWidth(img, WIN_WIDTH//3 - 2 * MARGIN)
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()


