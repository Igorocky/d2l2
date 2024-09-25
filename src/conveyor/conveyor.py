import math
import random
from typing import Callable

import pygame.draw
from pygame import Rect, Surface, SurfaceType
from pygame.font import Font

from common import BLACK, WHITE, PASTEL_RED, RED, PALE_GREEN


class Box:
    def __init__(self, created_at_sec: float, start_pos_x: float, start_pos_y: float, velocity_x_px_sec: float,
                 velocity_y_px_sec: float, radius: float):
        self.created_at_sec = created_at_sec
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.curr_pos_x = start_pos_x
        self.curr_pos_y = start_pos_y
        self.velocity_x_px_sec = velocity_x_px_sec
        self.velocity_y_px_sec = velocity_y_px_sec
        self.radius = radius
        self.is_focused = False
        self.is_failed = False

    def update_coords(self, curr_time_sec: float) -> None:
        time_shift = curr_time_sec - self.created_at_sec
        x_shift = self.velocity_x_px_sec * time_shift
        y_shift = self.velocity_y_px_sec * time_shift
        self.curr_pos_x = self.start_pos_x + x_shift
        self.curr_pos_y = self.start_pos_y + y_shift

    def contains_point(self, x: float, y: float) -> bool:
        return math.sqrt((x - self.curr_pos_x) ** 2 + (y - self.curr_pos_y) ** 2) < self.radius


class Conveyor:
    def __init__(self,
                 curr_time_sec: float,
                 conv_rect: Rect, min_delay_sec: float, max_delay_sec: float,
                 box_radius: int,
                 velocity_x_px_sec: float, velocity_y_px_sec: float,
                 box_origin_x: float, box_origin_y: float,
                 focus_point_x: float, focus_point_y: float,
                 draw_focus_line: Callable[[Surface | SurfaceType], None],
                 font: Font) -> None:
        self._created_at_sec = curr_time_sec
        self._conv_rect = conv_rect
        self._min_delay_sec = min_delay_sec
        self._max_delay_sec = max_delay_sec
        self._box_radius = box_radius
        self._velocity_x_px_sec = velocity_x_px_sec
        self._velocity_y_px_sec = velocity_y_px_sec
        self._box_origin_x = box_origin_x
        self._box_origin_y = box_origin_y
        self._cur_delay_sec = self._get_random_delay()
        self._boxes: list[Box] = []
        self._focus_point_x = focus_point_x
        self._focus_point_y = focus_point_y
        self._draw_focus_line = draw_focus_line
        self._error_cnt = 0
        self._font = font

    def _get_random_delay(self) -> float:
        return random.uniform(self._min_delay_sec, self._max_delay_sec)

    def _create_new_box(self, curr_time_sec: float) -> Box:
        return Box(
            created_at_sec=curr_time_sec, start_pos_x=self._box_origin_x, start_pos_y=self._box_origin_y,
            velocity_x_px_sec=self._velocity_x_px_sec, velocity_y_px_sec=self._velocity_y_px_sec,
            radius=self._box_radius
        )

    def _add_new_box_if_needed(self, curr_time_sec: float) -> None:
        last_time_sec = self._boxes[-1].created_at_sec if len(self._boxes) > 0 else self._created_at_sec
        if self._cur_delay_sec < curr_time_sec - last_time_sec:
            self._boxes.append(self._create_new_box(curr_time_sec))
            self._cur_delay_sec = self._get_random_delay()

    def update(self, curr_time_sec: float) -> None:
        # move all boxes
        for box in self._boxes:
            box.update_coords(curr_time_sec)
        # remove old boxes
        self._boxes = [box for box in self._boxes if self._conv_rect.collidepoint((box.curr_pos_x, box.curr_pos_y))]
        # add new boxes
        self._add_new_box_if_needed(curr_time_sec)
        # update focused/failed
        for box in self._boxes:
            if box.contains_point(self._focus_point_x, self._focus_point_y):
                box.is_focused = True
            elif box.is_focused:
                box.is_focused = False
                box.is_failed = True
                self._error_cnt += 1

    def remove_focused_boxes(self) -> None:
        old_boxes = self._boxes
        self._boxes = [box for box in self._boxes if not box.is_focused]
        if len(old_boxes) == len(self._boxes):
            self._error_cnt += 1

    def render(self, disp: Surface | SurfaceType) -> None:
        pygame.draw.lines(
            disp, WHITE, closed=True,
            points=[
                (self._conv_rect.left, self._conv_rect.top),
                (self._conv_rect.right, self._conv_rect.top),
                (self._conv_rect.right, self._conv_rect.bottom),
                (self._conv_rect.left, self._conv_rect.bottom),
            ]
        )
        text_surf = self._font.render(str(self._error_cnt), False, RED)
        text_surf = pygame.transform.scale_by(text_surf, self._conv_rect.height / text_surf.get_height())
        text_rect = text_surf.get_rect()
        text_rect.right = self._conv_rect.left - 50
        text_rect.top = self._conv_rect.top
        disp.blit(text_surf, text_rect)
        for box in self._boxes:
            color = PASTEL_RED if box.is_failed else PALE_GREEN if box.is_focused else BLACK
            pygame.draw.circle(disp, color, (box.curr_pos_x, box.curr_pos_y), self._box_radius)
        self._draw_focus_line(disp)
