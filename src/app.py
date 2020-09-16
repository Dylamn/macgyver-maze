from src.UI.menus import *
from src.UI.notification import Notification

from pygame.locals import *

from src.game import Game
from src.mixer import Mixer
from src.utils import *

BLACK = (0, 0, 0)


class App:
    """Represent the entire application."""

    # The name of the application.
    NAME = "MacGyver Maze"

    # The icon of the application.
    ICON = pygame.image.load(asset('tile-crusader-logo.png'))

    # Determines if the user click or not.
    click = False

    # Scale must be dynamic if resizable is available.
    # A specific event handler will manage that.
    scale = None

    # Screen attributes
    screen = None
    screen_size = None

    def __init__(self, size: tuple = (720, 720)):
        """Bootstrap the application."""

        self.scale = calculate_scale(size)

        self.screen_size = size
        self.screen = pygame.display.set_mode(self.screen_size, 0, depth=32)

        pygame.display.set_icon(self.ICON)
        pygame.display.set_caption(self.NAME)

        # Load the image in a temp variable, then assign it to the attribute (omit long one liner)
        main_background = pygame.image.load(asset("background_menu.jpg"))
        self.main_background = pygame.transform.scale(main_background, self.screen_size)

        # Bootstrap the notifications.
        self.notification = Notification(self.scale[0])

        # Audio
        self.mixer = Mixer(self.notification)

    def execute(self):
        # Load buttons images.
        buttons = {
            "play": pygame.image.load(asset('play_button.png')),
            "options": pygame.image.load(asset('options_button.png')),
            "quit": pygame.image.load(asset('quit_button.png'))
        }

        # Add a bit of transparency to the buttons (we'll make them more opaque when hovering it).
        for button in buttons.values():
            button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)

        # Get the rect of each buttons
        buttons_rect = {button: buttons.get(button).get_rect() for button in buttons}

        # Set the x, y coordinates of the buttons rect.
        for i, rect in enumerate(list(buttons_rect.values())):
            if i == 0:
                rect.topleft = (40, get_screen_height() - 450)
            else:
                precedent = list(buttons_rect.values())[i - 1]
                rect.topleft = (40, (precedent.y + precedent.height + 10))

        # This is the main menu.
        while True:
            self.screen.fill(BLACK)
            self.screen.blit(self.main_background, (0, 0))

            # Display buttons to the screen
            for button, rect in zip(buttons.values(), buttons_rect.values()):
                self.screen.blit(button, rect.topleft)

            # X and Y coordinates of the user mouse cursor.
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if buttons_rect.get('play').collidepoint((mouse_x, mouse_y)):
                # Make the button more opaque when we're hovering it.
                hovered(self.screen, buttons['play'], buttons_rect['play'])

                if self.click:
                    # Initialize the game.
                    game = Game(self.screen, self.mixer, self.notification, self.scale)

                    # Then execute the game loop.
                    game.execute()

                    # Remove resources.
                    del game

            if buttons_rect.get('options').collidepoint((mouse_x, mouse_y)):
                hovered(self.screen, buttons['options'], buttons_rect['options'])

                if self.click:
                    options_menu(self.screen)

            if buttons_rect.get('quit').collidepoint((mouse_x, mouse_y)):
                hovered(self.screen, buttons['quit'], buttons_rect['quit'])

                if self.click:
                    exit_app()

            # Reset the click attribute to false for each frame.
            self.click = False

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()

                    # Handle keys which interact with the audio
                    self.mixer.keys_interaction(keys)

                if event.type == QUIT:
                    exit_app()

                # If the user click somewhere.
                if event.type == MOUSEBUTTONDOWN:
                    self.click = True

            if self.notification.is_active:
                self.notification.render(self.screen)

            # Update the display
            pygame.display.update()
