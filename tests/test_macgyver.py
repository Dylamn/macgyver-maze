import unittest

from src.Macgyver import MacGyver


class MyTestCase(unittest.TestCase):
    def test_speed(self):
        macgyver = MacGyver()

        self.assertEqual(macgyver.SPEED.get('X'), (1, 0))
        self.assertEqual(macgyver.SPEED.get('Y'), (0, 1))


if __name__ == '__main__':
    unittest.main()
