import sys

import pygame
import pygame.locals as pg
from pygame import Surface, SurfaceType

from common import GRAY
from gamemanager import GameManager

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISP: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Notes')


def main() -> None:
    game_manager = GameManager(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, db_file_path=sys.argv[1])
    while True:
        handle_events(game_manager)
        render_state(game_manager)


def handle_events(state: GameManager) -> None:
    for event in pygame.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            state.handle_click(event.pos)


def render_state(state: GameManager) -> None:
    if state.needs_rerender():
        DISP.fill(GRAY)
        state.render(DISP)
        state.mark_rendered()
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
