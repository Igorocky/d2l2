WHITE = (255, 255, 255)
YELLOW = (234, 221, 202)
YELLOWISH = (255, 250, 226)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (70, 70, 70)

MAX_NOTE = 87
WHITE_KEYS_IN_OCTAVE = {0, 2, 4, 5, 7, 9, 11}
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def is_white_key(note: int) -> bool:
    if note == 0 or note == 2:
        return True
    if note == 1:
        return False
    note_12 = (note - 3) % 12
    return note_12 in WHITE_KEYS_IN_OCTAVE


WHITE_KEYS = [note for note in range(MAX_NOTE + 1) if is_white_key(note)]
NUM_OF_WHITE_KEYS = len(WHITE_KEYS)
NOTE_TO_WHITE_KEY_IDX: dict[int, int] = {note: idx for idx, note in enumerate(WHITE_KEYS)}


def note_to_str(note: int) -> str:
    if note == 0:
        return 'A0'
    elif note == 1:
        return 'A0#'
    elif note == 2:
        return 'B0'
    else:
        note = note - 3
        return f'{note // 12}{NOTE_NAMES[note % 12]}'
