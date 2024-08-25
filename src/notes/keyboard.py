import pygame
from pygame import Rect, Surface, SurfaceType

from common import WHITE, BLACK

MAX_NOTE = 87
NUM_OF_WHITE_KEYS = 2 + 49 + 1
WHITE_KEYS_IN_OCTAVE = {0, 2, 4, 5, 7, 9, 11}


def is_white_key(note: int) -> bool:
    if note == 0 or note == 2:
        return True
    if note == 1:
        return False
    note_12 = (note - 3) % 12
    return note_12 in WHITE_KEYS_IN_OCTAVE


WHITE_NOTES = [note for note in range(MAX_NOTE + 1) if is_white_key(note)]
NOTE_TO_WHITE_KEY_IDX: dict[int, int] = {note: idx for idx, note in enumerate(WHITE_NOTES)}


class Keyboard:
    def __init__(self, rect: Rect):
        self.keyboard_rect = rect
        keyboard_width = rect.width
        keyboard_height = rect.height
        white_key_width = keyboard_width / NUM_OF_WHITE_KEYS
        black_key_width = white_key_width * 0.35
        self.white_key_rects = [Rect(rect.left + i * white_key_width, rect.top, white_key_width, keyboard_height) for i
                                in range(len(WHITE_NOTES))]

    def render(self, disp: Surface | SurfaceType):
        for rect in self.white_key_rects:
            pygame.draw.rect(disp, WHITE, rect)
            pygame.draw.lines(disp, BLACK, True,
                              [(rect.left, rect.top), (rect.right, rect.top), (rect.right, rect.bottom),
                               (rect.left, rect.bottom)])
