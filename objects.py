import cv2
from bounding_box import BoundingBox
import constants
import utility as u


# ======================================================== BASE CLASSES ========================================================
class Object:
    def __init__(self, bbox):
        self.bbox: BoundingBox = bbox

    def __str__(self):
        return str(self.bbox)

    def __repr__(self):
        return str(self)

    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (0,0,255), 4)

class Staff(Object):
    def __init__(self, bbox):
        super().__init__(bbox)
        self.line_height = round(self.bbox.height / 4)

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


class Clef(MusicalSymbol):
    def __init__(self, bbox, staff, name):
        super().__init__(bbox, staff)
        self.name = name

class Note(MusicalSymbol):
    def __init__(self, bbox, staves, clef, is_line_note):
        super().__init__(bbox, staves)
        self.clef: Clef = clef
        self.is_line_note = is_line_note
        self.relative_pos = self.calculate_relative_pos() # According to middle of staff, B
        self.pitch = self.calculate_pitch()
        self.duration = None
        
    def __str__(self):
        return str(self.pitch) + " Note: " + str(self.bbox)

    def calculate_relative_pos(self):
        if self.is_line_note:
            for i in range(0, 3):
                # Going up
                line = self.staff.middle - self.staff.line_height * i
                if (line - constants.DEVIATION) < self.bbox.y < (line + constants.DEVIATION):
                    return i * 2
                
                # Going down
                line = self.staff.middle - self.staff.line_height * -i
                if (line - constants.DEVIATION) < self.bbox.y < (line + constants.DEVIATION):
                    return -i * 2
        else:
            for i in range(0, 2):
                # Going up
                line = self.staff.middle - self.staff.line_height * i - round(self.staff.line_height/2)
                if (line - constants.DEVIATION) < self.bbox.y < (line + constants.DEVIATION):
                    return 1 + i*2 
                
                # Going down
                line = self.staff.middle - self.staff.line_height * -i + round(self.staff.line_height/2)
                if (line - constants.DEVIATION) < self.bbox.y < (line + constants.DEVIATION):
                    return -1 - i*2
        return None

    def calculate_pitch(self):
        if self.relative_pos is not None:
            return constants.NOTES[self.relative_pos % 7] 
        return None