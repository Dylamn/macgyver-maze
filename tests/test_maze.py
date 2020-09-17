import unittest
import pygame

from src.maze.maze import Maze
from src.maze.wall import Wall
from src.maze.floor import Floor


class MazeTestCase(unittest.TestCase):
    """Tests for Maze class."""

    @classmethod
    def setUpClass(cls) -> None:
        # The following lines are necessary for the tests to work.
        # Maze class create Wall and Floor instances which needs to be added in a sprite group.
        cls.walls = pygame.sprite.Group()
        cls.floors = pygame.sprite.Group()

        # Assign the groups for each class.
        Wall.containers = cls.walls
        Floor.containers = cls.floors

        cls.maze = Maze((1, 1), file_pattern='tests/test_maze.txt')

    def test_maze_length(self):
        """Test the length of the maze. (Must be a 15x15)"""
        self.assertEqual(15, self.maze.columns, "columns is not equal to 15.")
        self.assertEqual(15, self.maze.rows, "N is not equal to 15.")

        self.assertEqual(15, len(self.maze.grid), "the lines of the maze does not have the intended dimensions.")

        for columns in self.maze.grid:
            self.assertEqual(15, len(columns), "The columns of the maze does not have the intended dimensions.")

    def test_maze_pattern(self):
        """Test if the maze grid is correctly built."""
        self.assertEqual([
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "#", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", "S", "#"],
            ["#", " ", " ", " ", " ", "#", "#", " ", "#", " ", " ", " ", "#", "#", "#"],
            ["#", "#", "#", "#", " ", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
            ["#", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", "#"],
            ["#", " ", " ", " ", " ", "#", "#", " ", " ", "#", "#", "#", "#", "#", "#"],
            ["#", "#", " ", "#", "#", "#", "#", "#", " ", " ", " ", "#", " ", "#", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ", " ", "#"],
            ["#", "#", "#", "#", "#", " ", "#", "#", "#", "#", "#", " ", "#", " ", "#"],
            ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#"],
            ["#", " ", "#", "#", "#", "#", " ", " ", "#", " ", "#", "#", "#", " ", "#"],
            ["#", " ", "#", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ", "#"],
            ["#", " ", " ", " ", "#", "#", "#", "#", " ", " ", "#", " ", "#", " ", "#"],
            ["#", " ", " ", "#", " ", " ", "#", " ", " ", "#", "#", " ", " ", " ", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "F", "#", "#", "#", "#", "#", "#", "#"],
        ], self.maze.grid, "Parsed Maze pattern doesn't match.")

    def test_random_coordinates(self):
        point = self.maze.random_coordinates()
        x, y = point
        adjacents = [
            (x - 1, y),  # left
            (x + 1, y),  # right
            (x, y + 1),  # top
            (x, y - 1),  # bottom
        ]

        # Check to see if there are any adjacent tiles, they've normally been removed.
        for adjacent in adjacents:
            self.assertNotIn(adjacent, self.maze.empty_tiles)


if __name__ == '__main__':
    unittest.main()
