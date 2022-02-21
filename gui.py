from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QIcon
from PyQt5.QtCore import Qt
import utils as u
import numpy as np
import cv2
import pygame
import os
import webbrowser
from constants import WIN_WIDTH, WIN_HEIGHT, MARGIN, TEMPLATE_PATH, BLOCKS_MARGIN, DEFAULT_FONT


from music_piece import MusicPiece


class GUI(QMainWindow):
    def __init__(self, model):
        self.img = cv2.imread(TEMPLATE_PATH)
        self.model = model

        self.bpm = 120
        self.playing = False

        super(GUI, self).__init__()
        self._init_UI()
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle("DL5 Music Detector")

    def _init_UI(self):
        self.image_label = QLabel(self)

        img = QPixmap(u.convert_nparray_to_QPixmap(self.img))
        img = QPixmap.scaledToHeight(img, WIN_HEIGHT - (6 * MARGIN))
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()
        self.image_label.move(WIN_WIDTH//2 - self.image_label.width()//2, MARGIN)
        
        self._create_buttons_and_icons()
        self._create_settings_window()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 6, Qt.SolidLine))
        painter.drawRect(self.image_label.x(), self.image_label.y(), self.image_label.width(), self.image_label.height()) # Main Square

        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawRect(self.image_label.x() + self.image_label.width() + BLOCKS_MARGIN, self.image_label.y(), BLOCKS_MARGIN*2, self.image_label.height()) # Settings Square

    def _create_buttons_and_icons(self):
        self.file_button = QPushButton("Upload Image", self)

        file_button_width, file_button_height = 200, 30
        self.file_button.setGeometry(WIN_WIDTH//2 - file_button_width//2, (self.image_label.height() + WIN_HEIGHT)//2 - MARGIN,
                                     file_button_width, file_button_height)
        self.file_button.setFont(QFont(DEFAULT_FONT, 12))
        self.file_button.clicked.connect(self._open_image_file)

        github_icon_size = 200
        self.github_button = QPushButton(self)
        self.github_button.setIcon(QIcon('assets\github_icon.png'))
        self.github_button.setIconSize(QtCore.QSize(round(github_icon_size/2.5), round(github_icon_size/2.5)))
        self.github_button.setGeometry(self.image_label.x() - BLOCKS_MARGIN - github_icon_size, WIN_HEIGHT//2 - github_icon_size//2, github_icon_size, github_icon_size)
        self.github_button.clicked.connect(self._open_github)

    def _create_settings_window(self):
        settings_x = self.image_label.x() + self.image_label.width() + BLOCKS_MARGIN + MARGIN
        settings_y = self.image_label.y() + MARGIN
        settings_width = BLOCKS_MARGIN*2 - MARGIN*2
        settings_height = 30
        line_width = 90

        self.settings_label = QLabel("Settings", self)
        self.settings_label.setGeometry(settings_x, settings_y, settings_width, settings_height)
        self.settings_label.setFont(QFont(DEFAULT_FONT, 24))
        self.settings_label.adjustSize()
        self.settings_label.setFixedWidth(settings_width)
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter)
        settings_y += self.settings_label.height() + MARGIN

        self.mode_label = QLabel("Note Deviation:", self)
        self.mode_label.move(settings_x, settings_y)
        self.mode_label.setFont(QFont(DEFAULT_FONT, 16))
        self.mode_label.adjustSize()

        self.mode_line = QLineEdit(self)
        self.mode_line.setText('15')
        self.mode_line.setGeometry(self.mode_label.x() + self.mode_label.width() + MARGIN, self.mode_label.y(), line_width, self.mode_label.height())
        settings_y += self.mode_label.height() + MARGIN

        self.tempo_label = QLabel("Tempo (BPM):", self)
        self.tempo_label.move(settings_x, settings_y)
        self.tempo_label.setFont(QFont(DEFAULT_FONT, 16))
        self.tempo_label.adjustSize()

        self.tempo_line = QLineEdit(self)
        self.tempo_line.setText('120')
        self.tempo_line.setGeometry(self.tempo_label.x() + self.tempo_label.width() + MARGIN, self.tempo_label.y(), line_width, self.tempo_label.height())

        self.play_button = QPushButton("Play", self)
        self.play_button.setGeometry(settings_x, self.image_label.height() - MARGIN - settings_height, settings_width, settings_height)
        self.play_button.setFont(QFont(DEFAULT_FONT, 12))
        self.play_button.clicked.connect(self._play_midi_file)

        self.analyze_button = QPushButton("Analzye", self)
        self.analyze_button.setGeometry(settings_x, self.image_label.height() - MARGIN*2 - settings_height*2, settings_width, settings_height)
        self.analyze_button.setFont(QFont(DEFAULT_FONT, 12))
        self.analyze_button.clicked.connect(self._analyze_image)

    def _analyze_image(self):
        piece = MusicPiece(self.img, self.model, 0, int(self.mode_line.text()))
        piece.create_midi(100, int(self.tempo_line.text()))

        analyzed_img = np.copy(self.img)
        piece.draw(analyzed_img)
        img = u.convert_nparray_to_QPixmap(analyzed_img)
        img = QPixmap.scaledToHeight(img, WIN_HEIGHT - (6 * MARGIN))
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()


    def _play_midi_file(self):
        pygame.init()

        if not self.playing:
            self.playing = True
            pygame.mixer.music.load("song.mid")
            pygame.mixer.music.play()
        else:
            self.playing = False
            pygame.mixer.music.stop()

    def _open_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Image File', "", "Image files (*.jpg *.jpeg *.png)")  # Path
        # Remember to handle null strings if canceled midway
        print(file_name)
        if file_name == '':
            return
        self.img = u.paste_on_template(cv2.imread(file_name))
        img = u.convert_nparray_to_QPixmap(self.img)
        img = QPixmap.scaledToHeight(img, WIN_HEIGHT - (6 * MARGIN))
        self.image_label.setPixmap(img)
        self.image_label.adjustSize()

    def _open_github(self):
        webbrowser.open('https://github.com/illaysasson/DL5-Music-Detector')

    # Redfines the close event to remove the song.mid file after closing gui
    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        if os.path.exists("song.mid"):
            os.remove("song.mid")

