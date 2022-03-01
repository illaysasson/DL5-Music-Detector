from objects import Note, Staff, BoundingBox
from midiutil import MIDIFile
from constants import INPUT_SIZE, MAX_TOTAL_SIZE, MAX_OUTPUT_SIZE_PER_CLASS, CATEGORIES
import tensorflow as tf
import numpy as np
from objects import BoundingBox
import utils as u
import cv2

# Represents a music piece
class MusicPiece:
    def __init__(self, img, model, mode, note_deviation):
        self.mode = mode

        self.note_deviation = note_deviation # for note calculations

        self.img = img
        self.img_height, self.img_width = img.shape[:2]

        staves_bbox, notes_bbox = self.predict(model)

        self.staves: Staff = self.create_staves(staves_bbox)
        self.notes: Note = self.create_notes(notes_bbox) # formatted like [[note1_in_staff1, note2_in_staff1], [note1_in_staff2, note2_in_staff2]]

    # Runs the model on the image and returns a list of bboxes of staves and notes
    def predict(self, model):
        # Pastes small images on template
        infer = model.signatures['serving_default']

        image_data = cv2.resize(self.img, (INPUT_SIZE, INPUT_SIZE))
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
        max_output_size_per_class=MAX_OUTPUT_SIZE_PER_CLASS
        max_total_size=MAX_TOTAL_SIZE
        iou_threshold=0.45
        score_threshold=0.25

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(boxes, scores, max_output_size_per_class, max_total_size, iou_threshold, score_threshold)
        image_h, image_w, _ = self.img.shape
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        out_boxes = pred_bbox[0]

        staves_bbox = []
        notes_bbox = []

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

            bbox = BoundingBox(cat, x, y, width, height)

            if CATEGORIES[bbox.category] == 'staff':
                staves_bbox.append(bbox)
            else:
                notes_bbox.append(bbox) # everything else is a note

        return staves_bbox, notes_bbox

    # Sorts (from top to bottom) and creates the staves list
    def create_staves(self, staves_bbox):
        staves_list = [Staff(bbox) for bbox in staves_bbox]
        staves_list.sort(key=lambda s: s.bbox.y) # sort by who's higher

        return staves_list
            
    # Sorts (from left to right for each staff) and creates the notes list
    def create_notes(self, notes_bbox):
        notes_list_unordered = []

        for note_bbox in notes_bbox:
            category = note_bbox.category
            if 'Line' in CATEGORIES[category]: # Later add the option for other classes and make this a general function
                notes_list_unordered.append(Note(note_bbox, self.staves, 'Treble', True, self.note_deviation))
            else:
                notes_list_unordered.append(Note(note_bbox, self.staves, 'Treble', False, self.note_deviation))

        # I can be efficent and put everything into one loop, but im lazy

        notes_list = []

        bass_counter = 1 # For piano mode, every even staff is a bass clef

        for staff in self.staves:
            notes_in_staff = []

            for note in notes_list_unordered:
                if note.staff == staff:
                    if bass_counter % 2 == 0 and self.mode==1:
                        note.set_clef('Bass')
                    notes_in_staff.append(note)
            
            notes_in_staff.sort(key=lambda n: n.bbox.x) # sort by who's first
            notes_list.append(notes_in_staff)

            bass_counter += 1

        return notes_list

    # Returns 2 lists - one that includes all of the note's durations in order, and the other and includes all of the note's MIDI number in order.
    def notes_to_degrees_and_duration(self):
        degrees = []
        duration = []

        for notes_lists in self.notes:
            for note in notes_lists:
                if note.pitch is not None or note.duration != 0: # Only notes that have pitch and duration
                    degrees.append(u.note_to_midi(note.pitch))
                    duration.append(note.duration)

        return degrees, duration

    # Creates the MIDI file
    def create_midi(self, volume, tempo):
        track = 0
        channel = 0
        time = 1 # In beats

        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(track, time, tempo)
        
        degrees, durations = self.notes_to_degrees_and_duration() # degrees: MIDI note number, duration: In beats

        for i, pitch in enumerate(degrees):
            MyMIDI.addNote(track, channel, pitch, time, durations[i], volume)
            time = time + durations[i]

        with open("song.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)

    # Draws on an image all of the staves and notes in the music piece
    def draw(self, img):
        for staff in self.staves:
            staff.draw(img)
        
        for notes_list in self.notes:
            for note in notes_list:
                note.draw(img)