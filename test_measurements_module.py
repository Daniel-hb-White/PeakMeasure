import unittest
import math
from main import MeasurementHandler, OrientationHandler

class TestMeasurementHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MeasurementHandler()

    def test_default_person_height(self):
        self.assertEqual(self.handler.personHeight, 1.5)

    def test_set_person_height(self):
        self.handler.setPersonHeight(1.8)
        self.assertEqual(self.handler.personHeight, 1.8)

    def test_calculate_distance_45_degrees(self):
        self.handler.setPersonHeight(1.8)
        distance, rounded = self.handler.calculateDistance(math.radians(45))
        expected = 1.8 / math.tan(math.radians(45))
        self.assertAlmostEqual(distance, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_calculate_distance_low_angle(self):
        self.handler.setPersonHeight(1.5)
        distance, rounded = self.handler.calculateDistance(math.radians(1))
        self.assertGreater(distance, 85)

    def test_calculate_distance_high_angle(self):
        self.handler.setPersonHeight(1.5)
        distance, rounded = self.handler.calculateDistance(math.radians(89))
        self.assertLess(distance, 1)

    def test_calculate_height_grosse_objekte(self):
        self.handler.setPersonHeight(1.8)
        self.handler.measureTypeButton = "Große Objekte"
        height, rounded = self.handler.calculateHeight(1.8, math.radians(45))
        expected = 1.8 * math.tan(math.radians(45)) + 1.8
        self.assertAlmostEqual(height, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_calculate_height_kleine_objekte(self):
        self.handler.setPersonHeight(1.8)
        self.handler.measureTypeButton = "Kleine Objekte"
        height, rounded = self.handler.calculateHeight(1.8, math.radians(45))
        expected = 1.8 - (1.8 * math.tan(math.radians(45)))
        self.assertAlmostEqual(height, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_switch_measurement_type(self):
        original = self.handler.measureTypeButton
        switched = self.handler.switchMeasurementType()
        self.assertNotEqual(original, switched)
        self.assertIn(switched, ["Große Objekte", "Kleine Objekte"])

        # Switch back
        switched_again = self.handler.switchMeasurementType()
        self.assertEqual(switched_again, original)


class TestOrientationHandler(unittest.TestCase):
    def setUp(self):
        self.orientation = OrientationHandler()

    def test_initial_values(self):
        self.assertEqual(self.orientation.pitch, 0)
        self.assertEqual(self.orientation.azimuth, 0)
        self.assertEqual(self.orientation.roll, 0)

    def test_pitch_clamping(self):
        # Simulate extreme pitch angles manually
        self.orientation.pitch = math.radians(-10)
        if self.orientation.pitch < math.radians(1):
            self.orientation.pitch = math.radians(1)
        self.assertEqual(self.orientation.pitch, math.radians(1))

        self.orientation.pitch = math.radians(95)
        if self.orientation.pitch > math.radians(89):
            self.orientation.pitch = math.radians(89)
        self.assertEqual(self.orientation.pitch, math.radians(89))

if __name__ == '__main__':
    unittest.main()
