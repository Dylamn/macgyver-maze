import pygame.sprite as sprite
import pygame.image

from src.utils import asset


class Macgyver(sprite.Sprite):
    """This class represents MacGyver."""

    # Will receive the sprite groups
    containers = None

    # The filename of the MacGyver image.
    MAC_GYVER = "MacGyver.png"

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

        super().__init__(self.containers)

        self.image = pygame.image.load(asset(self.MAC_GYVER))

        self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()  # Represent the hitbox and the position of MacGyver.

        # Place MacGyver on the starting point.
        self.rect.topleft = tuple(point * scaling for point, scaling in zip(start, scale))

        # Scale the moves directions of MacGyver.
        self._set_scale_moves(scale)
        self._old_coordinates = (0, 0)

    @property
    def coordinates(self):
        """Get MacGyver's coordinates."""
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, value):
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

    def _set_scale_moves(self, scale: tuple):
        """Updates MacGyver's Motion Scale to match the screen scale."""
        x_scale = scale[0]
        y_scale = scale[1]

        self.UP = (0, -y_scale)
        self.DOWN = (0, y_scale)
        self.LEFT = (-x_scale, 0)
        self.RIGHT = (x_scale, 0)
