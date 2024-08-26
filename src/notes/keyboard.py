import pygame
from pygame import Rect, Surface, SurfaceType

from common import DARK_GRAY, WHITE_KEYS, MAX_NOTE, is_white_key, NOTE_TO_WHITE_KEY_IDX, NUM_OF_WHITE_KEYS, YELLOWISH


class Keyboard:
    def __init__(self, rect: Rect):
        self.keyboard_rect = rect
        keyboard_width = rect.width
        keyboard_height = rect.height
        white_key_width = keyboard_width / NUM_OF_WHITE_KEYS
        black_key_width = white_key_width * (1.1 / 2.3)
        black_key_height = keyboard_height * (10 / 15)
        self.white_key_rects = [Rect(rect.left + i * white_key_width, rect.top, white_key_width, keyboard_height) for i
                                in range(len(WHITE_KEYS))]
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
