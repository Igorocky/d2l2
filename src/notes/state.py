import random
from typing import Tuple

from pygame import SurfaceType, Surface, Rect

from common import is_white_key
from common import str_to_note
from keyboard import Keyboard
from staff import Clef
from staff import render_note


class NotesState:
    def __init__(self, window_width: int, window_height: int):
        keyboard_width = window_width * 0.9
        keyboard_height = keyboard_width * (15 / 122.5)
        keyboard_rect = Rect((window_width - keyboard_width) / 2, (window_height - keyboard_height) / 2, keyboard_width,
                             keyboard_height)
        self._keyboard = Keyboard(keyboard_rect)
        staff_width = 60
        staff_height = staff_width * 4
        self._staff_rect = Rect(0, 0, staff_width, staff_height)
        self._staff_rect.center = (window_width / 2, keyboard_rect.top / 2)

        self._show_keyboard = False
        self._generate_questions()
        self._mark_needs_rerender()

    def mark_rendered(self) -> None:
        self._needs_rerender = False

    def needs_rerender(self) -> bool:
        return self._needs_rerender

    def render(self, disp: Surface | SurfaceType):
        if self._show_keyboard:
            self._keyboard.render(disp)
        render_note(disp, self._staff_rect, self._questions[0][0], self._questions[0][1])

    def handle_click(self, pos: Tuple[int, int]) -> None:
        self._mark_needs_rerender()
        if not self._show_keyboard:
            self._show_keyboard = True
        else:
            clicked_note = self._keyboard.get_clicked_note(pos)
            if clicked_note is not None and self._questions[0][1] == clicked_note:
                self._show_keyboard = False
                if len(self._questions) == 1:
                    self._generate_questions()
                else:
                    self._questions.pop(0)

    def _mark_needs_rerender(self):
        self._needs_rerender = True

    def _generate_questions(self):
        self._questions = []
        for note in range(str_to_note('1D'), str_to_note('5D') + 1):
            if is_white_key(note):
                self._questions.append((Clef.BASS, note))
        for note in range(str_to_note('2B'), str_to_note('6B') + 1):
            if is_white_key(note):
                self._questions.append((Clef.TREBLE, note))
        random.shuffle(self._questions)
