import time

import pygame
import sys
from pygame import Surface, SurfaceType, Rect

from common import GRAY
from conveyor import Conveyor

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISP: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Conveyor')


def main() -> None:
    conv_rect = Rect(0, 0, 800, 50)
    conv_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    conveyor = Conveyor(
        curr_time_sec=time.time(),
        conv_rect=conv_rect,
        min_delay_sec=0.2,
        max_delay_sec=1,
        box_radius=20,
        velocity_x_px_sec=-300,
        velocity_y_px_sec=0,
        box_origin_x=conv_rect.right - 1,
        box_origin_y=(conv_rect.top + conv_rect.bottom) / 2
    )
    while True:
        curr_time_sec = time.time()
        conveyor.update(curr_time_sec)
        handle_events(conveyor)
        render(conveyor)


def handle_events(conveyor: Conveyor) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     state.handle_click(event.pos)


def render(conveyor: Conveyor) -> None:
    DISP.fill(GRAY)
    conveyor.render(DISP)
    pygame.display.update()
    fpsClock.tick(FPS)
    # print(f'{fpsClock.get_fps()=}')


if __name__ == '__main__':
    main()
