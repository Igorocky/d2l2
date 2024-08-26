from pygame import SurfaceType, Surface, Rect

from common import str_to_note
from keyboard import Keyboard
from staff import Clef
from staff import render_note


class NotesState:
    def __init__(self, window_width: int, window_height: int):
        self._mark_needs_rerender()
        keyboard_width = window_width * 0.9
        keyboard_height = keyboard_width * (15 / 122.5)
        keyboard_rect = Rect((window_width - keyboard_width) / 2, (window_height - keyboard_height) / 2, keyboard_width,
                             keyboard_height)
        self.keyboard = Keyboard(keyboard_rect)
        staff_width = 60
        staff_height = staff_width * 4
        self.staff_rect = Rect(0, 0, staff_width, staff_height)
        self.staff_rect.center = (window_width / 2, keyboard_rect.top / 2)

    def mark_rendered(self) -> None:
        self._needs_rerender = False

    def needs_rerender(self) -> bool:
        return self._needs_rerender

    def render(self, disp: Surface | SurfaceType):
        self.keyboard.render(disp)
        # render_note(disp, self.staff_rect, Clef.TREBLE, str_to_note('4G'))
        render_note(disp, self.staff_rect, Clef.BASS, str_to_note('4G'))

    def _mark_needs_rerender(self):
        self._needs_rerender = True
