INPUT_SIZE = 704

NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
CATEGORIES = ["staff", "noteheadBlackOnLine", "noteheadBlackInSpace", "noteheadHalfOnLine", "noteheadHalfInSpace", "noteheadWholeOnLine", "noteheadWholeInSpace"]

MAX_OUTPUT_SIZE_PER_CLASS = 100 # For predictions
MAX_TOTAL_SIZE = 200 # For predictions

TEMPLATE_PATH = r'assets/template.jpg'

# GUI
WIN_WIDTH, WIN_HEIGHT = round(1920*0.9), round(1080*0.9)
BLOCKS_MARGIN = 150
MARGIN = 15
DEFAULT_FONT = 'Arial'
