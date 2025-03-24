import math

from kivy.clock import Clock
from plyer import spatialorientation


class OrientationHandler:
    """
    Author: Daniel Lacker
    """
    def __init__(self):
        """
        Initialize the orientation handler with default values for pitch, azimuth, and roll.
        """
        self.__pitch = 0
        self.__azimuth = 0
        self.__roll = 0

    def enableListener(self):
        """
        Enable the orientation sensor listener and start updating orientation values at a fixed interval.
        """
        spatialorientation.enable_listener()
        Clock.schedule_interval(self.getOrientation, 1 / 20.)

    def disableListener(self):
        """
        Disable the orientation sensor listener and stop updating orientation values.
        """
        spatialorientation.disable_listener()
        Clock.unschedule(self.getOrientation)

    def getOrientation(self, dt):
        """
        Update the orientation properties (azimuth, pitch, roll) based on sensor data.
        Pitch is converted to a range between 1° and 89° to avoid extreme values.
        """
        if spatialorientation.orientation != (None, None, None):
            azimuth, pitch, roll = spatialorientation.orientation
            self.__azimuth = azimuth * (180/math.pi)
            self.__pitch = 90 - (pitch * (180/math.pi) * -1)
            # Clamp pitch to avoid extreme values
            if self.__pitch < 1:
                self.__pitch = 1
            elif self.__pitch > 89:
                self.__pitch = 89

            self.__roll = roll * (180/math.pi)

    def setPitch(self, pitch):
        """
        Only used in test
        """
        self.__pitch = pitch

        return self

    def getPitch(self):
        return self.__pitch
    
    def getAzimuth(self):
        return self.__azimuth
    
    def getRoll(self):
        return self.__roll