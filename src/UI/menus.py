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

    return


def victory_screen(screen: pygame.Surface, mixer: Mixer):
    """Draw the victory screen."""
    pygame.display.set_caption('MacGyver Maze - Win')

    mixer.set_music('victory')

    banner = pygame.transform.scale(pygame.image.load(asset('victory_banner.png')), get_screen_size())

    next_action = loop_menu(screen, banner, 'victory', mixer)

    mixer.set_music('main')

    return next_action


def defeat_screen(screen: pygame.Surface, mixer: Mixer):
    """Draw the defeat screen."""
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

    # near to the bottom of the screen.
    offset_buttons_y = get_screen_height() * 0.80
    buttons_margin = 20

    # Initialize buttons
    original_back_button = pygame.image.load(asset('buttons/back.png'))
    original_exit_button = pygame.image.load(asset('buttons/exit_game.png'))

    # Scale size of buttons
    back_button = pygame.transform.scale(original_back_button, (int(get_screen_width() / 4), 70))
    exit_button = pygame.transform.scale(original_exit_button, (int(get_screen_width() / 4), 70))

    # Initialize retry button variables
    retry_button = None
    retry_rect = None

    exit_button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)
    back_button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)

    back_rect = back_button.get_rect()
    exit_rect = exit_button.get_rect()

    if menu_type == 'defeat':
        # We'll display the retry button only when the user doesn't win.
        original_retry_button = pygame.image.load(asset('buttons/retry.png'))
        retry_button = pygame.transform.scale(original_retry_button, (int(get_screen_width() / 4), 70))
        retry_button.fill((255, 255, 255, 120), None, pygame.BLEND_RGBA_MULT)
        retry_rect = retry_button.get_rect()
        retry_rect.topleft = (
            get_screen_width() / 2 - (retry_rect.width / 2),
            offset_buttons_y
        )

    back_rect.topleft = (buttons_margin, offset_buttons_y)

    exit_rect.topleft = (
        get_screen_width() - exit_rect.width - buttons_margin,
        offset_buttons_y
    )

    # Initialize click at False
    click = False

    while running:
        # X and Y coordinates of the user mouse cursor.
        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.blit(banner, (0, 0))
        screen.blit(back_button, back_rect.topleft)
        screen.blit(exit_button, exit_rect.topleft)

        # Draw the retry button
        if retry_rect is not None:
            screen.blit(retry_button, retry_rect.topleft)

            if retry_rect.collidepoint((mouse_x, mouse_y)):
                hovered(screen, retry_button, retry_rect)
                if click:
                    running = False
                    next_action = 'retry'

        if back_rect.collidepoint((mouse_x, mouse_y)):
            hovered(screen, back_button, back_rect)
            if click:
                running = False
                next_action = 'back'

        if exit_rect.collidepoint((mouse_x, mouse_y)):
            hovered(screen, exit_button, exit_rect)
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
