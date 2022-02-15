import gui as g
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from PyQt5.QtWidgets import QApplication
import sys

model = tf.saved_model.load('data\yolov3-704', tags=[tag_constants.SERVING])

def window(m):
    app = QApplication(sys.argv)
    win = g.GUI(m)
    win.show()
    sys.exit(app.exec_())

window(model)
