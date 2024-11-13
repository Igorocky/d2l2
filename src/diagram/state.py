import math
from typing import Tuple

import pygame
from pygame import SurfaceType, Surface

from common import YELLOW


class State:
    def __init__(self, centers: list[Tuple[float, float]], radius: float = 50):
        self.centers = centers.copy()
        self.radius = radius
        self.selected_idx: int | None = None
        self.selected_shift: Tuple[float, float] = 0, 0
        self._mark_needs_rerender()

    def _mark_needs_rerender(self) -> None:
        self._needs_rerender = True

    def mark_rendered(self) -> None:
        self._needs_rerender = False

    def needs_rerender(self) -> bool:
        return self._needs_rerender

    def render(self, disp: Surface | SurfaceType) -> None:
        for i in range(len(self.centers) - 1):
            pygame.draw.line(disp, YELLOW, self.centers[i], self.centers[i + 1])
        for c in self.centers:
            pygame.draw.circle(disp, YELLOW, c, self.radius)

    def on_mouse_button_down(self, pos: Tuple[int, int]) -> None:
        for i, c in enumerate(self.centers):
            if self.radius > math.sqrt((c[0] - pos[0]) ** 2 + (c[1] - pos[1]) ** 2):
                self.selected_idx = i
                self.selected_shift = c[0] - pos[0], c[1] - pos[1]
                print(f'{self.selected_idx=}')
                break

    def on_mouse_button_up(self) -> None:
        self.selected_idx = None

    def on_mouse_move(self, pos: Tuple[int, int]) -> None:
        if self.selected_idx is not None:
            self.centers[self.selected_idx] = self.selected_shift[0] + pos[0], self.selected_shift[1] + pos[1]
            self._mark_needs_rerender()
