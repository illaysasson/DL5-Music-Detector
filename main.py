from music_piece import MusicPiece
import cv2
import utils as u
import constants
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants

img = cv2.imread(r'data\Capture.PNG')
if img.shape[0] > constants.INPUT_SIZE or img.shape[1] > constants.INPUT_SIZE:
    img = u.paste_on_template(img)
else:
    img = img

model = tf.saved_model.load('data\yolov3-704', tags=[tag_constants.SERVING])
piece = MusicPiece(img, model, mode=0, note_deviation=15)
# Mode 0 - Default: Just Treble clef
# Mode 1 - Piano: Treble & Bass clef
# Mode 2 - Orchestra: Just Treble but everything at once - TBA

piece.create_midi(100, 120)

piece.draw(img)
u.show_image(img, constants.WIN_SIZE, 1.5)
