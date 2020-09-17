import pygame.sprite as sprite
from abc import ABCMeta, abstractmethod


class ICollectableItem(metaclass=ABCMeta):
    """This interface is used to define an item."""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'collect') and
                callable(subclass.collect) or
                NotImplemented)

    # The name of the item.
    name = None

    # Image that represents the object.
    _image_file = None

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

    # The name of the item.
    name = None

    # Image that represents the object.
    _image_file = None

    # Determines if the item can be crafted
    craftable = False

    # The list of items needed for the craft of this item.
    items_required = []

    @classmethod
    @abstractmethod
    def can_be_crafted(cls, inventory: sprite.Group) -> bool:
        """Determine whether the item can be crafted or not with the items in inventory."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def craft(cls, inventory: sprite.Group) -> bool:
        """Craft the item and consume the items in inventory needed for the craft."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def missing_items(cls, inventory: sprite.Group) -> list:
        """Determine which items are missing for the craft."""
        raise NotImplementedError
