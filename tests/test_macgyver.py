import unittest

from src.Macgyver import Macgyver


class MacGyverTestCase(unittest.TestCase):
    def test_moves(self):
        # Place Macgyver on the origin.
        macgyver = Macgyver((0, 0))

        self.assertEqual(macgyver.coordinates, (0, 0))
        macgyver.move_down()

        self.assertEqual(macgyver.coordinates, (0, 20))


if __name__ == '__main__':
    unittest.main()
