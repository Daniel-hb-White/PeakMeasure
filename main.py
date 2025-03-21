import numpy as np
from PIL import Image
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock

if platform == "android":
    from android.permissions import request_permissions, Permission  # type: ignore


class RootWidget(RelativeLayout):

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


class Main(MDApp):

    def build(self):
        self.icon = './mokup_und_logo/PeakMeasureLogo.png'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "White"

        self.root = RootWidget()

        if platform in ["android", "ios"]:
            self.request_app_permissions()
        else:
            # Simulate permissions granted on non-mobile platforms
            self.on_permissions_granted()

    def request_app_permissions(self):
        if platform == "android":
            request_permissions([Permission.CAMERA], self.on_app_permissions_result)
        else:
            # Simulate permission granted on non-Android platforms
            self.on_permissions_granted()

    def on_app_permissions_result(self, permissions, results):
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Camera permission granted.")
            self.on_permissions_granted()
        else:
            print("Error: Camera permission not granted.")

    def on_permissions_granted(self):
        print("Starting RootWidget...")
        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
        self.root.setup_camera()

Main().run()
