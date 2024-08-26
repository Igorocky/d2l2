from enum import Enum

import pygame
from pygame import SurfaceType, Surface, Rect

from common import NOTE_TO_WHITE_KEY_IDX
from common import note_to_str, BLACK


class Clef(Enum):
    BASS = 'BASS'
    TREBLE = 'TREBLE'


BASS_MIDDLE_NOTE = 2 + 12 * 3 + 3
BASS_MIDDLE_NOE_WHITE_KEY_IDX = NOTE_TO_WHITE_KEY_IDX[BASS_MIDDLE_NOTE]
TREBLE_MIDDLE_NOTE = 2 + 12 * 5
TREBLE_MIDDLE_NOTE_WHITE_KEY_IDX = NOTE_TO_WHITE_KEY_IDX[TREBLE_MIDDLE_NOTE]
MAX_LEVEL_ABS = 14


def render_note(disp: Surface | SurfaceType, rect: Rect, clef: Clef, note: int) -> None:
    assert note in NOTE_TO_WHITE_KEY_IDX, f'note={note_to_str(note)}'
    white_key_idx = NOTE_TO_WHITE_KEY_IDX[note]
    note_level = white_key_idx - (
        BASS_MIDDLE_NOE_WHITE_KEY_IDX if clef == Clef.BASS else TREBLE_MIDDLE_NOTE_WHITE_KEY_IDX)
    assert abs(note_level) <= MAX_LEVEL_ABS, f'note_level={note_level}'
    level_dy = rect.height / (MAX_LEVEL_ABS * 2 + 2)
    middle_x = (rect.left + rect.right) / 2
    short_width = level_dy * 4
    half_short_width = short_width / 2
    color = BLACK
    for i in range(1, MAX_LEVEL_ABS * 2 + 2):
        cur_level = MAX_LEVEL_ABS + 1 - i
        if cur_level % 2 == 0:
            y = rect.top + i * level_dy
            if note_level <= cur_level < -4 or 4 < cur_level <= note_level:
                pygame.draw.line(disp, color, (middle_x - half_short_width, y), (middle_x + half_short_width, y))
            elif -4 <= cur_level <= 4:
                pygame.draw.line(disp, color, (rect.left, y), (rect.right, y))
    note_rect = Rect(0, 0, level_dy * 3, level_dy * 2)
    note_rect.center = (middle_x, rect.top + (MAX_LEVEL_ABS + 1 - note_level) * level_dy)
    pygame.draw.ellipse(disp, color, note_rect)
