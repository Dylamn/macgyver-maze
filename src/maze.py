import random

from src.utils import base_path
from src.wall import Wall
from src.floor import Floor


class Maze:
    grid = []

    def __init__(self, scale, file_pattern='maze.txt'):
        """Default Maze constructor."""

        # Set a scale attribute that will be used by floors and walls.
        self.scale = scale

        self.M = 15  # Number of columns
        self.N = 15  # Number of rows

        self.pattern_file = file_pattern
        self.parse_maze_pattern()  # Populate the maze grid property.

        # Contains every coordinates where a item can be placed.
        # key/value dictionary. The key are coordinates and values are " " spaces character.
        self.empty_tiles = {}

        # Starting and ending point coordinates.
        self.start = self.find_points('S')
        self.end = self.find_points('F')

        self._init()

    def _init(self):
        """Setup the maze grid."""
        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):

                if tile == "#":
                    # Add a new wall.
                    Wall(x, y, self.scale)
                elif tile == " ":
                    Floor(x, y, self.scale)
                    # Add every empty tiles into the array `empty_tiles`.
                    # This array will be helpful for the placement of items.
                    self.empty_tiles.setdefault((x, y), " ")
                else:
                    # Add a new floor tile.
                    Floor(x, y, self.scale)

    def find_points(self, wanted: str):
        """Find the coordinates of the specified point (start or end)"""
        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):

                # Turn both strings into lowercase because "S" or "F" can be lowercase in the pattern file.
                if tile.lower() == wanted.lower():
                    return x, y

    def random_coordinates(self):
        """Generate random coordinates. The result is an unoccupied ground (not a S, F, I, or #)."""
        coords = random.choice(list(self.empty_tiles))
        print(len(self.empty_tiles))

        # Remove the selected tile.
        self.empty_tiles.pop(coords, None)
        print(len(self.empty_tiles))

        # Remove adjacent empty tiles.
        self._remove_adjacent_coordinates(coords)
        print(len(self.empty_tiles))
        exit(1)

        # Extract x and y point.
        column, line = coords
        self.grid[column][line] = 'I'

        return coords

    def _remove_adjacent_coordinates(self, point: tuple):
        """Remove adjacent empty tiles (ommit the possibility to place an item next to another)"""
        for i in [-1, 1]:
            col, row = point
            adjacent_x = (col + i, row)
            adjacent_y = (col, row + i)

            if adjacent_x in self.empty_tiles:
                self.empty_tiles.pop(adjacent_x, None)

            if adjacent_y in self.empty_tiles:
                self.empty_tiles.pop(adjacent_y, None)

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                # Ignore lines that begin with ";". These are comments.
                if not line.startswith(';'):
                    row = list(line.strip('\n'))
                    self.grid.append(row)
