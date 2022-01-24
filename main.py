from music_piece import MusicPiece
import cv2
import utility as u

test_img = cv2.imread(r'example_data\machine_data\jonathan.jpg')
test_data_path = r'example_data\machine_data\jonathan_results.txt'

# another example is twinkle

piece = MusicPiece(test_img, test_data_path, note_deviation=15)
piece.draw(test_img)
u.show_image(test_img, 2.5)

piece.create_midi(100, 120)