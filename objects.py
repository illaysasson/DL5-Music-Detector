import cv2
from bounding_box import BoundingBox
import constants
import utility as u


# ======================================================== BASE CLASSES ========================================================
class Object:
    def __init__(self, bbox):
        self.bbox: BoundingBox = bbox

    def __repr__(self):
        return str(self.bbox)

    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (0,0,255), 4)

class Staff(Object):
    def __init__(self, bbox):
        super().__init__(bbox)
        self.line_height = round(self.bbox.height / 4)

        bottom = self.bbox.max_corner[1]
        self.middle = bottom - self.line_height * 2 # middle B, can be replaced wit just bbox.y but this is more accurate

# ======================================================== ADVANCED CLASSES ========================================================

class MusicalSymbol(Object):
    def __init__(self, bbox, staff):
        super().__init__(bbox)
        self.staff: Staff = staff

class Clef(MusicalSymbol):
    def __init__(self, bbox, staff, name):
        super().__init__(bbox, staff)
        self.name = name

class Note(MusicalSymbol):
    def __init__(self, bbox, staff, clef, is_line_note):
        super().__init__(bbox, staff)
        self.clef: Clef = clef
        self.is_line_note = is_line_note
        self.relative_pos = self.find_relative_pos() # According to middle of staff, B
        self.pitch = None
        self.duration = None

    def find_relative_pos(self):
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

img = cv2.imread(r'C:\Users\illay\Documents\Coding Projects (C)\DL5 Music Detector\data\example_data\lg-2267728-aug-beethoven--page-2.png')
img_height, img_width = img.shape[:2]
note1_bbox = BoundingBox(1, 0.69819, 0.047022, 0.010713, 0.006531, img_width, img_height)
note2_bbox = BoundingBox(1, 0.907277, 0.059039, 0.010713, 0.006531, img_width, img_height)
note3_bbox = BoundingBox(2, 0.808275, 0.050157, 0.010344, 0.006792, img_width, img_height)
staff_bbox = BoundingBox(0, 0.499815, 0.059039, 0.905061, 0.024556, img_width, img_height)

staff = Staff(staff_bbox)
note1 = Note(note1_bbox, staff, 'None', True)
note2 = Note(note2_bbox, staff, 'None', True)
note3 = Note(note3_bbox, staff, 'None', False)

# add: calculate pitch