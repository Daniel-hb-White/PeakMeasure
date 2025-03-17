import cv2

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.relativelayout import RelativeLayout

from kivymd.app import MDApp


class RootWidget(RelativeLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.capture = cv2.VideoCapture(0)
        self.image_widget = self.ids.camera_image
        Clock.schedule_interval(self.update_camera, 1 / 30)

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_widget.texture = texture

    def on_stop(self):
        if self.capture.isOpened():
            self.capture.release()

    def update_labe_distance_value(self, distance):
        self.ids.label_distance.text = f"Distanz:\n{distance}m"

    def update_label_height_value(self, height):
        self.ids.label_height.text = f"Höhe:\n{height}m"

    def text_field_person_height_on_text(self, text):
        print(f"Text entered: {text}")

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
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])

        return RootWidget()
    
    def on_stop(self):
        self.root.on_stop()


Main().run()
