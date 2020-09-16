import pygame.sprite as sprite
import pygame.transform

from src.utils import asset


class Floor(sprite.Sprite):

    # will receive the sprite groups.
    containers = None

    def __init__(self, x, y, scale):
        super().__init__(self.containers)

        # image property is reserved for the scaled image.
        self.original_img = pygame.image.load(asset('floor.png'))

        # Scaled image must be assigned to the image attribute.
        self.image = pygame.transform.scale(self.original_img, scale)

        # Unpack the scale values.
        self.width, self.height = scale

        # Retrieve the rect of the image.
        self.rect = self.image.get_rect()

        # Assign the coordinates of the floor.
        self.rect.topleft = (x * self.width, y * self.height)
