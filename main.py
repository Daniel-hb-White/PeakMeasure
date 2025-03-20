import cv2
import math

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from plyer import spatialorientation

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission

class RootWidget(RelativeLayout):
    # Measurement values
    distanceRounded = NumericProperty(0)
    heightRounded = NumericProperty(0)
    label = StringProperty("")
    measureTypeButton = StringProperty("Große Objekte")

    facade = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.camera_initialized = False
        self.capture = None
        self.image_widget = self.ids.camera_image
        self.orientationHandler = OrientationHandler()
        self.measurementsHandler = MeasurementHandler()

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: Could not access the camera.")
        else:
            self.camera_initialized = True
            Clock.schedule_interval(self.update_camera, 1 / 30)
            print("Camera successfully started.")

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_widget.texture = texture

    def on_stop(self):
        if self.capture is not None and self.capture.isOpened():
            self.capture.release()
    
    def text_field_person_height_on_text(self, text):
        """Set the person's height based on user input."""
        try:
            self.measurementsHandler.setPersonHeight(float(text))
        except ValueError:
            self.label = "Fehler: Ungültige Eingabe."
    
    def on_measure_button(self):
        """
        Handle button press to perform distance or height calculation in two steps.
        Step 0: Measure horizontal distance.
        Step 1: Measure vertical height using previously calculated distance.
        Step 2: Reset distance and height value
        """
        try:
            if self.step == 0:
                # Step 1: Calculate distance using the pitch angle
                distance, self.distanceRounded = self.measurementsHandler.calculateDistance(self.orientationHandler.pitch)
                self.step = 1

            elif self.step == 1:
                # Step 2: Calculate height using distance and new pitch angle
                height, self.heightRounded = self.measurementsHandler.calculateHeight(distance, self.orientationHandler.pitch)
                self.step = 2
            else:
                #Step 3: Reset values in UI
                self.measurementsHandler.resetMeasurements()    

        except Exception as e:
            # Handle any unexpected errors during calculation
            self.label = f"Fehler: {str(e)}"
    
    def switchMeasurementType(self):
        self.measureTypeButton = self.measurementsHandler.switchMeasurementType()

#---------------------------- OrientationHandler ---------------------------------
class OrientationHandler:
    def __init__(self):
        self.pitch = 0
        self.azimuth = 0
        self.roll = 0

    def enable_listener(self):
        """Enable the orientation listener and start updating orientation values."""
        spatialorientation.enable_listener()
        Clock.schedule_interval(self.get_orientation, 1 / 20.)

    def disable_listener(self):
        """Disable the orientation listener and stop updating orientation values."""
        spatialorientation.disable_listener()
        Clock.unschedule(self.get_orientation)

    def get_orientation(self, dt):
        """Update the orientation properties if valid data is available."""
        if spatialorientation.orientation != (None, None, None):
            azimuth, pitch, roll = spatialorientation.orientation
            self.azimuth = azimuth * (180/math.pi)
            self.pitch = 90 - (pitch * (180/math.pi) * -1)
            #check border values -> lead to high results
            if self.pitch < 1:
                self.pitch = 1
            elif self.pitch > 89:
                self.pitch = 89
            self.pitchRounded = round(self.pitch, 2)
            self.roll = roll * (180/math.pi)

#----------------------------------------------------------------------------------
#----------------------------- MeasurementHandler ---------------------------------
class MeasurementHandler:
    def __init__(self):
        self.distance = 0
        self.distanceRounded = 0
        self.height = 0
        self.heightRounded = 0
        self.step = 0
        self.personHeight = 1.5  # Default height in meters
        self.measureTypeButton = "Große Objekte"

    def setPersonHeight(self, height):
        self.personHeight = height    

    def calculateDistance(self, pitch):
        """Calculate horizontal distance based on the pitch angle."""
        distance = abs(self.personHeight / math.tan(math.radians(pitch)))
        return distance, round(distance, 2)

    def calculateHeight(self, distance, pitch):
        """Calculate vertical height based on the horizontal distance and pitch angle."""
        height = abs(distance * math.tan(math.radians(pitch)))
                
        if self.measureTypeButton == "Große Objekte":
            height = height + self.personHeight
        else:
            height = self.personHeight - height

        return height, round(height, 2)

    def switchMeasurementType(self):
        """Toggle between 'Große Objekte' and 'Kleine Objekte'."""
        if self.measureTypeButton == "Große Objekte":
            self.measureTypeButton = "Kleine Objekte"
        else:
            self.measureTypeButton = "Große Objekte"

        self.resetMeasurements()

        return self.measureTypeButton

    def resetMeasurements(self):
        self.distanceRounded = 0
        self.heightRounded = 0
        self.step = 0
#----------------------------------------------------------------------------------

class Main(MDApp):

    # def on_start(self):
    #     self.fps_monitor_start()

    def build(self):
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "White"

        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
        if platform == "android":
            request_permissions([Permission.CAMERA])
            if check_permission(Permission.CAMERA):
                print("Camera permission granted.")
            else:
                print("Camera permission not granted.")

        return RootWidget()
    
    def on_start(self):
        self.root.start_camera()
        self.root.enable_listener()

    def on_stop(self):
        self.root.on_stop()
        self.root.disable_listener()

Main().run()
