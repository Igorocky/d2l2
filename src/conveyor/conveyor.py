import pygame.draw
from pygame import Rect, Surface, SurfaceType

from common import BLACK
from common import WHITE


class Box:
    def __init__(self, created_at_sec: float, box_rect: Rect, velocity_x_px_sec: float, velocity_y_px_sec: float):
        self.created_at_sec = created_at_sec
        self.start_box_rect = box_rect
        self.box_rect = box_rect
        self.velocity_x_px_sec = velocity_x_px_sec
        self.velocity_y_px_sec = velocity_y_px_sec

    def update_coords(self, curr_time_sec: float) -> None:
        time_shift = curr_time_sec - self.created_at_sec
        x_shift = self.velocity_x_px_sec * time_shift
        y_shift = self.velocity_y_px_sec * time_shift
        self.box_rect.centerx = int(self.start_box_rect.centerx + x_shift)
        self.box_rect.centery = int(self.start_box_rect.centery + y_shift)


class Conveyor:
    def __init__(self,
                 curr_time_sec: float,
                 conv_rect: Rect, min_gap_sec: int, max_gap_sec: int,
                 box_width: int, box_height: int,
                 velocity_x_px_sec: float, velocity_y_px_sec: float,
                 box_origin_x: float, box_origin_y: float) -> None:
        self._conv_rect = conv_rect
        self._min_gap_millis = min_gap_sec
        self._max_gap_millis = max_gap_sec
        self._box_width = box_width
        self._box_height = box_height
        self._velocity_x_px_sec = velocity_x_px_sec
        self._velocity_y_px_sec = velocity_y_px_sec
        self._box_origin_x = box_origin_x
        self._box_origin_y = box_origin_y

        self._boxes = [self._create_new_box(curr_time_sec)]

    def _create_new_box(self, curr_time_sec: float) -> Box:
        box_rect = Rect(0, 0, self._box_width, self._box_height)
        box_rect.center = (int(self._box_origin_x), int(self._box_origin_y))
        return Box(
            created_at_sec=curr_time_sec, box_rect=box_rect,
            velocity_x_px_sec=self._velocity_x_px_sec, velocity_y_px_sec=self._velocity_y_px_sec
        )

    def update(self, curr_time_sec: float) -> None:
        # move all boxes
        for box in self._boxes:
            box.update_coords(curr_time_sec)
        # remove missed boxes
        self._boxes = [box for box in self._boxes if self._conv_rect.collidepoint(box.box_rect.center)]

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
            pygame.draw.rect(disp, BLACK, box.box_rect)
