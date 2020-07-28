import pygame

from src.utils import asset, base_path
from src.wall import Wall
from src.floor import Floor


class Maze:
    grid = []

    def __init__(self, scale, walls: pygame.sprite.Group, floors: pygame.sprite.Group, file_pattern='maze.txt'):
        # Add references to the Maze class. Maybe useless,
        # I let them here for the moment.
        self.wall_container = walls
        self.floor_container = floors

        # Set a scale attribute that will be used by floors and walls.
        self.scale = scale

        self.M = 15  # Number of columns
        self.N = 15  # Number of rows

        self.pattern_file = file_pattern
        self.parse_maze_pattern()  # Populate the maze grid property.

        # Starting and ending point coordinates.
        self.start = self.find_points('S')
        self.end = self.find_points('F')

        self._init()

    def _init(self):
        """Setup the maze grid."""
        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):

                if tile == "#":
                    self.wall_container.add(Wall(x, y, self.scale))
                else:
                    self.floor_container.add(Floor(x, y, self.scale))

    def find_points(self, wanted: str):
        """Find the coordinates of the specified point (start or end)"""
        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):
                if tile == wanted:
                    return x, y

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                row = list(line.strip('\n'))
                self.grid.append(row)
