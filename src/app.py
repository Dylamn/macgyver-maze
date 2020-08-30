import sys
import pygame
from src.game import Game

from pygame.locals import *
from src.utils import *

BLACK = (0, 0, 0)


class App:
    """Represent the entire application."""

    # The name of the application.
    NAME = "MacGyver Maze"

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

        pygame.display.set_caption(self.NAME)

        # Load the image in a temp variable, then assign it to the attribute (omit long one liner)
        main_background = pygame.image.load(asset("background_menu.jpg"))
        self.main_background = pygame.transform.scale(main_background, self.screen_size)

    def execute(self):
        # Load buttons images.
        play_button = pygame.image.load(asset('play_button.png'))
        options_button = pygame.image.load(asset('options_button.png'))
        quit_button = pygame.image.load(asset('quit_button.png'))

        # Get the rect of each buttons
        play_button_rect, options_button_rect = play_button.get_rect(), options_button.get_rect()
        quit_button_rect = quit_button.get_rect()

        # Set the x, y coordinates of the buttons rect.
        play_button_rect.topleft = (40, 320)
        options_button_rect.topleft = (40, (play_button_rect.y + play_button_rect.height + 10))
        quit_button_rect.topleft = (40, options_button_rect.y + (options_button_rect.height + 10))

        while True:
            self.screen.fill(BLACK)
            self.screen.blit(self.main_background, (0, 0))

            # Display buttons to the screen
            self.screen.blit(play_button, play_button_rect.topleft)
            self.screen.blit(options_button, options_button_rect.topleft)
            self.screen.blit(quit_button, quit_button_rect.topleft)

            # X and Y coordinates of the user mouse cursor.
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if play_button_rect.collidepoint((mouse_x, mouse_y)):
                if self.click:
                    # Initialize the game.
                    game = Game(self.screen, self.scale)

                    # Then execute the game loop.
                    game.execute()

            if options_button_rect.collidepoint((mouse_x, mouse_y)):
                if self.click:
                    print("options button")

            if quit_button_rect.collidepoint((mouse_x, mouse_y)):
                if self.click:
                    pygame.quit()
                    sys.exit()

            # Reset the click attribute to false for each frame.
            self.click = False

            # Wait for an event
            event = pygame.event.wait()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # If the user click somewhere.
            if event.type == MOUSEBUTTONDOWN:
                self.click = True

            # Update the display
            pygame.display.update()
