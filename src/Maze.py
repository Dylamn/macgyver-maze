import pygame

from src.utils import asset, base_path


class Maze:
    grid = []

    def __init__(self, file_pattern='maze.txt'):
        self.wall = pygame.image.load(asset('wall.png'))
        # self.walls = pygame.sprite.Group()

        self.floor = pygame.image.load(asset('floor.png'))

        self.M = 15  # Number of columns
        self.N = 15  # Number of rows

        self.pattern_file = file_pattern
        self.parse_maze_pattern()  # Populate the maze grid property.

        # Starting and ending point coordinates.
        self.start = self.find_points('S')
        self.end = self.find_points('F')

    def draw(self, screen):
        for x, rows in enumerate(self.grid):
            for y, tile in enumerate(rows):

                if tile == "#":
                    screen.blit(self.wall, (x * 20, y * 20))

                elif tile == " " or tile == "S" or tile == "F":
                    screen.blit(self.floor, (x * 20, y * 20))

    def find_points(self, wanted):
        """Find the coordinates of the specified point (start or end)"""
        for x, rows in enumerate(self.grid):
            for y, tile in enumerate(rows):
                if tile == wanted:
                    return x, y

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                row = list(line.strip('\n'))
                self.grid.append(row)
