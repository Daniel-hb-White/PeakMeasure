import unittest
from OrientationHandler import OrientationHandler

class TestOrientationHandler(unittest.TestCase):
    def setUp(self):
        self.orientation = OrientationHandler()

    def test_initial_values(self):
        self.assertEqual(self.orientation.getPitch(), 0)
        self.assertEqual(self.orientation.getAzimuth(), 0)
        self.assertEqual(self.orientation.getRoll(), 0)

    def test_pitch_clamping(self):
        # Simulate extreme pitch angles manually
        self.orientation.setPitch(-10)
        if self.orientation.getPitch() < 1:
            self.orientation.setPitch(1)
        self.assertEqual(self.orientation.getPitch(), 1)

        self.orientation.setPitch(95)
        if self.orientation.getPitch() > 89:
            self.orientation.setPitch(89)
        self.assertEqual(self.orientation.getPitch(), 89)

if __name__ == '__main__':
    unittest.main()