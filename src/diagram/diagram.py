import sys

import pygame
import pygame.locals as pg
from pygame import Surface, SurfaceType

from common import GRAY
from state import State

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISP: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Diagram')


def main() -> None:
    state = State(centers=[(100+i*170,100) for i in range(6)])
    while True:
        handle_events(state)
        render_state(state)


def handle_events(state: State) -> None:
    for event in pygame.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            state.on_mouse_button_down(event.pos)
        elif event.type == pg.MOUSEBUTTONUP:
            state.on_mouse_button_up()
        elif event.type == pg.MOUSEMOTION:
            state.on_mouse_move(event.pos)


def render_state(state: State) -> None:
    if state.needs_rerender():
        DISP.fill(GRAY)
        state.render(DISP)
        state.mark_rendered()
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
