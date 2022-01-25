from music_piece import MusicPiece
import cv2
import utility as u
import constants

test_img = cv2.imread(r'example_data\machine_data\twinkle.jpg')
test_data_path = r'example_data\machine_data\twinkle_results.txt'

piece = MusicPiece(test_img, test_data_path, mode=1, note_deviation=10)
# Mode 0 - Default: Just Treble clef
# Mode 1 - Piano: Treble & Bass clef
# Mode 2 - Orchestra: Just Treble but everything at once - TBA

piece.draw(test_img)
u.show_image(test_img, constants.WIN_SIZE)

piece.create_midi(100, 120)