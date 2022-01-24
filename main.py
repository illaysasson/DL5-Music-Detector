from bounding_box import BoundingBox
from music_piece import MusicPiece
import cv2
import utility as u

test_img = cv2.imread(r'example_data\machine_data\ido.jpg')
test_data_path = r'example_data\machine_data\ido_results.txt'

piece = MusicPiece(test_img, test_data_path)
piece.draw(test_img)
u.show_image(test_img, 2)


'''
img = cv2.imread(r'example_data\lg-2267728-aug-beethoven--page-2.png')
img_height, img_width = img.shape[:2]
note1_bbox = BoundingBox(1, 0.69819, 0.047022, 0.010713, 0.006531, img_width, img_height)
note2_bbox = BoundingBox(1, 0.907277, 0.059039, 0.010713, 0.006531, img_width, img_height)
note3_bbox = BoundingBox(2, 0.808275, 0.050157, 0.010344, 0.006792, img_width, img_height)
staff1_bbox = BoundingBox(0, 0.499815, 0.059039, 0.905061, 0.024556, img_width, img_height)
staff2_bbox = BoundingBox(0, 0.499815, 0.1186, 0.905061, 0.024295, img_width, img_height)


staff1 = Staff(staff1_bbox)
staff2 = Staff(staff2_bbox)
staves = [staff1, staff2]

note1 = Note(note1_bbox, staves, 'None', True)
note2 = Note(note2_bbox, staves, 'None', True)
note3 = Note(note3_bbox, staves, 'None', False)

staff1.draw(img)
staff2.draw(img)

print(note1)
note1.draw(img)

print(note2)
note2.draw(img)

print(note3)
note3.draw(img)

u.show_image(img, 3)
'''