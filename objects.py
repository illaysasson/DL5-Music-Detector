import cv2
from bounding_box import BoundingBox
import constants
import utils as u


# ======================================================== BASE CLASSES ========================================================
class Object:
    def __init__(self, bbox):
        self.bbox: BoundingBox = bbox

    def __str__(self):
        return str(self.bbox)

    def __repr__(self):
        return str(self)

    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (255,0,255), 4)

class Staff(Object):
    def __init__(self, bbox):
        super().__init__(bbox)
        self.line_height = self.bbox.height // 4

        bottom = self.bbox.max_corner[1]
        self.middle = bottom - self.line_height * 2 # middle B, can be replaced wit just bbox.y but this is more accurate
    
    def __str__(self):
        return "Staff: " + str(self.bbox)

# ======================================================== ADVANCED CLASSES ========================================================

class MusicalSymbol(Object):
    def __init__(self, bbox, staves):
        super().__init__(bbox)
        self.staff: Staff = self.find_closest_staff(staves)

    def find_closest_staff(self, staves):
        # Check y distance - bbox must be abs
        staves_bbox = [staff.bbox for staff in staves]
        distance_to_note = [abs(bbox.y-self.bbox.y) for bbox in staves_bbox]
        min_distance = min(distance_to_note)
        min_index = distance_to_note.index(min_distance)

        return staves[min_index]

class Note(MusicalSymbol):
    def __init__(self, bbox, staves, clef, is_line_note, note_deviation):
        super().__init__(bbox, staves)
        self.clef = clef # Treble or Bass
        self.is_line_note = is_line_note
        self.relative_pos = self.calculate_relative_pos(note_deviation) # According to middle of staff, B
        self.pitch = self.calculate_pitch()
        self.duration = self.calculate_duration()

    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (0,255,0), 2)
        image = cv2.putText(image, str(self.pitch), (self.bbox.max_corner[0], self.bbox.min_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 7)
        image = cv2.putText(image, str(self.pitch), (self.bbox.max_corner[0], self.bbox.min_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    def __str__(self):
        return str(self.pitch) #+ " Note: " + str(self.bbox)

    def calculate_relative_pos(self, note_deviation):
        if self.is_line_note:
            for i in range(0, 5): # change to 2 for only in staff
                # Going up
                line = self.staff.middle - self.staff.line_height * i
                if (line - note_deviation) < self.bbox.y < (line + note_deviation):
                    return i * 2
                
                # Going down
                line = self.staff.middle - self.staff.line_height * -i
                if (line - note_deviation) < self.bbox.y < (line + note_deviation):
                    return -i * 2
        else:
            for i in range(0, 5): # change to 3 for only in staff
                # Going up
                line = self.staff.middle - self.staff.line_height * i - self.staff.line_height//2
                if (line - note_deviation) < self.bbox.y < (line + note_deviation):
                    return 1 + i*2 
                
                # Going down
                line = self.staff.middle - self.staff.line_height * -i + self.staff.line_height//2
                if (line - note_deviation) < self.bbox.y < (line + note_deviation):
                    return -1 - i*2
        return None

    def set_clef(self, clef):
        self.clef = clef
        self.pitch = self.calculate_pitch()
    
    def calculate_pitch(self):
        if self.relative_pos is not None:
            if self.clef == 'Bass': # bass clef
                note_index = self.relative_pos % 7 - 6 # -1 because notes list starts with C, but when relative_pos=0 the note is B.
                octave_number = 4 + (self.relative_pos-6) // 7 # middle of the staff B4
            else: # treble clef is default
                note_index = self.relative_pos % 7 - 1 # -1 because notes list starts with C, but when relative_pos=0 the note is B.
                octave_number = 5 + (self.relative_pos-1) // 7 # middle of the staff D3

            return constants.NOTES[note_index] + str(octave_number)
        return None

    def calculate_duration(self):
        category = constants.CATEGORIES[self.bbox.category]

        if self.pitch == None: # If not is not recognized, then 0
            return 0
        elif 'Half' in category:
            return 2
        elif 'Whole' in category:
            return 4
        else:
            return 1