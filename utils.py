import cv2
import constants
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from bounding_box import BoundingBox

def show_image(img, img_size=None, multiplier=1):
    if img_size is not None:
        img = cv2.resize(img, (int(img_size[0]*multiplier), int(img_size[1]*multiplier)))
    cv2.imshow('image', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

def predict(model, image):
    infer = model.signatures['serving_default']

    image_data = cv2.resize(image, (constants.INPUT_SIZE, constants.INPUT_SIZE))
    image_data = image_data / 255.

    images_data = []
    for i in range(1):
        images_data.append(image_data)
    images_data = np.asarray(images_data).astype(np.float32)

    batch_data = tf.constant(images_data)
    pred_bbox = infer(batch_data)

    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4))
    scores=tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1]))
    max_output_size_per_class=constants.MAX_OUTPUT_SIZE_PER_CLASS
    max_total_size=constants.MAX_TOTAL_SIZE
    iou_threshold=0.45
    score_threshold=0.25

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(boxes, scores, max_output_size_per_class, max_total_size, iou_threshold, score_threshold)
    image_h, image_w, _ = image.shape
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    out_boxes = pred_bbox[0]

    bboxes = []

    for i in range(out_boxes.shape[1]):
        coor = out_boxes[0][i]
        cat = int(pred_bbox[2][0][i])
        coor = [int(coor[1] * image_w), int(coor[0] * image_h), int(coor[3] * image_w), int(coor[2] * image_h)]

        width = coor[2] - coor[0]
        height = coor[3] - coor[1]
        x = round(coor[0] + width/2)
        y = round(coor[1] + height/2)

        if coor == [0, 0, 0, 0]: # Stop once hit the end of prediction
            break

        bboxes.append(BoundingBox(cat, x, y, width, height))

    return bboxes

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
