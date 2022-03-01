import gui as g
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from PyQt5.QtWidgets import QApplication
import sys

# Loads the model.
model = tf.saved_model.load('assets\yolov3-704', tags=[tag_constants.SERVING])

# Main Functions. Opens the GUI window.
def window(m):
    app = QApplication(sys.argv)
    win = g.GUI(m)
    win.show()
    sys.exit(app.exec_())

window(model)
