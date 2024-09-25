import sys
import time

import pygame
from pygame import Surface, SurfaceType, Rect
from pygame.font import Font

from common import GRAY, BLUE
from conveyor import Conveyor

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 400

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

pygame.font.init()
font: Font = pygame.font.SysFont('Comic Sans MS', 30)

DISP: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Conveyor')


def draw_focus_line(disp: Surface | SurfaceType, conv_rect: Rect, focus_point_x: float) -> None:
    pygame.draw.line(disp, BLUE, (focus_point_x, conv_rect.top), (focus_point_x, conv_rect.bottom), width=3)


def make_conveyor(conv_rect: Rect) -> Conveyor:
    box_origin_x = conv_rect.right - 1
    box_origin_y = (conv_rect.top + conv_rect.bottom) / 2
    focus_point_x: float = conv_rect.left + 0.2 * conv_rect.width
    radius = (conv_rect.height * 0.8) / 2
    seconds_till_focus_point = 10
    px_till_focus_point = conv_rect.right - focus_point_x
    min_gap_px = radius * 2 * 4
    max_gap_px = min_gap_px * 2
    abs_velocity_x_px_sec = px_till_focus_point / seconds_till_focus_point
    return Conveyor(
        curr_time_sec=time.time(),
        conv_rect=conv_rect,
        min_delay_sec=min_gap_px / abs_velocity_x_px_sec,
        max_delay_sec=max_gap_px / abs_velocity_x_px_sec,
        box_radius=int(radius),
        velocity_x_px_sec=-abs_velocity_x_px_sec,
        velocity_y_px_sec=0,
        box_origin_x=box_origin_x,
        box_origin_y=box_origin_y,
        focus_point_x=focus_point_x,
        focus_point_y=box_origin_y,
        draw_focus_line=lambda disp: draw_focus_line(disp, conv_rect, focus_point_x),
        font=font,
    )


GameState = dict[int, Conveyor]


def main() -> None:
    game_state: GameState = {}

    upper_conv_rect: Rect = Rect(0, 0, WINDOW_WIDTH * 0.8, 50)
    upper_conv_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    upper_conv_rect.top = int((WINDOW_HEIGHT - 3 * upper_conv_rect.height) / 2)
    upper_conv_rect.left += int(upper_conv_rect.height * 1.5)
    game_state[pygame.K_j] = make_conveyor(upper_conv_rect)

    lower_conv_rect = upper_conv_rect.copy()
    lower_conv_rect.top = upper_conv_rect.bottom + upper_conv_rect.height
    game_state[pygame.K_f] = make_conveyor(lower_conv_rect)

    while True:
        curr_time_sec = time.time()
        for conv in game_state.values():
            conv.update(curr_time_sec)
        handle_events(game_state)
        render(game_state)


def handle_events(game_state: GameState) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in game_state:
                game_state[event.key].remove_focused_boxes()


def render(game_state: GameState) -> None:
    DISP.fill(GRAY)
    for conv in game_state.values():
        conv.render(DISP)
    pygame.display.update()
    fpsClock.tick(FPS)
    # print(f'{fpsClock.get_fps()=}')


if __name__ == '__main__':
    main()
