import math

class MeasurementHandler:
    """
    Author: Daniel
    """
    def __init__(self):
        """
        Initialize the measurement handler with a default person height (1.5 m)
        and default measurement mode set to 'Große Objekte' (Tall Objects).
        """
        self.__personHeight = 1.5  # Default height in meters
        self.__measureTypeButton = "Große Objekte"

    def setPersonHeight(self, height):
        """
        Set the height of the person used as a reference in calculations.

        :param height: Height of the person in meters
        """
        self.__personHeight = height

    def getPersonHeight(self):
        return self.__personHeight

    def setMeasureTypeButton(self, type):
        self.__measureTypeButton = type

    def getMeasureTypeButton(self):
        return self.__measureTypeButton    

    def calculateDistance(self, pitch):
        """
        Calculate horizontal distance based on the pitch angle.

        :param pitch: Pitch angle in degrees
        :return: Tuple of (exact distance, rounded distance in meters)
        """
        distance = abs(self.__personHeight / math.tan(math.radians(pitch)))
        return distance, round(distance, 2)

    def calculateHeight(self, distance, pitch):
        """
        Calculate vertical height based on the horizontal distance and pitch angle.
        The formula adjusts based on the selected measurement type.

        :param distance: Horizontal distance in meters
        :param pitch: Pitch angle in degrees
        :return: Tuple of (exact height, rounded height in meters)
        """
        height = abs(distance * math.tan(math.radians(pitch)))
                
        if self.__measureTypeButton == "Große Objekte":
            height = height + self.__personHeight
        else:
            height = self.__personHeight - height

        return height, round(height, 2)

    def switchMeasurementType(self):
        """
        Toggle between 'Große Objekte' (Tall Objects) and 'Kleine Objekte' (Small Objects)
        measurement modes.

        :return: The updated measurement type as a string
        """
        if self.__measureTypeButton == "Große Objekte":
            self.__measureTypeButton = "Kleine Objekte"
        else:
            self.__measureTypeButton = "Große Objekte"

        return self.__measureTypeButton