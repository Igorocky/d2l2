import datetime
import random
import time
from typing import Tuple

import pygame
from pygame import SurfaceType, Surface, Rect

from common import WHITE, GRAY, note_to_str
from common import is_white_key
from common import str_to_note
from database import Database
from gamestate import State
from keyboard import Keyboard
from staff import Clef
from staff import render_note


class GameManager:
    def __init__(self, window_width: int, window_height: int, db_file_path: str):
        self._window_width = window_width
        self._window_height = window_height
        self._database = Database(db_file_path)
        self._database.backup()
        keyboard_width = window_width * 0.9
        keyboard_height = keyboard_width * (15 / 122.5)
        keyboard_rect = Rect((window_width - keyboard_width) / 2, (window_height - keyboard_height) / 2, keyboard_width,
                             keyboard_height)
        self._keyboard = Keyboard(keyboard_rect)
        staff_width = 60
        staff_height = staff_width * 4
        self._staff_rect = Rect(0, 0, staff_width, staff_height)
        self._staff_rect.center = (int(window_width / 2), int(keyboard_rect.top / 2))

        font_obj = pygame.font.Font('freesansbold.ttf', 32)
        self._text_surface_obj = font_obj.render('Click to start.', True, WHITE, GRAY)
        self._text_rect = self._text_surface_obj.get_rect()
        self._text_rect.center = (int(window_width / 2), int(keyboard_rect.top / 2))

        self._state = State()
        self._mark_needs_rerender()

    def mark_rendered(self) -> None:
        self._needs_rerender = False

    def needs_rerender(self) -> bool:
        return self._needs_rerender

    def render(self, disp: Surface | SurfaceType) -> None:
        if self._state.started:
            if self._state.show_keyboard:
                self._keyboard.render(disp)
            render_note(disp, self._staff_rect, self._state.questions[0][0], self._state.questions[0][1])
        else:
            disp.blit(self._text_surface_obj, self._text_rect)
            self._keyboard.render(disp)

    def handle_click(self, pos: Tuple[int, int]) -> None:
        self._mark_needs_rerender()
        if not self._state.started:
            self._state.started = True
            self._generate_questions()
            self._state.asked_at = self._current_epoch_millis()
        else:
            if not self._state.show_keyboard:
                self._state.show_keyboard = True
            else:
                clicked_note = self._keyboard.get_clicked_note(pos)
                if clicked_note is not None:
                    if self._state.first_ans is None:
                        self._state.first_ans = clicked_note
                        self._log_ans()

                    if self._state.questions[0][1] == clicked_note:
                        self._state.show_keyboard = False
                        if len(self._state.questions) == 1:
                            self._generate_questions()
                        else:
                            self._state.questions.pop(0)
                        self._state.asked_at = self._current_epoch_millis()
                        self._state.first_ans = None

    def _log_ans(self) -> None:
        assert self._state.first_ans is not None, f'{self._state.first_ans=}'
        self._database.con.execute(
            """insert into TRAIN_LOG(ask_at, ask_at_str, ask_clef, ask_note, ask_note_name, ans_at, ans_note, ans_note_name) 
            values (:ask_at, :ask_at_str, :ask_clef, :ask_note, :ask_note_name, :ans_at, :ans_note, :ans_note_name)""",
            {
                'ask_at': self._state.asked_at,
                'ask_at_str': datetime.datetime.fromtimestamp(self._state.asked_at / 1000,
                                                              datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z'),
                'ask_clef': 'B' if self._state.questions[0][0] == Clef.BASS else 'T',
                'ask_note': self._state.questions[0][1],
                'ask_note_name': note_to_str(self._state.questions[0][1]),
                'ans_at': self._current_epoch_millis(),
                'ans_note': self._state.first_ans,
                'ans_note_name': note_to_str(self._state.first_ans)
            }
        )

    def _mark_needs_rerender(self) -> None:
        self._needs_rerender = True

    def _generate_questions(self) -> None:
        self._state.questions = []
        for note in range(str_to_note('1D'), str_to_note('5D') + 1):
            if is_white_key(note):
                self._state.questions.append((Clef.BASS, note))
        for note in range(str_to_note('2B'), str_to_note('6B') + 1):
            if is_white_key(note):
                self._state.questions.append((Clef.TREBLE, note))
        for _ in range(10):
            random.shuffle(self._state.questions)

    @staticmethod
    def _current_epoch_millis() -> int:
        return int(time.time() * 1000)
