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
                keys = pygame.key.get_pressed()

                if keys[K_ESCAPE]:
                    running = False

        pygame.display.update()


def victory_screen(screen: pygame.Surface, mixer: Mixer):
    pygame.display.set_caption('MacGyver Maze - Win')

    mixer.set_music('victory')

    banner = pygame.transform.scale(pygame.image.load(asset('victory_banner.png')), get_screen_size())

    next_action = loop_menu(screen, banner, 'victory', mixer)

    mixer.set_music('main')

    return next_action


def defeat_screen(screen: pygame.Surface,mixer: Mixer):
    pygame.display.set_caption('MacGyver Maze - Defeat')

    mixer.set_music('defeat')

    banner = pygame.transform.scale(pygame.image.load(asset('defeat_banner.png')), get_screen_size())

    next_action = loop_menu(screen, banner, 'defeat', mixer)

    if next_action[1] != 'quit':
        mixer.set_music('main')

    return next_action


def loop_menu(screen: pygame.Surface, banner: pygame.Surface, menu_type: str, mixer: Mixer):
    """Handle events of the victory/defeat menus."""
    running = True
    next_action = None

    back_button = pygame.image.load(asset('back_button.png'))
    back_button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)
    back_rect = back_button.get_rect()

    if menu_type == 'victory':
        pass
    elif menu_type == 'defeat':
        pass

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
                next_action = 'quit'

        # Reset the click state at each frame.
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                exit_app()

            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                mixer.keys_interaction(keys)

                if keys[K_ESCAPE]:
                    running = False

            # If the user click somewhere.
            if event.type == MOUSEBUTTONDOWN:
                click = True

        if mixer.notification.is_active:
            mixer.notification.render(screen)

        pygame.display.update()

    return next_action
