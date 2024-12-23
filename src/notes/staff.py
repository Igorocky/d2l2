from enum import Enum
from typing import Tuple

import pygame
from pygame import SurfaceType, Surface, Rect

from common import NOTE_TO_WHITE_KEY_IDX, str_to_note
from common import note_to_str, BLACK
from common import is_white_key


class Clef(Enum):
    BASS = 'BASS'
    TREBLE = 'TREBLE'


BASS_MIDDLE_NOTE = str_to_note('3D')
BASS_MIDDLE_NOE_WHITE_KEY_IDX = NOTE_TO_WHITE_KEY_IDX[BASS_MIDDLE_NOTE]
TREBLE_MIDDLE_NOTE = str_to_note('4B')
TREBLE_MIDDLE_NOTE_WHITE_KEY_IDX = NOTE_TO_WHITE_KEY_IDX[TREBLE_MIDDLE_NOTE]
MAX_LEVEL_ABS = 14

treble_clef_img = pygame.image.load('treble-clef.png')
bass_clef_img = pygame.image.load('bass-clef.png')


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
    note_rect.center = (int(middle_x), int(rect.top + (MAX_LEVEL_ABS + 1 - note_level) * level_dy))
    pygame.draw.ellipse(disp, color, note_rect)

    clef_img = treble_clef_img if clef == Clef.TREBLE else bass_clef_img
    clef_img_width, clef_img_height = clef_img.get_size()
    clef_img_height_new = (20 if clef == Clef.TREBLE else 7) * level_dy
    clef_img_width_new = clef_img_height_new * (clef_img_width / clef_img_height)
    clef_img = pygame.transform.smoothscale(clef_img, (clef_img_width_new, clef_img_height_new))
    clef_rect = Rect(0, 0, *clef_img.get_size())
    clef_rect.right = rect.left - 10
    middle_y = rect.top + (MAX_LEVEL_ABS + 1) * level_dy
    clef_rect.top = int(middle_y - clef_rect.height / 2 - (0 if clef == Clef.TREBLE else rect.height * 0.02))
    disp.blit(clef_img, clef_rect)


def get_all_notes() -> list[Tuple[Clef,int]]:
    res = []
    for note in range(str_to_note('1D'), str_to_note('5D') + 1):
        if is_white_key(note):
            res.append((Clef.BASS, note))
    for note in range(str_to_note('2B'), str_to_note('6B') + 1):
        if is_white_key(note):
            res.append((Clef.TREBLE, note))
    return res