import numpy as np
from PIL import Image
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.camera import Camera
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # type: ignore


class RootWidget(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule a check for camera permissions in the main thread
        Clock.schedule_interval(self.check_camera_permissions, 1)

    def check_camera_permissions(self, *args):
        if platform == "android":
            if check_permission(Permission.CAMERA):
                print("Success: Camera permission already granted.")
                self.setup_camera()
                Clock.unschedule(self.check_camera_permissions)
            else:
                print("Error: Camera permission not granted yet.")
        else:
            # On non-Android platforms, simulate permission granted
            self.setup_camera()
            Clock.unschedule(self.check_camera_permissions)

    def setup_camera(self):
        print("Setting up the camera...")
        window_width, window_height = Window.size
        # Hidden camera widget only for accessing the camera; not visible
        self.camera = Camera(resolution=(int(window_width), int(window_height)), play=True, opacity=0)
        self.add_widget(self.camera)

        # Schedule the update_image method to process the camera feed
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


class Main(MDApp):

    def build(self):
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "White"

        # Ask for permissions if on Android
        if platform ==  "android":
            self.request_app_permissions()
        else:
            Window.size = (360, 640)

        return RootWidget()

    def request_app_permissions(self):
        request_permissions([Permission.CAMERA], self.on_app_permissions_result)

    def on_app_permissions_result(self, permissions, results):
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Camera permission granted.")
        else:
            print("Error: Camera permission not granted.")


Main().run()
