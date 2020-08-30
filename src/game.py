import sys
import pygame
from pygame.locals import *

from src.utils import *
from src.UI.notification import Notification

from src.maze import Maze
from src.wall import Wall
from src.floor import Floor
from src.macgyver import Macgyver
from src.guardian import Guardian

# Items
from src.items.craftableitem import CraftableItem
from src.items.syringe import Syringe
from src.items.collectableitem import CollectableItem
from src.items.plastictube import PlasticTube
from src.items.needle import Needle
from src.items.ether import Ether

# Game constants
MAZE_PATTERN_FILE = 'maze.txt'
CAPTION = 'MacGyver Maze'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    # A list containing each item that will be placed inside the maze.
    item_kit = [Needle, PlasticTube, Ether]

    # Screen attributes
    screen = None

    # Determine whether the game is running or not.
    __running = False

    # No action can be performed when set to true.
    # This value is used when the player win.
    __lock = False

    def __init__(self, screen: pygame.Surface, scale: tuple = (48, 48)):
        """Initialize the game."""
        screen.fill(BLACK)

        # Store the application screen and scaling ratio.
        self.screen = screen
        self.scale = scale

        # Initialize Game Groups.
        self.characters = pygame.sprite.GroupSingle()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.sprites = pygame.sprite.RenderUpdates()

        # Assign default groups to each Sprite class.
        Macgyver.containers = self.sprites
        Guardian.containers = self.sprites, self.characters
        Wall.containers = self.sprites, self.walls
        Floor.containers = self.sprites, self.floors
        CollectableItem.containers = self.sprites, self.items
        CraftableItem.containers = self.sprites

        # Set maze dependency.
        self.maze = Maze(self.scale, file_pattern=MAZE_PATTERN_FILE)

        # Retrieve the finish point.
        self.finish_point = scale_position(self.maze.end, self.scale)

        # Init last dependencies.
        self.macgyver = Macgyver(self.maze.start, self.scale)
        self.guardian = Guardian(self.finish_point, self.scale)

        # Place items...
        for item in self.item_kit:
            coords = self.maze.random_coordinates()
            item(coords, self.scale)

        self._init()

    def _init(self):
        """Initialize pygame modules and required stuff like screen, game loop value..."""

        pygame.display.set_caption(CAPTION)
        self.notification = Notification(self.scale[0])

        self.__running = True

    def on_event(self, event):
        """Handle pygame events."""
        if event.type == QUIT:
            self.__running = False
            pygame.quit()
            sys.exit()

        if self.__lock:
            return

        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[K_c]:
                is_crafted = Syringe.craft(self.macgyver.inventory)

                if is_crafted:
                    self.notification.active('crafted').set_timer(3)
                else:
                    self.notification.active('missing-items').set_timer(3)

            if keys[K_e]:
                if self.notification.is_active:
                    self.notification.erase()

            if keys[K_UP]:
                self.macgyver.move_up()

            elif keys[K_RIGHT]:
                self.macgyver.move_right()

            elif keys[K_DOWN]:
                self.macgyver.move_down()

            elif keys[K_LEFT]:
                self.macgyver.move_left()

            elif keys[K_ESCAPE]:
                self.__running = False

    def on_loop(self):
        """Perform checks, such as checking for colliding sprites."""

        if Syringe.can_be_crafted(self.macgyver.inventory):
            self.notification.active('craft-available')

        # Check if MacGyver threw himself against a wall...
        if pygame.sprite.spritecollide(self.macgyver, self.walls, False):
            self.macgyver.rollback()

        # Macgyver will collect the item and add it to it's inventory...
        for item in pygame.sprite.spritecollide(self.macgyver, self.items, False):
            item.collect(self.macgyver.inventory)

        if self.macgyver.coordinates == self.finish_point:
            self.notification.active('win')

    def render(self):
        """Make the render of the game."""
        dirty = self.sprites.draw(self.screen)

        # Only update sprites, not the whole screen.
        pygame.display.update(dirty)

        if self.notification.is_active:
            self.notification.render(self.screen)

            # Display the text.
            pygame.display.update()

    def on_cleanup(self):
        # pygame.quit()
        pass

    def execute(self):
        """Execute the game loop."""

        while self.__running:
            pygame.event.pump()
            event = pygame.event.wait()

            # Send events to the handler.
            self.on_event(event)

            # Perform checks about walls and items.
            self.on_loop()

            # Render graphics.
            self.render()

            if self.guardian.alive():
                # MacGyver's in front of the guardian.
                if self.macgyver.rect in self.guardian.adjacent_tiles:
                    # Calculates whether MacGyver will die or put the guardian to sleep.
                    self.__running = self.guardian.is_beatable(self.macgyver)

                    if self.macgyver.coordinates == self.maze.end:
                        self.__lock = True

        self.on_cleanup()
