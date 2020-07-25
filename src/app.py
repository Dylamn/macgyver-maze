import pygame
from pygame.locals import *

from src.utils import *
from src.Maze import Maze
from src.Macgyver import Macgyver

# Game constants
MAZE_PATTERN_FILE = 'maze.txt'
CAPTION = 'MacGyver Maze'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class App:
    screen = None
    screen_size = None

    _running = False  # Determine whether the game is running or not.

    def __init__(self, size=(720, 480)):
        """Initialize the game/application."""
        self.screen_size = size

        # Inject dependencies.
        self.maze = Maze(MAZE_PATTERN_FILE)
        self.macgyver = Macgyver(self.maze.start)

        self._init()

    def _init(self):
        """Initialize pygame modules and required stuff like screen, game loop value..."""
        pygame.init()

        self.screen = pygame.display.set_mode(self.screen_size)

        pygame.display.set_caption(CAPTION)
        self._running = True

    def on_event(self, event):
        """Handle pygame events."""
        if event.type == QUIT:
            self._running = False

        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[K_UP]:
                self.macgyver.move_up()

            elif keys[K_RIGHT]:
                self.macgyver.move_right()

            elif keys[K_DOWN]:
                self.macgyver.move_down()

            elif keys[K_LEFT]:
                self.macgyver.move_left()

            elif keys[K_ESCAPE]:
                self._running = False

    def on_loop(self):
        """Make specific actions ?"""
        pass

    def render(self):
        """Render the grid once at the beginning."""
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)  # TODO: Give a grid instead of the screen and then blit the grid ?
        self.screen.blit(self.macgyver.image, self.macgyver.rect)
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def execute(self):
        """Execute the game."""

        while self._running:
            pygame.event.pump()
            event = pygame.event.wait()

            self.on_event(event)

            self.on_loop()

            self.render()

        self.on_cleanup()


if __name__ == '__main__':
    # Default size of the screen as a tuple.
    window_size = get_screen_size()

    # Initialize the game.
    app = App(size=window_size)

    # Then execute the game loop.
    app.execute()
