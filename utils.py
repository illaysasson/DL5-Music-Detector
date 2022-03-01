import cv2
from constants import TEMPLATE_PATH
from PyQt5.QtGui import QPixmap, QImage

# Shows and resizes an image
def show_image(img, img_size=None, multiplier=1):
    if img_size is not None:
        img = cv2.resize(img, (int(img_size[0]*multiplier), int(img_size[1]*multiplier)))
    cv2.imshow('image', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

# Pastes an image on the blank template, so it could match the GUI and the machine's ideal input size
def paste_on_template(img):
    new_img = cv2.imread(TEMPLATE_PATH)
    original_height, original_width, _ = img.shape
    resize_factor = new_img.shape[1] / original_width

    img = cv2.resize(img, (new_img.shape[1], round(original_height * resize_factor)))
    new_img[0:img.shape[0], 0:img.shape[1]] = img

    return new_img

# Converts an image to a QPixmap (for the GUI)
def convert_nparray_to_QPixmap(img):
    w,h,ch = img.shape
    # Convert resulting image to pixmap
    if img.ndim == 1:
        img =  cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    qimg = QImage(img.data, h, w, 3*h, QImage.Format_RGB888) 
    qpixmap = QPixmap(qimg)

    return qpixmap

# Returns the MIDI value of a note's pitch
# Thanks to Fusion_Prog_Guy from StackOverflow! https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
def note_to_midi(KeyOctave):
    # KeyOctave is formatted like 'C#3'

    notes_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]   # eg 3, 4
    answer = -1

    try:
        if 'b' in key:
            pos = notes_flat.index(key)
        else:
            pos = notes_sharp.index(key)
    except:
        print('The key is not valid', key)
        return answer

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer
