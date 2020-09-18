import pygame.font

from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, QUIT, \
    BLEND_RGBA_MULT

from src.mixer import Mixer
from src.utils import asset, hovered, exit_app, \
    get_screen_size, get_screen_width, get_screen_height

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MARGIN = 40
LINE_SPACING = get_screen_height() / 8


def help_menu(screen: pygame.Surface, mixer: Mixer):
    running = True

    # Create the background of the menu (transparent black)
    background = pygame.Surface((get_screen_width(), get_screen_height()))
    background.set_alpha(240)
    background.fill(BLACK)
    screen.blit(background, (0, 0))

    pygame.display.set_caption('MacGyver Maze - Options')

    font = pygame.font.SysFont(None, 50)

    back_button = pygame.image.load(asset('buttons/back.png'))
    back_button.fill((255, 255, 255, 192), None, BLEND_RGBA_MULT)
    back_button_rect = back_button.get_rect()
    back_button_rect.topleft = (
        get_screen_width() / 2 - (back_button_rect.width / 2),
        get_screen_height() - back_button_rect.height - MARGIN
    )

    # Y offset for lines
    offset_line1 = LINE_SPACING
    offset_line2 = offset_line1 + LINE_SPACING
    offset_line3 = offset_line2 + LINE_SPACING
    offset_line4 = offset_line3 + LINE_SPACING

    # Initialize each key image and associate coordinates for each image.
    # Line 1 - Start with arrow keys.
    # These will be displayed with the same layout as on a standard keyboard.
    key_left = pygame.image.load(asset('keys/key_left.png'))
    key_left_rect = key_left.get_rect()
    key_left_rect.topleft = (MARGIN, offset_line1)

    key_down = pygame.image.load(asset('keys/key_down.png'))
    key_down_rect = key_down.get_rect()
    key_down_rect.topleft = (key_left_rect.right, offset_line1)

    key_up = pygame.image.load(asset('keys/key_up.png'))
    key_up_rect = key_up.get_rect()
    key_up_rect.topleft = (
        key_down_rect.left,
        (offset_line1 - key_down_rect.height)
    )

    key_right = pygame.image.load(asset('keys/key_right.png'))
    key_right_rect = key_right.get_rect()
    key_right_rect.topleft = (key_down_rect.right, offset_line1)

    # Line 2 - C key
    key_c = pygame.image.load(asset('keys/key_c.png'))
    key_c_rect = key_c.get_rect()
    key_c_rect.topleft = (MARGIN, offset_line2)

    # Line 3 - F1 key
    key_f1 = pygame.image.load(asset('keys/key_f1.png'))
    key_f1_rect = key_f1.get_rect()
    key_f1_rect.topleft = (MARGIN, offset_line3)

    # Line 4 - numeric keys - & +
    key_minus = pygame.image.load(asset('keys/key_n_minus.png'))
    key_minus_rect = key_minus.get_rect()
    key_minus_rect.topleft = (MARGIN, offset_line4)

    key_plus = pygame.image.load(asset('keys/key_n_plus.png'))
    key_plus_rect = key_plus.get_rect()
    key_plus_rect.topleft = (key_minus_rect.right, offset_line4)

    # Now, create a caption for each key
    # Arrow keys caption
    arrow_keys_caption = font.render("Move MacGyver", True, WHITE)
    arrow_keys_caption_rect = arrow_keys_caption.get_rect()
    arrow_keys_caption_rect.topleft = (key_right_rect.right + MARGIN, offset_line1),

    # Get the X axis of the first caption,
    # we'll align every captions based on this one.
    offset_caption_x = arrow_keys_caption_rect.left

    # C key caption
    key_c_caption = font.render("Craft the syringe", True, WHITE)
    key_c_caption_rect = key_c_caption.get_rect()
    key_c_caption_rect.topleft = (offset_caption_x, offset_line2)

    # F1 key caption
    f1_key_caption = font.render("Mute/unmute the volume", True, WHITE)
    f1_key_caption_rect = f1_key_caption.get_rect()
    f1_key_caption_rect.topleft = (offset_caption_x, offset_line3)

    # -/+ key caption
    volume_key_caption = font.render("Increase/decrease volume", True, WHITE)
    volume_key_caption_rect = volume_key_caption.get_rect()
    volume_key_caption_rect.topleft = (offset_caption_x, offset_line4)

    # Initialize click variable which
    # will determines if the user click or not.
    click = False

    while running:
        # Blit each images to the screen.
        screen.blits([
            # Back button
            (back_button, back_button_rect.topleft),

            # Arrow key images
            (key_up, key_up_rect.topleft),
            (key_left, key_left_rect.topleft),
            (key_down, key_down_rect.topleft),
            (key_right, key_right_rect.topleft),

            # other keys (C, F1, etc...)
            (key_c, key_c_rect.topleft), (key_f1, key_f1_rect.topleft),
            (key_minus, key_minus_rect), (key_plus, key_plus_rect),

            # captions
            (arrow_keys_caption, arrow_keys_caption_rect.topleft),
            (key_c_caption, key_c_caption_rect.topleft),
            (f1_key_caption, f1_key_caption_rect),
            (volume_key_caption, volume_key_caption_rect),
        ])

        # X and Y coordinates of the user mouse cursor.
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if back_button_rect.collidepoint((mouse_x, mouse_y)):
            # Make the button more opaque when we're hovering it.
            hovered(screen, back_button, back_button_rect)

            if click:
                # We'll leave the menu
                running = False

        if running:
            click, running, _ = handle_keys_event(mixer)

        pygame.display.update()

    return


def victory_screen(screen: pygame.Surface, mixer: Mixer):
    """Draw the victory screen."""
    pygame.display.set_caption('MacGyver Maze - Win')

    mixer.set_music('victory')

    banner = pygame.transform.scale(
        pygame.image.load(asset('victory_banner.png')),
        get_screen_size()
    )

    next_action = loop_menu(screen, banner, 'victory', mixer)

    if next_action != 'quit':
        mixer.set_music('main')

    return next_action


def defeat_screen(screen: pygame.Surface, mixer: Mixer):
    """Draw the defeat screen."""
    pygame.display.set_caption('MacGyver Maze - Defeat')

    mixer.set_music('defeat')

    banner = pygame.transform.scale(
        pygame.image.load(asset('defeat_banner.png')),
        get_screen_size()
    )

    next_action = loop_menu(screen, banner, 'defeat', mixer)

    if next_action != 'quit':
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
    back_button = pygame.transform.scale(
        original_back_button,
        (int(get_screen_width() / 4), original_back_button.get_height())
    )
    exit_button = pygame.transform.scale(
        original_exit_button,
        (int(get_screen_width() / 4), original_exit_button.get_height())
    )

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
        retry_button = pygame.transform.scale(
            original_retry_button, (int(get_screen_width() / 4), 70)
        )
        retry_button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)
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

        if running:
            click, running, next_action = handle_keys_event(mixer, next_action)

        if mixer.notification.is_active:
            mixer.notification.render(screen)

        pygame.display.update()

    return next_action


def handle_keys_event(mixer, next_action=None):
    # Reset the click variable to false for each frame.
    running = True
    click = False

    for event in pygame.event.get():
        if event.type == QUIT:
            exit_app()

        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()

            mixer.keys_interaction(keys)

            if keys[K_ESCAPE]:
                running = False
                next_action = 'back'

        # If the user click somewhere.
        if event.type == MOUSEBUTTONDOWN:
            click = True

    return click, running, next_action
