import pygame.draw
from pygame import Rect, Surface, SurfaceType

from common import BLACK
from common import WHITE


class Box:
    def __init__(self, created_at_sec: float, start_pos_x: float, start_pos_y: float, velocity_x_px_sec: float,
                 velocity_y_px_sec: float):
        self.created_at_sec = created_at_sec
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.curr_pos_x = start_pos_x
        self.curr_pos_y = start_pos_y
        self.velocity_x_px_sec = velocity_x_px_sec
        self.velocity_y_px_sec = velocity_y_px_sec

    def update_coords(self, curr_time_sec: float) -> None:
        time_shift = curr_time_sec - self.created_at_sec
        x_shift = self.velocity_x_px_sec * time_shift
        y_shift = self.velocity_y_px_sec * time_shift
        self.curr_pos_x = self.start_pos_x + x_shift
        self.curr_pos_y = self.start_pos_y + y_shift


class Conveyor:
    def __init__(self,
                 curr_time_sec: float,
                 conv_rect: Rect, min_gap_sec: int, max_gap_sec: int,
                 box_radius: int,
                 velocity_x_px_sec: float, velocity_y_px_sec: float,
                 box_origin_x: float, box_origin_y: float) -> None:
        self._conv_rect = conv_rect
        self._min_gap_millis = min_gap_sec
        self._max_gap_millis = max_gap_sec
        self._box_radius = box_radius
        self._velocity_x_px_sec = velocity_x_px_sec
        self._velocity_y_px_sec = velocity_y_px_sec
        self._box_origin_x = box_origin_x
        self._box_origin_y = box_origin_y

        self._boxes = [self._create_new_box(curr_time_sec)]

    def _create_new_box(self, curr_time_sec: float) -> Box:
        return Box(
            created_at_sec=curr_time_sec, start_pos_x=self._box_origin_x, start_pos_y=self._box_origin_y,
            velocity_x_px_sec=self._velocity_x_px_sec, velocity_y_px_sec=self._velocity_y_px_sec
        )

    def update(self, curr_time_sec: float) -> None:
        # move all boxes
        for box in self._boxes:
            box.update_coords(curr_time_sec)
        # remove missed boxes
        self._boxes = [box for box in self._boxes if self._conv_rect.collidepoint((box.curr_pos_x, box.curr_pos_y))]

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
        for box in self._boxes:
            pygame.draw.circle(disp, BLACK, (box.curr_pos_x, box.curr_pos_y), self._box_radius)
