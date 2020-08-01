import pygame.sprite as sprite
import pygame.image
from .interfaces import CraftableItemInterface


class Syringe(sprite.Sprite, CraftableItemInterface):

    _items_required: list = []

    @property
    def items_required(self) -> list:
        return self._items_required

    def can_craft(self, inventory: list) -> bool:
        pass

    def craft(self, inventory: list) -> bool:
        pass

    def missing_items(self, inventory: list) -> list:
        pass
