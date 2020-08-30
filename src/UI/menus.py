import sys
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)


def options_menu(screen: pygame.Surface):
    running = True
    screen.fill(BLACK)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()