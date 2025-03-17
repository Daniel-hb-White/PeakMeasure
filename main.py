import math
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

# Load the user interface from the corresponding .kv file
Builder.load_file("sp_orientation_interface.kv")

class SpOrientationInterface(BoxLayout):

    # Orientation values in degrees
    pitch = NumericProperty(0)
    pitchRounded = NumericProperty(0)
    azimuth = NumericProperty(0)
    roll = NumericProperty(0)

    # Measurement values
    distance = NumericProperty(0)
    label = StringProperty("")
    measureButton = StringProperty("Distanz messen")
    step = NumericProperty(0)    # Step tracker (0 = measuring distance, 1 = measuring height)


    facade = ObjectProperty()

    def enable_listener(self):
        """Enable the orientation listener and start updating orientation values."""
        self.facade.enable_listener()
        Clock.schedule_interval(self.get_orientation, 1 / 20.)

    def disable_listener(self):
        """Disable the orientation listener and stop updating orientation values."""
        self.facade.disable_listener()
        Clock.unschedule(self.get_orientation)

    def get_orientation(self, dt):
        """Update the orientation properties if valid data is available."""
        if self.facade.orientation != (None, None, None):
            azimuth, pitch, roll = self.facade.orientation
            self.azimuth = azimuth * (180/math.pi)
            self.pitch = pitch * (180/math.pi) * -1
            self.pitchRounded = round(self.pitch, 2)
            self.roll = roll * (180/math.pi)
    
    def on_measure_button(self):
        """
        Handle button press to perform distance or height calculation in two steps.
        Step 0: Measure horizontal distance.
        Step 1: Measure vertical height using previously calculated distance.
        """
        try:
            h = 1.5 # Approximate phone height from the ground in meters

            if self.step == 0:
                # Step 1: Calculate distance using the pitch angle
                self.distance = h * math.tan(self.pitch)
                self.label = f"Gemessene Distanz: {self.distance:.2f} m"
                self.measureButton = "Höhe berechnen"
                self.step = 1

            else:
                # Step 2: Calculate height using distance and new pitch angle
                height = self.distance * math.tan(self.pitch) + h
                self.label = f"Berechnete Höhe: {height:.2f} m"
                self.measureButton = "Erneut messen"
                self.step = 0

        except Exception as e:
            # Handle any unexpected errors during calculation
            self.label = f"Fehler: {str(e)}"


class PeakMeassureApp(App):
    """Main application class."""
    def build(self):
        return SpOrientationInterface()

if __name__ == "__main__":
    PeakMeassureApp().run()