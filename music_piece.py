from objects import Note, Staff
from bounding_box import BoundingBox
from midiutil import MIDIFile
import constants
import utility as u

class MusicPiece:
    def __init__(self, img, data_path, mode, note_deviation, is_from_machine=True):
        self.mode = mode

        self.note_deviation = note_deviation # for note calculations

        self.img = img
        self.img_height, self.img_width = img.shape[:2]

        if is_from_machine:
            staves_bbox, notes_bbox = self.machine_file_into_bbox(data_path)
        else:
            staves_bbox, notes_bbox = self.dataset_file_into_bbox(data_path)
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
        
        if self.mode == 0: # Normal
            degrees, durations = self.notes_to_degrees_and_duration() # degrees: MIDI note number, duration: In beats

            for i, pitch in enumerate(degrees):
                MyMIDI.addNote(track, channel, pitch, time, durations[i], volume)
                time = time + durations[i]
        elif self.mode == 1: # Piano
            degrees, durations = self.seperate_notes_to_degrees_and_duration()
            time_treble = 1
            time_bass = 1

            for staff_num in range(len(degrees)): # Goes through every staff
                if staff_num % 2 == 0: # Treble clef
                    for i in range(len(degrees[staff_num])):
                        MyMIDI.addNote(track, channel, degrees[staff_num][i], time_treble, durations[staff_num][i], volume)
                        time_treble = time_treble + durations[staff_num][i]
                else: # Bass clef
                    for i in range(len(degrees[staff_num])):
                        MyMIDI.addNote(track, channel, degrees[staff_num][i], time_bass, durations[staff_num][i], volume)
                        time_bass = time_bass + durations[staff_num][i]
        else:
            return

        with open("song.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)


    def machine_line_into_bbox(self, line):
        list_line = line.split(' ')
        category_name = list_line[0].strip(":")
        category = constants.CATEGORIES.index(category_name)
        coords = [int(x.strip(')\n')) for x in list_line if x.strip(')\n').strip('-').isnumeric()]
        left_x, top_y, width, height = coords
        x, y = round(left_x + width/2), round(top_y + height/2)
        bbox = BoundingBox(category, x, y, width, height, self.img_width, self.img_height)

        return bbox

    def machine_file_into_bbox(self, data_path):
        staves_bbox = []
        notes_bbox = []
        line_count = 0

        with open(data_path, 'r') as file:
            for line in file:
                line_count += 1

                if line_count > 10: # Actual detection starts from line 11
                    bbox: BoundingBox = self.machine_line_into_bbox(line)
                    
                    if constants.CATEGORIES[bbox.category] == 'staff':
                        staves_bbox.append(bbox)
                    else:
                        notes_bbox.append(bbox) # everything else is a note

        return staves_bbox, notes_bbox

    
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

    # To add for chords - Sort by first x, every note is a chord = a list of close notes ([A4 C4] or just [A4] if alone)
    def group_close_notes(self, notes):
        new_notes = []

        for note in notes:
            if note == notes[0]: # Skips the first one
                continue
            

    def __repr__(self):
        return str(self.notes)
