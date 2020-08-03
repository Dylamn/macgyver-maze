import pygame.sprite as sprite
from abc import ABCMeta, abstractmethod


class ICollectableItem(metaclass=ABCMeta):
    """This interface is used to define an item."""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'collect') and
                callable(subclass.collect) or
                NotImplemented)

    @property
    @abstractmethod
    def item_file(self) -> str:
        """The name of the file used for the visual representation of the item."""
        raise NotImplementedError

    @abstractmethod
    def collect(self, inventory: sprite.Group) -> None:
        """Collect an item and add it to the given inventory."""
        raise NotImplementedError


class ICraftableItem(metaclass=ABCMeta):
    """This interface is used to define an item that can be crafted."""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'items_required') and
                hasattr(subclass, 'can_be_crafted') and
                callable(subclass.can_be_crafted) and
                hasattr(subclass, 'craft') and
                callable(subclass.craft) and
                hasattr(subclass, 'missing_items') and
                callable(subclass.missing_items) or
                NotImplemented)

    @property
    @abstractmethod
    def item_file(self) -> str:
        """The name of the file used for the visual representation of the item."""
        raise NotImplementedError

    @property
    @abstractmethod
    def items_required(self) -> list:
        """The list of items needed for the craft of this item."""
        raise NotImplementedError

    @abstractmethod
    def can_be_crafted(self, inventory: sprite.Group) -> bool:
        """Determine whether the item can be crafted or not with the items in inventory."""
        raise NotImplementedError

    @abstractmethod
    def craft(self, inventory: sprite.Group) -> bool:
        """Craft the item and consume the items in inventory needed for the craft."""
        raise NotImplementedError

    def missing_items(self, inventory: sprite.Group) -> list:
        """Determine which items are missing for the craft."""
        raise NotImplementedError
