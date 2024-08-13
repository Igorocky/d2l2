import random as rnd

from pygame import Rect


class NotesState:
    def __init__(self, max_x: int, max_y: int, min_x: int = 0, min_y: int = 0, rect_width: int = 30, rect_height: int = 30):
        self._needs_rerender = True
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.generate_next_rect()

    def mark_rendered(self):
        self._needs_rerender = False

    def mark_needs_rerender(self):
        self._needs_rerender = True

    def needs_rerender(self):
        return self._needs_rerender

    def generate_next_rect(self):
        self.mark_needs_rerender()
        self.rect = Rect(
            rnd.randint(self.min_x, self.max_x - self.rect_width),
            rnd.randint(self.min_y, self.max_y - self.rect_height),
            self.rect_width,
            self.rect_height
        )
