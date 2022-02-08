import cv2

WIN_SIZE = (712, 990)
INPUT_SIZE = 704

NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
CATEGORIES = ["staff", "noteheadBlackOnLine", "noteheadBlackInSpace", "noteheadHalfOnLine", "noteheadHalfInSpace", "noteheadWholeOnLine", "noteheadWholeInSpace"]

MAX_OUTPUT_SIZE_PER_CLASS = 100 # For predictions
MAX_TOTAL_SIZE = 200 # For predictions

IMG_TEMPLATE = cv2.imread(r'data\template.jpg')

# GUI
WIN_WIDTH, WIN_HEIGHT = 1600, 800
MARGIN = 10