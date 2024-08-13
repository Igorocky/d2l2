import sys

import pygame
import pygame.locals as pg

from state import NotesState

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Notes')

WHITE = (255, 255, 255)
YELLOW = (234, 221, 202)


def main():
    state = NotesState(max_x=WINDOW_WIDTH, max_y=WINDOW_HEIGHT)
    while True:
        handle_events(state)
        render_state(state)


def handle_events(state: NotesState):
    for event in pygame.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if state.rect.collidepoint(event.pos):
                state.generate_next_rect()


def render_state(state: NotesState):
    if state.needs_rerender():
        DISPLAYSURF.fill(WHITE)
        render_rect(state)
        state.mark_rendered()
        pygame.display.update()
        fpsClock.tick(FPS)


def render_rect(state: NotesState):
    pygame.draw.rect(DISPLAYSURF, YELLOW, state.rect)


if __name__ == '__main__':
    main()
