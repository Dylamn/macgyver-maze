import pygame.sprite as sprite
import pygame.image
from .interfaces import CollectableItemInterface
from ..utils import asset, scale_position


class Ether(sprite.Sprite, CollectableItemInterface):
    # The filename of the Ether image.
    ETHER = "ether.png"

    @property
    def item_file(self):
        return self.ETHER

    # Will contains the sprite groups.
    containers = None

    def __init__(self, pos: tuple, scale: tuple, *containers: sprite.Group):
        """Ether default constructor.

        :param pos A given position where the item will be placed.
        """

        # Override default containers if provided.
        if containers:
            self.containers = containers

        # Call the parent constructor.
        super().__init__(self.containers)

        # The original graphic representation of the Ether.
        self.original_img = pygame.image.load(asset(self.item_file))

        # Scaled graphic representation of the Ether.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Represent the hitbox and the position of the Ether.
        self.rect = self.image.get_rect()

        # Place the item at the given coordinates.
        self.rect.topleft = scale_position(pos, scale)

    def collect(self, inventory: list) -> bool:
        pass
