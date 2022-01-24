from objects import Note, Staff
from bounding_box import BoundingBox
import constants

class MusicPiece:
    def __init__(self, img, data_path, is_from_machine=True):
        self.img = img
        self.img_height, self.img_width = img.shape[:2]

        if is_from_machine:
            staves_bbox, notes_bbox = self.machine_file_into_bbox(data_path)
        else:
            staves_bbox, notes_bbox = self.dataset_file_into_bbox(data_path)
        self.staves: Staff = [Staff(bbox) for bbox in staves_bbox]
        self.notes: Note = self.create_notes(notes_bbox)
            
    def draw(self, img):
        for staff in self.staves:
            staff.draw(img)
        
        for note in self.notes:
            note.draw(img)

    def machine_line_into_bbox(self, line):
        list_line = line.split(' ')
        category_name = list_line[0].strip(":")
        category = constants.CATEGORIES.index(category_name)
        coords = [int(x.strip(')\n') for x in list_line if x.strip(')\n').isnumeric())]
        left_x, top_y, width, height = coords
        x, y = round(left_x + width/2), round(top_y + height/2)
        bbox = BoundingBox(category, x, y, width, height, self.img_width, self.img_height)

        return bbox

    def machine_file_into_bbox(self, data_path):
        print(data_path)
        staves_bbox = []
        notes_bbox = []
        line_count = 0

        with open(data_path, 'r') as file:
            for line in file:
                line_count += 1

                if line_count >= 10:
                    bbox: BoundingBox = self.machine_file_into_bbox(line)
                    
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


    def create_notes(self, notes_bbox):
        notes_list = []

        for note_bbox in notes_bbox:
            category = note_bbox.category
            if 'Line' in constants.CATEGORIES[category]: # Later add the option for other classes and make this a general function
                notes_list.append(Note(note_bbox, self.staves, None, True))
            else:
                notes_list.append(Note(note_bbox, self.staves, None, False))

        return notes_list

    def __repr__(self):
        return str(self.notes)
