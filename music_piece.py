from objects import Note, Staff
from bounding_box import BoundingBox
from midiutil import MIDIFile
import constants
import utils as u

class MusicPiece:
    def __init__(self, img, model, mode, note_deviation):
        self.mode = mode

        self.note_deviation = note_deviation # for note calculations

        self.img = img
        self.img_height, self.img_width = img.shape[:2]

        staves_bbox, notes_bbox = self.predict_to_bbox(model)

        self.staves: Staff = self.create_staves(staves_bbox)
        self.notes: Note = self.create_notes(notes_bbox) # formatted like [[note1_in_staff1, note2_in_staff1], [note1_in_staff2, note2_in_staff2]]
            
    def draw(self, img):
        for staff in self.staves:
            staff.draw(img)
        
        for notes_list in self.notes:
            for note in notes_list:
                note.draw(img)

    def notes_to_degrees_and_duration(self):
        degrees = []
        duration = []

        for notes_lists in self.notes:
            for note in notes_lists:
                if note.pitch is not None or note.duration != 0: # Only notes that have pitch and duration
                    degrees.append(u.note_to_midi(note.pitch))
                    duration.append(note.duration)

        return degrees, duration

    def seperate_notes_to_degrees_and_duration(self):
        degrees = []
        durations = []

        for notes_list in self.notes:
            staff_durations = []
            staff_degrees = []
            for note in notes_list:
                if note.pitch is not None or note.duration != 0: # Only notes that have pitch and duration
                    staff_degrees.append(u.note_to_midi(note.pitch))
                    staff_durations.append(note.duration)
            degrees.append(staff_degrees)
            durations.append(staff_durations)

        return degrees, durations


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

    def predict_to_bbox(self, model):
        staves_bbox = []
        notes_bbox = []
        
        bboxes: BoundingBox = u.predict(model, self.img)

        for bbox in bboxes:
            if constants.CATEGORIES[bbox.category] == 'staff':
                staves_bbox.append(bbox)
            else:
                notes_bbox.append(bbox) # everything else is a note

        return staves_bbox, notes_bbox

    def create_staves(self, staves_bbox):
        staves_list = [Staff(bbox) for bbox in staves_bbox]
        staves_list.sort(key=lambda s: s.bbox.y) # sort by who's higher

        return staves_list
            
    def create_notes(self, notes_bbox):
        notes_list_unordered = []

        for note_bbox in notes_bbox:
            category = note_bbox.category
            if 'Line' in constants.CATEGORIES[category]: # Later add the option for other classes and make this a general function
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

    def __repr__(self):
        return str(self.notes)


    ''' FOR TESTING PURPOSES
    def dataset_file_into_bbox(self, data_path):
        staves_bbox = []
        notes_bbox = []

        with open(data_path, 'r') as file:
            for line in file:
                bbox_str = line.strip('\n').replace(' ', ', ') # string representation of list
                bbox = bbox_str.split(', ')
                bbox = [float(x) for x in bbox]
                bbox[0] = int(bbox[0]) # turn category into int
                category, x, y, width, height = bbox

                # Unpacking doesn't work here for some reason
                if constants.CATEGORIES[category] == 'staff':
                    staves_bbox.append(BoundingBox(category, x, y, width, height, self.img_width, self.img_height))
                else:
                    notes_bbox.append(BoundingBox(category, x, y, width, height, self.img_width, self.img_height)) # everything else is a note

        return staves_bbox, notes_bbox'''
