import pygame

from src.utils import asset


class Maze:
    def __init__(self):
        self.wall = pygame.image.load(asset('wall.png'))
        # self.walls = pygame.sprite.Group()

        self.floor = pygame.image.load(asset('floor.png'))

        self.M = 15  # Number of columns
        self.N = 15  # Number of rows

        self.pattern = [
            # TODO: Make a method that transform a string pattern into a MxN matrix like this :
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", "S", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", "#", "#", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", " ", "#", "#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", " ", " ", "#", "#", " ", " ", " ", "#", " ", "#", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ", " ", "#"],
            ["#", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "#", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "F", "#", "#", "#", "#", "#", "#", "#"],
        ]
        self.grid = self.pattern

        # Starting and ending point coordinates.
        self.start = self.find_points('S')
        self.end = self.find_points('F')

    def draw(self, screen):
        for x, rows in enumerate(self.grid):
            for y, tile in enumerate(rows):

                if tile == "#":
                    screen.blit(self.wall, (x * 20, y * 20))

                elif tile == " ":
                    screen.blit(self.floor, (x * 20, y * 20))

    def find_points(self, wanted):
        """Find the coordinates of the specified point (start or end)"""
        for x, rows in enumerate(self.grid):
            for y, tile in enumerate(rows):
                if tile == wanted:
                    return x, y



