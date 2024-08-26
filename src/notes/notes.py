import sys

import pygame
import pygame.locals as pg
from pygame import Surface, SurfaceType

from common import GRAY
from state import NotesState

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISP: Surface | SurfaceType = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Notes')


def main():
    state = NotesState(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)
    while True:
        handle_events(state)
        render_state(state)


def handle_events(state: NotesState):
    for event in pygame.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == pg.MOUSEBUTTONDOWN:
        #     if state.rect.collidepoint(event.pos):
        #         state.generate_next_rect()


def render_state(state: NotesState):
    if state.needs_rerender():
        DISP.fill(GRAY)
        state.render(DISP)
        state.mark_rendered()
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
