import math
import json
import numpy as np
from PIL import Image
from kivymd.app import MDApp
from datetime import datetime
from plyer import spatialorientation

from kivymd.app import MDApp
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission # type: ignore
    documents_path = "./height_data.json"

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

    
    @mainthread
    def setup_camera(self):
        """
        Set up the camera widget programmatically because of complications with android permissions & Kivy's camera widget.
        """
        print("Setting up camera..")
        if check_permission(Permission.CAMERA):
            # Create hidden camera widget used only for accessing the camera feed
            self.camera = Camera(play=True, opacity=0)
            self.ids.screen_camera.add_widget(self.camera)
            # Schedule the camera feed update at 30 FPS
            Clock.schedule_interval(self.update_image, 1.0 / 30.0)
            print("Camera setup complete.")

    def update_image(self, dt):
        """
        Update the camera feed by rotating the image received from Kivy's 'Camera' widget,
        then displaying it on the screen by updating the 'Image' widget.

        :param dt: The time interval since the last update.
        """
        if self.camera and self.camera.texture:
            texture = self.camera.texture
            width, height = texture.size

            # Convert the texture to a NumPy array for manipulation
            pixels = np.frombuffer(texture.pixels, dtype=np.uint8).reshape(height, width, 4)
            pil_image = Image.fromarray(pixels, mode='RGBA')

            # Rotate the image by 90 degrees
            transformed_image = pil_image.rotate(90, expand=True)

            # Create a new texture from the rotated image
            rotated_texture = Texture.create(size=(transformed_image.width, transformed_image.height), colorfmt='rgba')
            rotated_texture.blit_buffer(transformed_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')

            # Update the texture of the Image widget
            self.ids.image_camera.texture = rotated_texture

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
        if not then act as a normal button (start process of height calculation).

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

    def text_field_person_height_on_text(self, text):
        """Set the person's height based on user input."""
        try:
            self.measurementsHandler.setPersonHeight(float(text))
            self.label = ""
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
                self.distance, self.distanceRounded = self.measurementsHandler.calculateDistance(self.orientationHandler.getPitch())
                self.step = 1

            elif self.step == 1:
                # Step 2: Calculate height using distance and new pitch angle
                height, self.heightRounded = self.measurementsHandler.calculateHeight(self.distance, self.orientationHandler.getPitch())
                self.step = 2
                self.export_height_data_as_json(height)
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
        """
        Export the calculated height data as a JSON file.

        :param height: The height value to save.
        """
        new_entry = {
            "height": height,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        file_path = documents_path

        try:
            # Bestehende Daten laden, falls möglich
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    if not isinstance(data, list):
                        data = [data]
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(new_entry)

            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Höhenwert erfolgreich als JSON gespeichert: {file_path}")

            # Debug-Ausgabe
            print("Aktueller JSON-Inhalt:", data)

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

    def getPitch(self):
        return self.__pitch
    
    def getAzimuth(self):
        return self.__azimuth
    
    def getRoll(self):
        return self.__roll

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
        self.__personHeight = 1.5  # Default height in meters
        self.__measureTypeButton = "Große Objekte"

    def setPersonHeight(self, height):
        """
        Set the height of the person used as a reference in calculations.

        :param height: Height of the person in meters
        """
        self.__personHeight = height    

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

#----------------------------------------------------------------------------------

class Main(MDApp):
    """
    Main application class that initializes and runs the KivyMD app.
    """

    def build(self):
        """
        Build the application UI and initialize platform-specific settings.
        """
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "White"

        self.root = RootWidget()

        # Handle platform-specific configurations
        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
            self.root.setup_camera()
        elif platform == "android":
            self.request_app_permissions()

        return self.root
    
    def request_app_permissions(self):
        """
        Request necessary permissions for the app to function on Android.
        """
        request_permissions([Permission.CAMERA], self.on_app_permissions_result)

    def on_app_permissions_result(self, permissions, results):
        """
        Handle the result of the permission request.

        :param permissions: List of requested permissions.
        :param results: List of results for each permission.
        """
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Required permissions granted.")
            self.root.setup_camera()
        else:
            print("Error: Required permissions not granted.")

    def on_start(self):
        """
        Called when the app starts. Enables the orientation sensor listener.
        """
        self.root.orientationHandler.enableListener()

    def on_stop(self):
        """
        Called when the app stops. Disables the orientation sensor listener.
        """
        self.root.orientationHandler.disableListener()


Main().run()
