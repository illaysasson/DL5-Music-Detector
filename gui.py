from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QPixmap
import sys

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self._init_UI()
        self.setGeometry(200, 200, 600, 800)
        self.setWindowTitle("DL5 Music Detector")

    def _init_UI(self):
        self._create_menu_bar()

        self.label = QtWidgets.QLabel(self)
        self.label.setText("Hello")
        self.label.move(50, 50)

    def _create_menu_bar(self):
        # Overall menu bar
        menu_bar = self.menuBar()
        # File menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        open_file_action = QAction("Open Image", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(self._open_image_file)

        file_menu.addSeparator()

        save_midi_action = QAction("Save MIDI", self)
        save_midi_action.setShortcut("Ctrl+S")
        #save_midi_action.triggered.connect()

        file_menu.addSeparator()
        settings_action = QAction("Settings", self)
        #settings_action.triggered.connect()
        
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_midi_action)
        file_menu.addAction(settings_action)

        # Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        get_started_action = QAction("Get Started", self)
        #guide_action.triggered.connect()

        github_action = QAction("GitHub", self)
        #github_action.triggered.connect()

        help_menu.addAction(get_started_action)
        help_menu.addAction(github_action)

    def _open_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', "", "Image files (*.jpg *.jpeg *.gif)") # Path
        # Remember to handle null strings if canceled midway
        self.label.setPixmap(QPixmap(file_name))
        self.label.adjustSize()

def window(): 
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec_())

window()