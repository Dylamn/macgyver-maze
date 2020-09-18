import sys
import pygame

from pygame import sprite
from pygame.locals import KEYDOWN, K_ESCAPE, K_c, K_e, QUIT
from src.utils import scale_position, exit_app

from src.UI.menus import victory_screen, defeat_screen

# Structures
from src.maze.maze import Maze
from src.maze.wall import Wall
from src.maze.floor import Floor

# Characters
from src.characters.macgyver import Macgyver
from src.characters.guardian import Guardian

# Items
from src.items.craftableitem import CraftableItem
from src.items.syringe import Syringe
from src.items.collectableitem import CollectableItem
from src.items.plastictube import PlasticTube
from src.items.needle import Needle
from src.items.ether import Ether

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    """Class which manage the game."""

    # A list containing each item that will be placed inside the maze.
    item_kit = [Needle, PlasticTube, Ether]

    # The name of the maze pattern file.
    MAZE_PATTERN_FILE = 'maze.txt'

    # Screen attributes
    screen = None

    # Determine whether the game is running or not.
    __running = False

    def __init__(self, screen, mixer, notification, scale: tuple = (48, 48)):
        """Initialize the game."""

        screen.fill(BLACK)

        pygame.display.set_caption("MacGyver Maze - Game")

        # Store the application screen and scaling ratio.
        self.screen = screen
        self.scale = scale

        # Initialize Game Groups.
        self.guardian_group = pygame.sprite.GroupSingle()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.sprites = pygame.sprite.RenderUpdates()

        # Assign default groups to each Sprite class.
        Macgyver.containers = self.sprites
        Guardian.containers = self.sprites, self.guardian_group
        Wall.containers = self.sprites, self.walls
        Floor.containers = self.sprites, self.floors
        CollectableItem.containers = self.sprites, self.items
        CraftableItem.containers = self.sprites

        # Set maze dependency.
        self.maze = Maze(self.scale, file_pattern=self.MAZE_PATTERN_FILE)

        # Retrieve the finish point.
        self.finish_point = scale_position(self.maze.end, self.scale)

        # Init last dependencies.
        self.macgyver = Macgyver(self.maze.start, self.scale)
        self.guardian = Guardian(self.finish_point, self.scale)

        # Audio
        self.mixer = mixer

        # Notifications.
        self.notification = notification

        # Place items...
        self.place_items()

    def on_event(self, event):
        """Handle pygame events."""
        if event.type == QUIT:
            self.__running = False
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            key_unicode = event.unicode

            keys = pygame.key.get_pressed()

            # Handle audio related keys.
            self.mixer.keys_interaction(keys)

            if keys[K_ESCAPE]:
                # Go back to the main menu.
                self.__running = False

            if keys[K_c]:
                is_crafted = Syringe.craft(self.macgyver.inventory)

                if is_crafted:
                    self.notification.active('crafted').set_timer(2)
                else:
                    self.notification.active('missing-items').set_timer(2)

            if keys[K_e]:
                if self.notification.is_active:
                    self.notification.erase()

            self.macgyver.handle_keys(keys, key_unicode)

    def on_loop(self):
        """Perform checks, such as checking for colliding sprites."""

        if not Syringe.craftable:
            if Syringe.can_be_crafted(self.macgyver.inventory):
                Syringe.craftable = True
                self.notification.active('craft-available').set_timer(2)

        # Check if MacGyver threw himself against a wall...
        if sprite.spritecollide(self.macgyver, self.walls, False):
            self.macgyver.rollback()

        # Macgyver will collect the item and add it to it's inventory...
        for item in sprite.spritecollide(self.macgyver, self.items, False):
            item.collect(self.macgyver.inventory)

        # if self.macgyver.coordinates == self.finish_point:
        #     self.notification.active('win')

    def render(self):
        """Make the render of the game."""
        dirty = self.sprites.draw(self.screen)

        if self.notification.is_active:
            self.notification.render(self.screen)

            # Display the text.
            pygame.display.update()

        # Only update sprites, not the whole screen.
        pygame.display.update(dirty)

    def execute(self):
        """Execute the game loop."""

        # Set the value for the game loop to True.
        self.__running = True

        # Determines if the application delete the game instance or not.
        # When user loose and go back to the main menu, we can remove
        # the game resource.
        delete_on_leaving = False

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
                    self.mixer.play_sound('wilhelm_scream')

                    # Calculates whether MacGyver
                    # will die or put the guardian to sleep.
                    self.__running = self.guardian.is_beatable(self.macgyver)

                    if not self.macgyver.alive():
                        # MacGyver is dead, display the defeat screen.
                        next_action = defeat_screen(self.screen, self.mixer)

                        delete_on_leaving = \
                            self.handle_next_action(next_action)

            if self.macgyver.coordinates == self.finish_point:
                # MacGyver win, display the victory screen.
                next_action = victory_screen(self.screen, self.mixer)

                delete_on_leaving = self.handle_next_action(next_action)

        return delete_on_leaving

    def handle_next_action(self, next_action):
        """Handle the next action after a victory/defeat."""
        if next_action == 'retry':
            self.reset()

        elif next_action == 'quit':
            exit_app()

        elif next_action == 'back':
            self.__running = False
            return True

        return False

    def reset(self):
        """Reset the game."""
        self.__running = True

        # Remove all sprites.
        self.guardian_group.empty()
        self.walls.empty()
        self.floors.empty()
        self.items.empty()
        self.sprites.empty()

        # Delete the old maze and create a new one.
        del self.maze
        self.maze = Maze(self.scale, file_pattern=self.MAZE_PATTERN_FILE)

        # Retrieve the finish point.
        self.finish_point = scale_position(self.maze.end, self.scale)

        # Delete characters and initialize new ones.
        del self.macgyver
        del self.guardian

        self.macgyver = Macgyver(self.maze.start, self.scale)
        self.guardian = Guardian(self.finish_point, self.scale)

        # Place items randomly.
        self.place_items()

    def place_items(self):
        """Place each items, at random coordinates in the maze."""
        for item in self.item_kit:
            coords = self.maze.random_coordinates()
            item(coords, self.scale)
