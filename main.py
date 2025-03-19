from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # type: ignore


class RootWidget(RelativeLayout):

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

        if platform not in ["android", "ios"]:
            Window.size = (360, 640)
        if platform == "android":
            request_permissions([Permission.CAMERA])
            if check_permission(Permission.CAMERA):
                print("Camera permission granted.")
            else:
                print("Camera permission not granted.")

        return RootWidget()


Main().run()
