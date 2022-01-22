from bounding_box import BoundingBox
import cv2
import utility as u

def dataset_file_into_bbox(path, image_width, image_height):
    staves_bboxes = []
    notes_bboxes = []

    with open(path, 'r') as pred_file:
        for line in pred_file:
            unsorted_bbox = line.strip('\n').replace(' ', ', ') # string representation of list
            unsorted_bbox = unsorted_bbox.split(', ')
            unsorted_bbox = [float(x) for x in unsorted_bbox]
            unsorted_bbox[0] = int(unsorted_bbox[0]) # turn category into int
            bbox = BoundingBox(*unsorted_bbox, image_width=image_width, image_height=image_height) # Unpack unsorted bbox into arguements

            if bbox.category == 0:
                staves_bboxes.append(bbox)
            else:
                notes_bboxes.append(bbox)

    return staves_bboxes, notes_bboxes

img = cv2.imread(r'example_data\lg-2267728-aug-beethoven--page-2.png')
u.show_image(img, 2.5)
