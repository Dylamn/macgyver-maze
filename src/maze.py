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

        self.empty_tiles = []

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
                # elif tile == " ":
                #     self.empty_tiles.append((x, y))
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

    def random_coordinates(self):  # TODO: Make a function that delete adjacent index.
        """Generate random coordinates. The result is an unoccupied ground (not a S, F, I, or #)."""
        search = True
        coords = None

        # Try to find valid coordinates.
        while search:
            column = random.randint(0, self.M - 1)  # From 0 to 14
            line = random.randint(0, self.N - 1)  # From 0 to 14

            char = self.grid[column][line]

            if char not in ['#', 'S', 'F', 'I']:
                # Will stay at True if the selected tile is not adjacent to the guardian, an item or to MacGyver.
                # This allows items to be spread out by not being side by side.
                safe_place = True

                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if self.grid[column + y][line + x] in ['S', 'F', 'I']:
                            safe_place = False

                if safe_place:
                    coords = (line, column)

                    # Mark this tile as occuped by an item.
                    self.grid[column][line] = 'I'
                    search = False

        return coords

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                # Ignore lines that begin with ";". These are comments.
                if not line.startswith(';'):
                    row = list(line.strip('\n'))
                    self.grid.append(row)
