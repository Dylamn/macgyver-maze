import pygame
import pygame.sprite as sprite
from src.interfaces import ICraftableItem
from src.utils import scale_position, asset


class CraftableItem(sprite.Sprite, ICraftableItem):
    """Base concrete class for items that can be crafted."""
    _image_file = None

    @property
    def item_file(self) -> str:
        return self._image_file

    @property
    def items_required(self) -> list:
        return []

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

    def craft(self, inventory: sprite.Group) -> bool:
        if self.can_be_crafted(inventory):
            comsume = []
            for item in inventory:
                if item in self.items_required:
                    print("hi")
                    return True
        else:
            return False

    def can_be_crafted(self, inventory: sprite.Group) -> bool:
        if self.missing_items(inventory):
            return False
        else:
            return True

    def missing_items(self, inventory: sprite.Group) -> list:
        missings = []

        for item in self.items_required:
            if item not in inventory:  # TODO: Test inventory.has()
                missings.append(item)

        return missings
