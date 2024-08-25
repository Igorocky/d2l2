from pygame import SurfaceType, Surface, Rect

from keyboard import Keyboard


class NotesState:
    def __init__(self, window_width: int, window_height: int):
        self._mark_needs_rerender()
        keyboard_width = window_width * 0.9
        keyboard_height = keyboard_width * (15 / 122.5)
        self.keyboard = Keyboard(
            Rect((window_width - keyboard_width) / 2, (window_height - keyboard_height) / 2, keyboard_width,
                 keyboard_height))

    def mark_rendered(self) -> None:
        self._needs_rerender = False

    def needs_rerender(self) -> bool:
        return self._needs_rerender

    def render(self, disp: Surface | SurfaceType):
        self.keyboard.render(disp)

    def _mark_needs_rerender(self):
        self._needs_rerender = True
