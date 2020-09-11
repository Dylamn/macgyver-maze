import pygame
from pygame.locals import *

from src.mixer import Mixer
from src.utils import *

BLACK = (0, 0, 0)


def options_menu(screen: pygame.Surface):
    running = True
    screen.fill(BLACK)
    pygame.display.set_caption('MacGyver Maze - Options')

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_app()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()


def victory_screen(screen: pygame.Surface, mixer: Mixer):
    pygame.display.set_caption('MacGyver Maze - Win')

    mixer.set_music('victory')

    banner = pygame.transform.scale(pygame.image.load(asset('victory_banner.png')), get_screen_size())

    running = loop_menu(screen, banner, mixer)

    mixer.set_music('main')

    return running


def defeat_screen(screen: pygame.Surface, mixer: Mixer):
    pygame.display.set_caption('MacGyver Maze - Defeat')

    mixer.set_music('defeat')

    banner = pygame.transform.scale(pygame.image.load(asset('defeat_banner.png')), get_screen_size())

    running = loop_menu(screen, banner, mixer)

    mixer.set_music('main')

    return running


def loop_menu(screen: pygame.Surface, banner, mixer):
    """Handle events of the application."""
    running = True

    back_button = pygame.image.load(asset('back_button.png'))
    back_button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)
    back_rect = back_button.get_rect()

    back_rect.topleft = ((get_screen_width() / 2 - (back_rect.width / 2)), get_screen_height() * 0.8)

    # Initialize click at False
    click = False

    while running:
        screen.blit(banner, (0, 0))
        screen.blit(back_button, back_rect.topleft)

        # X and Y coordinates of the user mouse cursor.
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if back_rect.collidepoint((mouse_x, mouse_y)):
            hovered(screen, back_button, back_rect)
            if click:
                running = False

        # Reset the click state at each frame.
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                exit_app()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_F1:
                    mixer.toggle()

            # If the user click somewhere.
            if event.type == MOUSEBUTTONDOWN:
                click = True

        pygame.display.update()

    return running
