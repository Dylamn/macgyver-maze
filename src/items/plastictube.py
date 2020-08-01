import pygame.sprite as sprite
import pygame.image
from .interfaces import CollectableItemInterface
from ..utils import asset, scale_position


class PlasticTube(sprite.Sprite, CollectableItemInterface):
    # The filename of the PlasticTube image.
    PLASTIC_TUBE = "tube_plastique.png"

    @property
    def item_file(self) -> str:
        return self.PLASTIC_TUBE

    # Will contains the sprite groups.
    containers = None

    def __init__(self, pos: tuple, scale: tuple, *containers: sprite.Group):
        """PlasticTube default constructor.

        :param pos A given position where the item will be placed.
        """

        # Override default containers if provided.
        if containers:
            self.containers = containers

        # Call the parent constructor.
        super().__init__(self.containers)

        # The original graphic representation of the PlasticTube.
        self.original_img = pygame.image.load(asset(self.item_file))

        # Scaled graphic representation of the PlasticTube.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Represent the hitbox and the position of the PlasticTube.
        self.rect = self.image.get_rect()

        # Place the item at the given coordinates.
        self.rect.topleft = scale_position(pos, scale)

    def collect(self, inventory: list) -> bool:
        pass
