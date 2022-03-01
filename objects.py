import cv2
import constants

# ======================================================== BOUNDING BOX ========================================================
# Represents the bounding box of an object
class BoundingBox:
    def __init__(self, category, x, y, width, height, image_width=None, image_height=None):
        self.category, self.x, self.y, self.width, self.height = category, x, y, width, height

        self.bbox = [self.category, self.x, self.y, self.width, self.height]
        if x < 1: # Doesn't account for screen-wide bboxes
            self.bbox = self.absolute_bbox(self.bbox, image_width, image_height)
            self.category, self.x, self.y, self.width, self.height = self.bbox

        self.min_corner, self.max_corner = self.bbox_to_corner()

    # Given an image width and height, returns the absolute bbox. Only works if the bbox is not absolute.
    def absolute_bbox(self, bbox, image_width, image_height):
        abs_mid_x, abs_mid_y, abs_width, abs_height = bbox[1] * image_width, bbox[2] * image_height, bbox[3] * image_width, bbox[4] * image_height
        abs_bbox = [bbox[0], round(abs_mid_x), round(abs_mid_y), round(abs_width), round(abs_height)]

        return abs_bbox

    # Returns the top left and bottom right corners of the bbox. For drawing purposes.
    def bbox_to_corner(self):
        category, abs_mid_x, abs_mid_y, abs_width, abs_height = self.bbox
        abs_min_x, abs_min_y = round(abs_mid_x - abs_width/2), round(abs_mid_y - abs_height/2)
        min_corner = (abs_min_x, abs_min_y)

        abs_max_x, abs_max_y = round(abs_mid_x + abs_width/2), round(abs_mid_y + abs_height/2)
        max_corner = (abs_max_x, abs_max_y)

        return min_corner, max_corner

    # Returns the bounding box as a string
    def __str__(self):
        return str(self.bbox)

    # Returns the bounding box as a string for printing
    def __repr__(self):
        return str(self)


# ======================================================== BASE CLASSES ========================================================
# Represents a basic YOLO object
class Object:
    def __init__(self, bbox):
        self.bbox: BoundingBox = bbox

    # Returns the bounding box as a string
    def __str__(self):
        return str(self.bbox)

    # Returns the bounding box as a string for printing
    def __repr__(self):
        return str(self)

    # Draws the bounding box of the object on a given image
    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (255,0,255), 4)

# Represents a staff
class Staff(Object):
    def __init__(self, bbox):
        super().__init__(bbox)
        self.line_height = self.bbox.height // 4

        self.middle = self.bbox.y # middle B
    
    # Returns the staff as a string
    def __str__(self):
        return "Staff: " + str(self.bbox)

# ======================================================== ADVANCED CLASSES ========================================================
# Represents a note
class Note(Object):
    def __init__(self, bbox, staves, clef, is_line_note, note_deviation):
        super().__init__(bbox)
        self.staff = self.find_closest_staff(staves)
        self.clef = clef # Treble or Bass
        self.is_line_note = is_line_note
        self.relative_pos = self.calculate_relative_pos(note_deviation) # According to middle of staff, B
        self.pitch = self.calculate_pitch()
        self.duration = self.calculate_duration()
    
    # Given a list of all staves in the music piece, returns the closest staff (according to the y coordinate)
    def find_closest_staff(self, staves):
        # Check y distance - bbox must be abs
        staves_bbox = [staff.bbox for staff in staves]
        distance_to_note = [abs(bbox.y-self.bbox.y) for bbox in staves_bbox]
        min_distance = min(distance_to_note)
        min_index = distance_to_note.index(min_distance)

        return staves[min_index]

    # Calculates the relative position of the note to the staff.
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

    # Changes the clef (either 'Treble' or 'Bass')
    def set_clef(self, clef):
        self.clef = clef
        self.pitch = self.calculate_pitch()
    
    # Calculates the pitch of the note according to its relative position
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

    # Returns the duration of the note according to its YOLO category
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

    # Draws the note's bounding box and the pitch of it
    def draw(self, image):
        image = cv2.rectangle(image, self.bbox.min_corner, self.bbox.max_corner, (0,255,0), 2)
        image = cv2.putText(image, str(self.pitch), (self.bbox.max_corner[0], self.bbox.min_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 7)
        #image = cv2.putText(image, str(self.pitch), (self.bbox.max_corner[0], self.bbox.min_corner[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1)
    
    # Returns the pitch as a string
    def __str__(self):
        return str(self.pitch) #+ " Note: " + str(self.bbox)