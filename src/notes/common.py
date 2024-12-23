import time

WHITE = (255, 255, 255)
YELLOW = (234, 221, 202)
YELLOWISH = (255, 250, 226)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (70, 70, 70)
ERROR_COLOR = (210, 4, 45)

MAX_NOTE = 87
WHITE_KEYS_IN_OCTAVE = {0, 2, 4, 5, 7, 9, 11}
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def current_epoch_millis() -> int:
    return int(time.time() * 1000)


def is_white_key(note: int) -> bool:
    if note == 0 or note == 2:
        return True
    if note == 1:
        return False
    note_12 = (note - 3) % 12
    return note_12 in WHITE_KEYS_IN_OCTAVE


WHITE_KEYS = [note for note in range(MAX_NOTE + 1) if is_white_key(note)]
NUM_OF_WHITE_KEYS = len(WHITE_KEYS)
BLACK_KEYS = [note for note in range(MAX_NOTE + 1) if not is_white_key(note)]
NOTE_TO_WHITE_KEY_IDX: dict[int, int] = {note: idx for idx, note in enumerate(WHITE_KEYS)}


def note_to_str(note: int) -> str:
    if note == 0:
        return '0A'
    elif note == 1:
        return '0A#'
    elif note == 2:
        return '0B'
    else:
        note = note - 3
        return f'{(note // 12) + 1}{NOTE_NAMES[note % 12]}'


def str_to_note(name: str) -> int:
    assert 2 <= len(name) <= 3, f'{name=}'
    octave = int(name[0])
    rel_name = name[1:].upper()
    assert rel_name in NOTE_NAMES
    rel_idx = NOTE_NAMES.index(rel_name)
    if octave == 0:
        assert 0 <= rel_idx <= 2, f'{rel_idx=}'
        return rel_idx
    return 3 + (octave - 1) * 12 + rel_idx


def group_by_octaves(notes: list[int]) -> list[list[int]]:
    octaves: dict[str, list[int]] = {}
    for n in notes:
        oct = note_to_str(n)[0]
        if oct not in octaves:
            octaves[oct] = []
        octaves[oct].append(n)
    res = list(octaves.values())
    res.sort(key=lambda o: o[0])
    if len(res[0]) <= 3:
        res[1].extend(res[0])
        del res[0]
    if len(res[-1]) <= 3:
        res[-2].extend(res[-1])
        del res[-1]
    for grp in res:
        grp.sort()
    return res


def arrange_groups_for_learning(num_of_groups: int) -> list[list[int]]:
    res = [list(range(num_of_groups))]
    i = 0
    while i < len(res):
        cur = res[i]
        if len(cur) > 1:
            mid = len(cur) // 2 + len(cur) % 2
            res.insert(i + 1, cur[mid:len(cur)])
            res.insert(i + 2, cur[:mid])
        i += 1
    res.reverse()
    return res
