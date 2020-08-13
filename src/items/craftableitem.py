import pygame
import pygame.sprite as sprite
from src.interfaces import ICraftableItem
from src.utils import scale_position, asset


class CraftableItem(sprite.Sprite, ICraftableItem):
    """Base concrete class for items that can be crafted."""
    _image_file = None

    # The list of items needed for the craft of this item.
    items_required = []

    @property
    def item_file(self) -> str:
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

    def craft(self, inventory: sprite.Group) -> bool:
        if self.can_be_crafted(inventory):
            comsume = []
            for item in inventory:
                if item in self.items_required:
                    return True
        else:
            return False

    @classmethod
    def can_be_crafted(cls, inventory: sprite.Group) -> bool:
        if cls.missing_items(inventory):
            print('not craftable')
            return False
        else:
            print('craftable')
            return True

    @classmethod
    def missing_items(cls, inventory: sprite.Group) -> list:
        missings = cls.items_required.copy()

        for collected in inventory:
            for item in missings:
                if isinstance(collected, item):
                    missings.remove(item)

        print(f'What\'s missing : {missings}')
        return missings
