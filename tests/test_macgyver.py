import pygame
import unittest

from src.characters.macgyver import Macgyver


class MacGyverTestCase(unittest.TestCase):
    """Tests for Macgyver class"""

    @classmethod
    def setUpClass(cls) -> None:
        character = pygame.sprite.GroupSingle()
        Macgyver.containers = character

        cls.macgyver = Macgyver((0, 0), (10, 10))

    def test_moves(self):
        # Place Macgyver on the origin.
        self.assertEqual((0, 0), self.macgyver.coordinates)

        self.macgyver.move_down()
        self.assertEqual((0, 10), self.macgyver.coordinates)

        self.macgyver.move_left()
        self.assertEqual((-10, 10), self.macgyver.coordinates)

        self.macgyver.move_up()
        self.assertEqual((-10, 0), self.macgyver.coordinates)

        self.macgyver.move_right()
        self.assertEqual((0, 0), self.macgyver.coordinates)

    def test_rollback(self):
        # The last movement was to go to the right. So it will come back 10 pixels to the left (-10, 0).
        self.macgyver.rollback()
        self.assertEqual((-10, 0), self.macgyver.coordinates)


if __name__ == '__main__':
    unittest.main()
