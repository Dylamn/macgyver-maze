import random

from src.utils import base_path
from src.maze.wall import Wall
from src.maze.floor import Floor


class Maze:
    def __init__(self, scale, file_pattern='maze.txt'):
        """Default Maze constructor."""

        # The grid of the maze.
        self.grid = []

        # Set a scale attribute that will be used by floors and walls.
        self.scale = scale

        self.columns = 15  # Number of columns
        self.rows = 15  # Number of rows

        self.pattern_file = file_pattern
        self.parse_maze_pattern()  # Populate the maze grid property.

        # Contains every coordinates where a item can be placed.
        # The key are coordinates and values are " " spaces character.
        self.empty_tiles = {}

        # Starting and ending point coordinates.
        self.start = self.find_points('s')
        self.end = self.find_points('f')

        self._init()

    def _init(self):
        """Setup the maze grid."""

        # Initialize vars which will contains
        # the coordinates of the guardian and macgyver
        mac_gyver_pos = None
        guardian_pos = None

        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):

                if tile == "#":
                    # Add a new wall.
                    Wall(x, y, self.scale)
                elif tile == " ":
                    Floor(x, y, self.scale)
                    # Add every empty tiles into the array `empty_tiles`.
                    # This array will be helpful for the placement of items.
                    self.empty_tiles[(x, y)] = " "
                else:
                    # Add a new floor tile.
                    Floor(x, y, self.scale)

                    if tile == "S":
                        # The tile where MacGyver will start
                        mac_gyver_pos = (x, y)
                    elif tile == "F":
                        # The tile where the guardian will stand
                        guardian_pos = (x, y)

        # At the end, we remove the tiles adjacent to macgyver
        # and the guardian from the list of empty tiles.
        self._remove_adjacent_coordinates(mac_gyver_pos)
        self._remove_adjacent_coordinates(guardian_pos)

    def find_points(self, wanted: str):
        """Find the coordinates of the specified point (start or end)"""
        for y, columns in enumerate(self.grid):
            for x, tile in enumerate(columns):

                # Turn "tile" string into lowercase for safe comparison.
                # Tile characters can be upper/lower case in the pattern file.
                if tile.lower() == wanted:
                    return x, y

    def random_coordinates(self):
        """Generate random coordinates.

        The result is an unoccupied ground (not a S, F, I, or #).
        """
        coords = random.choice(list(self.empty_tiles))

        # Remove the selected tile.
        self.empty_tiles.pop(coords, None)

        # Remove adjacent empty tiles.
        self._remove_adjacent_coordinates(coords)

        # Extract x and y point.
        column, line = coords
        self.grid[column][line] = 'I'

        return coords

    def _remove_adjacent_coordinates(self, point: tuple):
        """Remove adjacent empty tiles.

         Omit the possibility to place an item next to another
         """
        for i in [-1, 1]:
            col, row = point
            adjacent_x = (col + i, row)
            adjacent_y = (col, row + i)

            self.empty_tiles.pop(adjacent_x, None)
            self.empty_tiles.pop(adjacent_y, None)

    def parse_maze_pattern(self):
        """Populate the maze grid by reading the maze file pattern."""
        with open(base_path(self.pattern_file), 'r') as file:
            for line in file:
                # Ignore lines that begin with ";". These are comments.
                if not line.startswith(';'):
                    row = list(line.strip('\n'))
                    self.grid.append(row)
