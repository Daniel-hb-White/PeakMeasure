import math
import json
import os
import numpy as np
from PIL import Image
from kivymd.app import MDApp
from datetime import datetime
from plyer import spatialorientation

from kivymd.app import MDApp
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission # type: ignore
    documents_path = "./height_data.json"
else:
    documents_path = os.path.join(os.getcwd(), "height_data.json")

class RootWidget(ScreenManager):
    """
    Root widget that manages the application's screens and handles user interactions.
    """
    # Measurement values
    distanceRounded = NumericProperty(0)
    distance = NumericProperty(0)
    heightRounded = NumericProperty(0)
    step = NumericProperty(0)
    label = StringProperty("")
    measureTypeButton = StringProperty("Große Objekte")

    def __init__(self, **kwargs):
        """
        Initialize the RootWidget with default values and handlers for orientation and measurements.
        """
        super().__init__(**kwargs)
        self.transition = SlideTransition()
        self.touch_start_x = 0
        self.orientationHandler = OrientationHandler()
        self.measurementsHandler = MeasurementHandler()

    def on_touch_down(self, touch):
        """
        Handle touch down events and store the starting x-coordinate of the touch.

        :param touch: The touch event object containing touch details.
        """
        self.touch_start_x = touch.x
        print("Pressed screen at:", touch.x)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        Handle touch up events and determine if a swipe gesture occurred.
        If the swipe is large enough, navigate to the appropriate screen.
        if not then act as a normal button (start height calculation process).

        :param touch: The touch event object containing touch details.
        """
        touch_end_x = touch.x
        delta_x = touch_end_x - self.touch_start_x

        if abs(delta_x) > 100:
            if delta_x > 0:
                self.transition.direction = "right"
                self.current = "screen_settings"
            else:
                self.transition.direction = "left"
                self.current = "screen_camera"
        else:
            if self.current == "screen_camera":
                self.on_measure_button()

    def update_labe_distance_value(self, distance):
        """
        Update the distance label with the given distance value.

        :param distance: The distance value to display.
        """
        self.ids.label_distance.text = f"Distanz:\n{distance}m"

    def update_label_height_value(self, height):
        """
        Update the height label with the given height value.

        :param height: The height value to display.
        """
        self.ids.label_height.text = f"Höhe:\n{height}m"
    
    def text_field_person_height_on_text(self, text):
        """Set the person's height based on user input."""
        try:
            self.measurementsHandler.setPersonHeight(float(text))
        except ValueError:
            self.label = "Fehler: Ungültige Eingabe."
    
    def on_measure_button(self):
        """
        Handle button press to perform distance or height calculation in three steps:
        Step 0: Measure horizontal distance based on current pitch angle.
        Step 1: Measure vertical height using previously calculated distance and new pitch angle.
        Step 2: Reset distance and height values and return to Step 0.
        Author: Daniel Lacker
        """
        try:
            if self.step == 0:
                # Step 1: Calculate distance using the pitch angle
                self.distance, self.distanceRounded = self.measurementsHandler.calculateDistance(self.orientationHandler.pitch)
                self.step = 1

            elif self.step == 1:
                # Step 2: Calculate height using distance and new pitch angle
                height, self.heightRounded = self.measurementsHandler.calculateHeight(self.distance, self.orientationHandler.pitch)
                self.step = 2
            else:
                #Step 3: Reset values in UI
                self.resetMeasurements()    

        except Exception as e:
            # Handle any unexpected errors during calculation
            self.label = f"Fehler: {str(e)}"
    
    def switchMeasurementType(self):
        """
        Toggle the measurement type between 'Große Objekte' (Tall Objects) 
        and 'Kleine Objekte' (Small Objects), then reset measurement values.
        Author: Daniel Lacker
        """
        self.measureTypeButton = self.measurementsHandler.switchMeasurementType()
        self.resetMeasurements()
    
    def resetMeasurements(self):
        """
        Reset all measurement values (distance, height) and set the step counter back to 0.
        Author: Daniel Lacker
        """
        self.distanceRounded = 0
        self.heightRounded = 0
        self.step = 0

    def export_height_data_as_json(self, height):
        data = {
            "height": height,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        file_path = documents_path
        
        try:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Höhe erfolgreich als JSON gespeichert: {file_path}")
            
            # Überprüfen, ob die Datei erfolgreich gespeichert wurde
            with open(file_path, "r") as json_file:
                content = json.load(json_file)
                print("Gespeicherte JSON-Daten:", content)
                
        except Exception as e:
            print(f"Fehler beim Speichern der Höhe: {e}")

#---------------------------- OrientationHandler ---------------------------------
class OrientationHandler:
    """
    Author: Daniel Lacker
    """
    def __init__(self):
        """
        Initialize the orientation handler with default values for pitch, azimuth, and roll.
        """
        self.pitch = 0
        self.azimuth = 0
        self.roll = 0

    def enable_listener(self):
        """
        Enable the orientation sensor listener and start updating orientation values at a fixed interval.
        """
        spatialorientation.enable_listener()
        Clock.schedule_interval(self.get_orientation, 1 / 20.)

    def disable_listener(self):
        """
        Disable the orientation sensor listener and stop updating orientation values.
        """
        spatialorientation.disable_listener()
        Clock.unschedule(self.get_orientation)

    def get_orientation(self, dt):
        """
        Update the orientation properties (azimuth, pitch, roll) based on sensor data.
        Pitch is converted to a range between 1° and 89° to avoid extreme values.
        """
        if spatialorientation.orientation != (None, None, None):
            azimuth, pitch, roll = spatialorientation.orientation
            self.azimuth = azimuth * (180/math.pi)
            self.pitch = 90 - (pitch * (180/math.pi) * -1)
            # Clamp pitch to avoid extreme values
            if self.pitch < 1:
                self.pitch = 1
            elif self.pitch > 89:
                self.pitch = 89

            self.pitchRounded = round(self.pitch, 2)
            self.roll = roll * (180/math.pi)

#----------------------------------------------------------------------------------
#----------------------------- MeasurementHandler ---------------------------------
class MeasurementHandler:
    """
    Author: Daniel
    """
    def __init__(self):
        """
        Initialize the measurement handler with a default person height (1.5 m)
        and default measurement mode set to 'Große Objekte' (Tall Objects).
        """
        self.personHeight = 1.5  # Default height in meters
        self.measureTypeButton = "Große Objekte"

    def setPersonHeight(self, height):
        """
        Set the height of the person used as a reference in calculations.

        :param height: Height of the person in meters
        """
        self.personHeight = height    

    def calculateDistance(self, pitch):
        """
        Calculate horizontal distance based on the pitch angle.

        :param pitch: Pitch angle in degrees
        :return: Tuple of (exact distance, rounded distance in meters)
        """
        distance = abs(self.personHeight / math.tan(math.radians(pitch)))
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
                
        if self.measureTypeButton == "Große Objekte":
            height = height + self.personHeight
        else:
            height = self.personHeight - height

        return height, round(height, 2)

    def switchMeasurementType(self):
        """
        Toggle between 'Große Objekte' (Tall Objects) and 'Kleine Objekte' (Small Objects)
        measurement modes.

        :return: The updated measurement type as a string
        """
        if self.measureTypeButton == "Große Objekte":
            self.measureTypeButton = "Kleine Objekte"
        else:
            self.measureTypeButton = "Große Objekte"

        return self.measureTypeButton

#----------------------------------------------------------------------------------

class Main(MDApp):

    def build(self):
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "White"

        self.root = RootWidget()

        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
            self.setup_camera()
        elif platform == "android":
            self.request_app_permissions()

        return self.root
    
    def request_app_permissions(self):
        request_permissions([Permission.CAMERA], self.on_app_permissions_result)

    def on_app_permissions_result(self, permissions, results):
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Required permissions granted.")
            self.setup_camera()
        else:
            print("Error: Required permissions not granted.")

    def setup_camera(self):
        """
        Set up the camera widget programmatically because of complications with android permissions & Kivy's camera widget.
        """
        # Create hidden camera widget used only for accessing the camera feed, not visible
        if check_permission(Permission.CAMERA):
            self.camera = Camera(play=True, opacity=0)
            self.add_widget(self.camera)
            Clock.schedule_interval(self.update_image, 1.0 / 30.0)
            print("Camera setup complete.")

    def update_image(self, dt):
        """
        Update the camera feed by rotating the image received from Kivy's 'Camera' widget,
        then displaying it on the screen per 'Image' widget.

        :param dt: The time interval since the last update.
        """
        if self.camera and self.camera.texture:
            texture = self.camera.texture
            width, height = texture.size

            pixels = np.frombuffer(texture.pixels, dtype=np.uint8).reshape(height, width, 4)
            pil_image = Image.fromarray(pixels, mode='RGBA')

            transformed_image = pil_image.rotate(90, expand=True)

            rotated_texture = Texture.create(size=(transformed_image.width, transformed_image.height), colorfmt='rgba')
            rotated_texture.blit_buffer(transformed_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')

            self.root.ids.image_camera.texture = rotated_texture

    def on_start(self):
        self.root.orientationHandler.enable_listener()
        self.root.export_height_data_as_json(1.75)

    def on_stop(self):
        self.root.orientationHandler.disable_listener()


Main().run()
