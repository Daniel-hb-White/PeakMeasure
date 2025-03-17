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

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission


class RootWidget(RelativeLayout):
    
    # Orientation values in degrees
    pitch = NumericProperty(0)
    pitchRounded = NumericProperty(0)
    azimuth = NumericProperty(0)
    roll = NumericProperty(0)

    # Measurement values
    distance = NumericProperty(0)
    label = StringProperty("")
    step = NumericProperty(0)    # Step tracker (0 = measuring distance, 1 = measuring height, 2 = reset values)

    facade = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.camera_initialized = False
        self.capture = None
        self.image_widget = self.ids.camera_image

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

    def update_label_distance_value(self, distance):
        self.ids.label_distance.text = f"Distanz:\n{distance}m"

    def update_label_height_value(self, height):
        self.ids.label_height.text = f"Höhe:\n{height}m"

    def text_field_person_height_on_text(self, text):
        print(f"Text entered: {text}")

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
                distance = h * math.tan(self.pitch)
                self.update_label_distance_value(distance)
                self.step = 1
            elif self.step == 1:
                # Step 2: Calculate height using distance and new pitch angle
                height = self.distance * math.tan(self.pitch) + h
                self.update_label_height_value(height)
                self.step = 2
            else:
                self.update_label_distance_value("")
                self.update_label_height_value("")


        except Exception as e:
            # Handle any unexpected errors during calculation
            self.label = f"Fehler: {str(e)}"


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
