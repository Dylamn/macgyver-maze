import pygame
from pygame.locals import *

from src.utils import *
from src.Maze import Maze
from src.wall import Wall
from src.floor import Floor
from src.Macgyver import Macgyver

# Game constants
MAZE_PATTERN_FILE = 'maze.txt'
CAPTION = 'MacGyver Maze'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class App:
    # Scale must be dynamic if resizable is available.
    # A specific event handler will manage that.
    scale = None

    # Screen attributes
    screen = None
    screen_size = None

    _running = False  # Determine whether the game is running or not.

    def __init__(self, size=(720, 720)):
        """Initialize the game/application."""
        self.screen_size = size
        self.scale = tuple(round(num / 15) for num in size)

        # Initialize Game Groups
        self.characters = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.sprites = pygame.sprite.RenderUpdates()

        # Assign default groups to each Sprite class.
        Macgyver.containers = self.sprites
        Wall.containers = self.sprites, self.walls
        Floor.containers = self.sprites, self.floors

        # Inject dependencies.
        self.maze = Maze(self.scale, self.walls, self.floors, file_pattern=MAZE_PATTERN_FILE)
        self.macgyver = Macgyver(self.maze.start, self.scale)

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
        """Perform checks, such as checking for colliding sprites."""
        if pygame.sprite.spritecollide(self.macgyver, self.walls, 0):
            self.macgyver.rollback()

    def render(self):
        """Make the render of the game."""
        self.screen.fill(BLACK)
        dirty = self.sprites.draw(self.screen)

        # Only update sprites, not the whole screen.
        pygame.display.update(dirty)

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def execute(self):
        """Execute the game."""

        while self._running:
            pygame.event.pump()
            event = pygame.event.wait()

            # Send events to the handler.
            self.on_event(event)

            self.on_loop()

            self.render()

        self.on_cleanup()


def main():
    """Bootstrap the game."""

    # Default size of the screen as a tuple.
    window_size = get_screen_size()

    # Initialize the game.
    app = App(size=window_size)

    # Then execute the game loop.
    app.execute()


if __name__ == '__main__':
    main()
