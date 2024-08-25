import pygame
from pygame import Rect, Surface, SurfaceType

from common import DARK_GRAY
from common import YELLOWISH

MAX_NOTE = 87
WHITE_KEYS_IN_OCTAVE = {0, 2, 4, 5, 7, 9, 11}


def is_white_key(note: int) -> bool:
    if note == 0 or note == 2:
        return True
    if note == 1:
        return False
    note_12 = (note - 3) % 12
    return note_12 in WHITE_KEYS_IN_OCTAVE


WHITE_NOTES = [note for note in range(MAX_NOTE + 1) if is_white_key(note)]
NUM_OF_WHITE_KEYS = len(WHITE_NOTES)
NOTE_TO_WHITE_KEY_IDX: dict[int, int] = {note: idx for idx, note in enumerate(WHITE_NOTES)}


class Keyboard:
    def __init__(self, rect: Rect):
        self.keyboard_rect = rect
        keyboard_width = rect.width
        keyboard_height = rect.height
        white_key_width = keyboard_width / NUM_OF_WHITE_KEYS
        black_key_width = white_key_width * (1.1 / 2.3)
        black_key_height = keyboard_height * (10 / 15)
        self.white_key_rects = [Rect(rect.left + i * white_key_width, rect.top, white_key_width, keyboard_height) for i
                                in range(len(WHITE_NOTES))]
        self.black_key_rects = []
        for note in range(MAX_NOTE + 1):
            if not is_white_key(note):
                w_note = note - 1
                w_rect = self.white_key_rects[NOTE_TO_WHITE_KEY_IDX[w_note]]
                black_key_rect = Rect(0, rect.top, black_key_width, black_key_height)
                black_key_rect.centerx = w_rect.right
                self.black_key_rects.append(black_key_rect)

    def render(self, disp: Surface | SurfaceType):
        for rect in self.white_key_rects:
            pygame.draw.rect(disp, YELLOWISH, rect)
            pygame.draw.line(disp, DARK_GRAY, (rect.left, rect.top), (rect.left, rect.bottom))
        for rect in self.black_key_rects:
            pygame.draw.rect(disp, DARK_GRAY, rect)
        pygame.draw.lines(disp, DARK_GRAY, True,
                          [(self.keyboard_rect.left, self.keyboard_rect.top),
                           (self.keyboard_rect.right, self.keyboard_rect.top),
                           (self.keyboard_rect.right, self.keyboard_rect.bottom),
                           (self.keyboard_rect.left, self.keyboard_rect.bottom)])
