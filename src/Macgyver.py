import pygame.sprite as sprite
import pygame.image

from src.utils import asset


class Macgyver(sprite.Sprite):
    """This class represents MacGyver."""

    # The filename of the MacGyver image.
    MAC_GYVER = "MacGyver.png"

    # Directional values. Each tile of the labyrinth is about 20px.
    # MacGyver will therefore make steps of 20px.
    UP = (0, -20)
    RIGHT = (20, 0)
    DOWN = (0, 20)
    LEFT = (-20, 0)

    def __init__(self):
        """MacGyver default constructor."""
        super().__init__()

        self.image = pygame.image.load(asset(self.MAC_GYVER))
        self.rect = self.image.get_rect()  # Represent the hitbox and the position of MacGyver.

    def move_up(self):
        """Move MacGyver to the top."""
        self.rect = self.rect.move(self.UP)

    def move_right(self):
        """Move MacGyver to the right."""
        self.rect = self.rect.move(self.RIGHT)

    def move_down(self):
        """Move MacGyver to the bottom."""
        self.rect = self.rect.move(self.DOWN)

    def move_left(self):
        """Move MacGyver to the left."""
        self.rect = self.rect.move(self.LEFT)
