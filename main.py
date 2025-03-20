from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.clock import Clock

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # type: ignore


class RootWidget(RelativeLayout):

    def setup_camera(self):
        self.camera = self.ids.hidden_camera
        if self.camera:
            self.camera.play = True
            Clock.schedule_interval(self.update_image, 1.0/30.0)

    def update_image(self, dt):
        if self.camera and self.camera.texture:
            texture = self.camera.texture
            width, height = texture.size

            # Create a new texture with swapped dimensions
            rotated_texture = Texture.create(size=(height, width), colorfmt='rgba')

            # Rearrange pixel data for -90° rotation and mirroring
            pixels = texture.pixels
            flipped_pixels = bytearray(len(pixels))

            for y in range(height):
                for x in range(width):
                    old_index = (y * width + x) * 4
                    new_index = ((width - x - 1) * height + (height - y - 1)) * 4  # Rotate -90° and mirror
                    flipped_pixels[new_index:new_index + 4] = pixels[old_index:old_index + 4]

            # Assign the rearranged pixel data to the new texture
            rotated_texture.blit_buffer(flipped_pixels, colorfmt='rgba', bufferfmt='ubyte')

            # Update the image widget with the new texture
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

        return RootWidget()

    def show_permission_popup(self):
        dialog = MDDialog(
            title="Permission Required",
            text="Camera access is required to use this app. Please grant camera permission.",
            buttons=[
                MDButton(
                    text="Retry",
                    on_release=self.request_app_permissions
                )
            ],
        )
        dialog.open()

    def request_app_permissions(self):
        request_permissions([Permission.CAMERA], self.on_app_permissions_result)

    def on_app_permissions_result(self, permissions, results):
        if Permission.CAMERA in permissions and results[permissions.index(Permission.CAMERA)]:
            print("Success: Camera permission granted.")
            self.root.setup_camera()
        else:
            print("Error: Camera permission not granted.")
            self.show_permission_popup()

    def on_start(self):
        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
            self.root.setup_camera()
        elif platform == "android":
            self.request_app_permissions()




Main().run()
