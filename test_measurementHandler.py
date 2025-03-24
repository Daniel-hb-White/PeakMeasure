import unittest
import math
from MeasurementHandler import MeasurementHandler

class TestMeasurementHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MeasurementHandler()

    def test_default_person_height(self):
        self.assertEqual(self.handler.getPersonHeight(), 1.5)

    def test_set_person_height(self):
        self.handler.setPersonHeight(1.8)
        self.assertEqual(self.handler.getPersonHeight(), 1.8)

    def test_calculate_distance_45_degrees(self):
        self.handler.setPersonHeight(1.8)
        distance, rounded = self.handler.calculateDistance(45)
        expected = 1.8 / math.tan(math.radians(45))
        self.assertAlmostEqual(distance, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_calculate_distance_low_angle(self):
        self.handler.setPersonHeight(1.5)
        distance, rounded = self.handler.calculateDistance(1)
        self.assertGreater(distance, 85)

    def test_calculate_distance_high_angle(self):
        self.handler.setPersonHeight(1.5)
        distance, rounded = self.handler.calculateDistance(89)
        self.assertLess(distance, 1)

    def test_calculate_height_grosse_objekte(self):
        self.handler.setPersonHeight(1.8)
        self.handler.setMeasureTypeButton("Große Objekte")
        height, rounded = self.handler.calculateHeight(1.8, 45)
        expected = 1.8 * math.tan(math.radians(45)) + 1.8
        self.assertAlmostEqual(height, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_calculate_height_kleine_objekte(self):
        self.handler.setPersonHeight(1.8)
        self.handler.setMeasureTypeButton("Kleine Objekte")
        height, rounded = self.handler.calculateHeight(1.8, 45)
        expected = 1.8 - (1.8 * math.tan(math.radians(45)))
        self.assertAlmostEqual(height, expected, places=5)
        self.assertEqual(rounded, round(expected, 2))

    def test_switch_measurement_type(self):
        original = self.handler.getMeasureTypeButton()
        switched = self.handler.switchMeasurementType()
        self.assertNotEqual(original, switched)
        self.assertIn(switched, ["Große Objekte", "Kleine Objekte"])

        # Switch back
        switched_again = self.handler.switchMeasurementType()
        self.assertEqual(switched_again, original)

if __name__ == '__main__':
    unittest.main()
