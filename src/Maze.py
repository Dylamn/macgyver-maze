import pygame

from src.utils import asset, base_path


class Maze:
    grid = []

    def __init__(self, scale, file_pattern='maze.txt'):
        self.wall_original = pygame.image.load(asset('wall.png'))
        self.wall = pygame.transform.scale(self.wall_original, scale)
        # self.walls = pygame.sprite.Group()

        self.floor_original = pygame.image.load(asset('floor.png'))
        self.floor = pygame.transform.scale(self.floor_original, scale)

        self.M = 15  # Number of columns
        self.N = 15  # Number of rows

        self.pattern_file = file_pattern
        self.parse_maze_pattern()  # Populate the maze grid property.

        # Starting and ending point coordinates.
        self.start = self.find_points('S')
        self.end = self.find_points('F')

    def draw(self, screen, scale: tuple):
        """Draw the maze grid."""
        width, height = scale

        for y, rows in enumerate(self.grid):
            for x, tile in enumerate(rows):

                if tile == "#":
                    screen.blit(self.wall, (x * width, y * height))
                else:
                    screen.blit(self.floor, (x * width, y * height))

    def find_points(self, wanted: str):
        """Find the coordinates of the specified point (start or end)"""
        for y, rows in enumerate(self.grid):
            for x, tile in enumerate(rows):
                if tile == wanted:
                    return x, y

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                row = list(line.strip('\n'))
                self.grid.append(row)
