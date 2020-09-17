from src.UI.menus import help_menu
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
    mouse = False

    # The index of the object where the user is.
    # If set to None, this mean's that the user is using
    # his mouse to navigate throught the menus.
    key_nav = None

    # Determines if the user press an enter key or not.
    enter_key = False

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
        self.screen = pygame.display.set_mode(self.screen_size, depth=32)

        pygame.display.set_icon(self.ICON)
        pygame.display.set_caption(self.NAME)

        # Load the image in a temp variable, then assign it to the attribute (omit long one liner)
        main_background = pygame.image.load(asset("background_menu.jpg"))
        self.main_background = pygame.transform.scale(main_background, self.screen_size)

        # Bootstrap the notifications.
        self.notification = Notification(self.scale[0])

        # Audio
        self.mixer = Mixer(self.notification)

        # Init game as None
        self.game = None

    def execute(self):
        # Load buttons images.
        buttons = {
            "play": pygame.image.load(asset('buttons/play.png')),
            "help": pygame.image.load(asset('buttons/help.png')),
            "quit": pygame.image.load(asset('buttons/quit.png'))
        }

        # Add a bit of transparency to the buttons (we'll make them more opaque when hovering it).
        for button in buttons.values():
            button.fill((255, 255, 255, 192), None, pygame.BLEND_RGBA_MULT)

        # Get the rect of each buttons
        btns_rect = {button: buttons.get(button).get_rect() for button in buttons}

        # Set the x, y coordinates of the buttons rect.
        for i, rect in enumerate(list(btns_rect.values())):
            if i == 0:
                rect.topleft = (40, get_screen_height() - 450)
            else:
                precedent = list(btns_rect.values())[i - 1]
                rect.topleft = (40, (precedent.y + precedent.height + 10))

        # X and Y coordinates of the user mouse cursor at the precedent frame.
        precedent_x, precedent_y = None, None

        # This is the main menu.
        while True:
            self.screen.fill(BLACK)
            self.screen.blit(self.main_background, (0, 0))

            # Display buttons to the screen
            for button, rect in zip(buttons.values(), btns_rect.values()):
                self.screen.blit(button, rect.topleft)

            # X and Y coordinates of the user mouse cursor.
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # The button that the mouse is hovering.
            # When the user switch to key navigation, we'll focus the button where the mouse is hovering.
            mouse_hovering = None

            # If the mouse perform an action (move or click) then leave the keyboard navigation
            if self.mouse or mouse_x != precedent_x or mouse_y != precedent_y:
                self.key_nav = None

            # PLAY button
            if self.key_nav == 0 or (btns_rect.get('play').collidepoint((mouse_x, mouse_y)) and self.key_nav is None):
                if self.key_nav is None:
                    mouse_hovering = 0

                # Make the button more opaque when we're hovering it.
                hovered(self.screen, buttons['play'], btns_rect['play'])

                if self.mouse or (self.key_nav is not None and self.enter_key):
                    # Initialize the game.
                    if self.game is None:
                        self.game = Game(self.screen, self.mixer, self.notification, self.scale)

                    # Then execute the game loop.
                    remove_game = self.game.execute()

                    # remove_game determines if we cleanup the resources that the game instance use.
                    if remove_game:
                        self.game = None

                    # Reset the standard caption.
                    pygame.display.set_caption(self.NAME)

            # HELP button
            if self.key_nav == 1 or (btns_rect.get('help').collidepoint((mouse_x, mouse_y)) and self.key_nav is None):
                if self.key_nav is None:
                    mouse_hovering = 1

                hovered(self.screen, buttons['help'], btns_rect['help'])

                if self.mouse or self.enter_key:
                    help_menu(self.screen, self.mixer)
                    pygame.display.set_caption(self.NAME)

            # QUIT button
            if self.key_nav == 2 or (btns_rect.get('quit').collidepoint((mouse_x, mouse_y)) and self.key_nav is None):
                if self.key_nav is None:
                    mouse_hovering = 2

                hovered(self.screen, buttons['quit'], btns_rect['quit'])

                if self.mouse or self.enter_key:
                    exit_app()

            # Reset the click and enter_key attributes to false for each frame.
            self.mouse = False
            self.enter_key = False

            # Assign the current mouse position.
            # These values will determines if the mouse cursor has moved or not.
            precedent_x, precedent_y = mouse_x, mouse_y

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[K_DOWN]:
                        # Start key navigation
                        if self.key_nav is None:
                            if mouse_hovering is None:
                                self.key_nav = 0
                            else:
                                self.key_nav = mouse_hovering

                        # Stay on key navigation...
                        else:
                            self.key_nav = 0 if self.key_nav == 2 else self.key_nav + 1

                    if keys[K_UP]:
                        if self.key_nav is None:
                            if mouse_hovering is None:
                                self.key_nav = 0
                            else:
                                self.key_nav = mouse_hovering

                        else:
                            self.key_nav = 2 if self.key_nav == 0 else self.key_nav - 1

                    # If the user press the enter key
                    if keys[K_RETURN] or keys[K_KP_ENTER]:
                        self.enter_key = True

                    # Handle keys which interact with the audio
                    self.mixer.keys_interaction(keys)

                if event.type == QUIT:
                    exit_app()

                # If the user click somewhere.
                if event.type == MOUSEBUTTONDOWN:
                    self.mouse = True

            if self.notification.is_active:
                self.notification.render(self.screen)

            # Update the display
            pygame.display.update()
