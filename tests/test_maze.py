import unittest

from src.Maze import Maze


class MazeTestCase(unittest.TestCase):

    """Tests for Maze."""

    def test_maze_length(self):
        """Test the length of the maze. (Must be a 15x15)"""
        maze = Maze()

        self.assertEqual(maze.M, 15, "M is not equal to 15.")
        self.assertEqual(maze.N, 15, "N is not equal to 15.")

        self.assertEqual(len(maze.grid), 15, "the maze does not have the intended dimensions.")

        for columns in maze.grid:
            self.assertEqual(len(columns), 15, "The columns of the maze does not have the intented dimensions.")

    def test_maze_pattern(self):
        """Test if the maze grid is correctly builded."""
        maze = Maze('tests/test_maze.txt')

        self.assertEqual(maze.grid,  [
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
        ])


if __name__ == '__main__':
    unittest.main()
