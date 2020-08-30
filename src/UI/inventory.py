import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


class InventoryUI:
    def __init__(self, scale: tuple, inv_color=BLACK):
        self.topleft, self.bottomright = (120, 120), (480, 480)

        # Size of the inventory UI is 2/3 of the screen
        self.width, self.height = scale[0] * 10, scale[1] * 10

        # Center the UI.
        self.origin = ((scale[0] * 15 - self.width) / 2, (scale[1] * 15 - self.height) / 2)

        # The background color of the UI.
        self.color = inv_color

    def draw(self, surface: pygame.Surface, items=None):
        rectangle = Rect(self.origin, (self.width, self.height))

        inventory_surface = surface.subsurface(rectangle)
        inventory_surface.fill((0, 0, 0))

        if surface.unlock():
            surface.blit(inventory_surface, self.origin)

        for i, item in enumerate(items, start=1):
            item_coords = tuple(val + (val * i) for val in item.rect.size)

            inventory_surface.blit(item.image, item_coords)
