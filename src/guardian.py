import pygame.sprite as sprite
import pygame.rect as pyrect
import pygame.image
from operator import sub
from src.utils import asset, scale_position
from src.macgyver import Macgyver

from src.items.syringe import Syringe


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

        # Call the parent constructor.
        super().__init__(self.containers)

        # The original graphic representation of the Guardian.
        self.original_img = pygame.image.load(asset(self.GUARDIAN))

        # Scaled graphic representation of the Guardian.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Represent the hitbox and the position of the Guardian.
        self.rect = self.image.get_rect()

        # Place the Guardian on the ending point.
        self.rect.topleft = end

        # Find the adjacent Guardian tiles where MacGyver will lose
        # if he doesn't have the required items while on one of these squares.
        self.adjacent_tiles = self.find_adjacent_tiles(scale)

    @property
    def coordinates(self):
        """Get MacGyver's coordinates."""
        return self.rect.topleft

    @coordinates.setter
    def coordinates(self, value):
        self.rect.topleft = value

    def find_adjacent_tiles(self, scale):
        width, height = scale

        # Retrieve all adjacent tiles.
        adjacent_top = pyrect.Rect(tuple(map(sub, self.coordinates, (0, -height))), (width, height))
        adjacent_down = pyrect.Rect(tuple(map(sub, self.coordinates, (0, height))), (width, height))
        adjacent_left = pyrect.Rect(tuple(map(sub, self.coordinates, (-width, 0))), (width, height))
        adjacent_right = pyrect.Rect(tuple(map(sub, self.coordinates, (width, 0))), (width, height))

        return [adjacent_top, adjacent_right, adjacent_down, adjacent_left]

    def _sleep(self):
        """The guardian will sleep, we can erase him from the display."""
        self.kill()

    def is_beatable(self, macgyver: Macgyver):
        for item in macgyver.inventory:
            if isinstance(item, Syringe):
                # MacGyver has the syringe
                self._sleep()

                # Return True to indicate to the app to continue.
                return True

        else:
            # MacGyver didn't have the syringe...
            macgyver.kill()
            # Return False to indicate to the app to stop running.
            return False
