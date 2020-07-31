import pygame.sprite as sprite
import pygame.image

from src.utils import asset


class Guardian(sprite.Sprite):
    """This class represents the Guardian."""

    # Will receive the sprite groups.
    containers = None

    # The filename of the Guardian image.
    GUARDIAN = "Gardien.png"

    def __init__(self, end: tuple, scale: tuple, *containers: sprite.Group):
        """Guardian default constructor."""

        # Override default containers if provided.
        if containers:
            self.containers = containers

        super().__init__(self.containers)

        self.image = pygame.image.load(asset(self.GUARDIAN))

        self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()  # Represent the hitbox and the position of the Guardian.

        # Place the Guardian on the ending point.
        self.rect.topleft = tuple(point * scaling for point, scaling in zip(end, scale))

    @property
    def coordinates(self):
        """Get MacGyver's coordinates."""
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, value):
        self.rect.topleft = value
