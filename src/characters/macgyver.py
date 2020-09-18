import pygame.sprite as sprite
import pygame.image

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

from src.utils import asset, scale_position


class Macgyver(sprite.Sprite):
    """This class represents MacGyver."""

    # Will receive the sprite groups
    containers = None

    # The filename of the MacGyver image.
    MAC_GYVER = "macGyver.png"

    # Directional values. Each tile of the labyrinth is about 20px.
    # MacGyver will therefore make steps of 20px.
    UP = (0, -20)
    RIGHT = (20, 0)
    DOWN = (0, 20)
    LEFT = (-20, 0)

    def __init__(self, start: tuple, scale: tuple, *containers: sprite.Group):
        """MacGyver default constructor."""

        # Override default containers
        if containers:
            self.containers = containers

        # Call the parent constructor.
        super().__init__(self.containers)

        # The original graphic representation of MacGyver.
        self.original_img = pygame.image.load(asset(self.MAC_GYVER))

        # Scaled graphic representation of MacGyver.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Represent the hitbox and the position of MacGyver.
        self.rect = self.image.get_rect()

        # Place MacGyver on the starting point.
        self.rect.topleft = scale_position(start, scale)

        # Scale the moves directions of MacGyver.
        self._set_scale_moves(scale)
        self._old_coordinates = (0, 0)

        # Represent the inventory of MacGyver where the items will be stored.
        # This inventory must be filled with the three needed items in order
        # to put the guardian in sleep.
        self.inventory = sprite.Group()

    @property
    def coordinates(self):
        """Get MacGyver's coordinates."""
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, value):
        """Set MacGyver's new coordinates."""
        self.rect.topleft = value

    def rollback(self):
        """Move MacGyver one move before."""
        self.coordinates = self._old_coordinates

    def move_up(self):
        """Move MacGyver to the top."""
        self._old_coordinates = self.rect.topleft
        self.rect = self.rect.move(self.UP)

    def move_right(self):
        """Move MacGyver to the right."""
        self._old_coordinates = self.rect.topleft
        self.rect = self.rect.move(self.RIGHT)

    def move_down(self):
        """Move MacGyver to the bottom."""
        self._old_coordinates = self.rect.topleft
        self.rect = self.rect.move(self.DOWN)

    def move_left(self):
        """Move MacGyver to the left."""
        self._old_coordinates = self.rect.topleft
        self.rect = self.rect.move(self.LEFT)

    def handle_keys(self, keys, key_unicode=None):
        """Handle keys which interacts with MacGyver."""

        # The game handle movements with standard directional keys (w, a, s, d for qwerty and z, q, s, d for azerty)
        if keys[K_UP] or key_unicode in ['w', 'z']:
            self.move_up()

        elif keys[K_RIGHT] or key_unicode == 'd':
            self.move_right()

        elif keys[K_DOWN] or key_unicode == 's':
            self.move_down()

        elif keys[K_LEFT] or key_unicode in ['a', 'q']:
            self.move_left()

    def _set_scale_moves(self, scale: tuple):
        """Updates MacGyver's Motion Scale to match the screen scale."""

        # width is the x axis, height the y axis.
        width, height = scale

        # Set the scale step of each directions.
        self.UP = (0, -height)
        self.DOWN = (0, height)
        self.LEFT = (-width, 0)
        self.RIGHT = (width, 0)
