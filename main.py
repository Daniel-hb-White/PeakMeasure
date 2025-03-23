import numpy as np
from PIL import Image
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.graphics.texture import Texture

from kivy.clock import Clock

if platform == "android":
    from android.permissions import request_permissions, Permission  # type: ignore


class RootWidget(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition()
        self.touch_start_x = 0

    def on_touch_down(self, touch):
        self.touch_start_x = touch.x
        print("Pressed screen at:", touch.x)

    def on_touch_up(self, touch):
        touch_end_x = touch.x
        delta_x = touch_end_x - self.touch_start_x

        if abs(delta_x) > 100:
            if delta_x > 0:
                self.transition.direction = "right"
                self.current = "screen_settings"
            else:
                self.transition.direction = "left"
                self.current = "screen_camera"

    def setup_camera(self):
        self.camera = self.ids.hidden_camera
        if self.camera:
            self.camera.play = True
            Clock.schedule_interval(self.update_image, 1.0 / 30.0)

    def update_image(self, dt):
        if self.camera and self.camera.texture:
            texture = self.camera.texture
            width, height = texture.size

            pixels = np.frombuffer(texture.pixels, dtype=np.uint8).reshape(height, width, 4)
            pil_image = Image.fromarray(pixels, mode='RGBA')

            transformed_image = pil_image.rotate(90, expand=True)

            rotated_texture = Texture.create(size=(transformed_image.width, transformed_image.height), colorfmt='rgba')
            rotated_texture.blit_buffer(transformed_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')

            self.ids.image_camera.texture = rotated_texture

    def update_labe_distance_value(self, distance):
        self.ids.label_distance.text = f"Distanz:\n{distance}m"

    def update_label_height_value(self, height):
        self.ids.label_height.text = f"Höhe:\n{height}m"

    def text_field_person_height_on_text(self, text):
        print(f"Text entered: {text}")

    def update_labe_distance_value(self, distance):
        self.ids.label_distance.text = f"Distanz:\n{distance}m"

    def update_label_height_value(self, height):
        self.ids.label_height.text = f"Höhe:\n{height}m"

    def text_field_person_height_on_text(self, text):
        print(f"Text entered: {text}")


class Main(MDApp):

    def build(self):
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "White"

        return RootWidget()

    def request_app_permissions(self):
        request_permissions([Permission.CAMERA], self.on_app_permissions_result)

    def on_app_permissions_result(self, permissions, results):
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Camera permission granted.")
            self.root.setup_camera()
        else:
            print("Error: Camera permission not granted.")

    def on_start(self):
        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
            self.root.setup_camera()
        elif platform == "android":
            self.request_app_permissions()


Main().run()
