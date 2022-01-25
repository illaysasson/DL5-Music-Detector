import cv2

def show_image(img, resize=None):
    if resize is not None:
        img = cv2.resize(img, resize)
    cv2.imshow('image', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

# Thanks to Fusion_Prog_Guy from StackOverflow! https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python
def note_to_midi(KeyOctave):
    # KeyOctave is formatted like 'C#3'

    notes_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]   # eg 3, 4
    answer = -1

    try:
        if 'b' in key:
            pos = notes_flat.index(key)
        else:
            pos = notes_sharp.index(key)
    except:
        print('The key is not valid', key)
        return answer

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer
