import pygame.sprite as sprite
import pygame.image
from src.interfaces import ICollectableItem
from src.utils import asset, scale_position


class CollectableItem(sprite.Sprite, ICollectableItem):
    """Base concrete class for items that can be collected."""
    _image_file = None

    # Name of the item
    name = None

    @property
    def item_file(self):
        return self._image_file

    # Will contains the sprite groups.
    containers = None

    def __init__(self, pos: tuple, scale: tuple, *containers: sprite.Group):
        """Needle default constructor.

        :param pos A given position where the item will be placed.
        """

        # Override default containers if provided.
        if containers:
            self.containers = containers

        # Call the parent constructor.
        super().__init__(self.containers)

        # The original graphic representation of the Needle.
        self.original_img = pygame.image.load(asset(self.item_file))

        # Scaled graphic representation of the Needle.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Represent the hitbox and the position of the Needle.
        self.rect = self.image.get_rect()

        # Place the item at the given coordinates.
        self.rect.topleft = scale_position(pos, scale)

    def collect(self, inventory: sprite.Group) -> None:
        # Remove the sprite from sprites and items group
        self.kill()
        # Add the item in the macgyver inventory.
        inventory.add(self)

