from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton

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
        elif platform == "android":
            self.request_app_permissions()

        return RootWidget()

    def enable_camera(self):
        camera = self.root.ids.get("camera")
        if camera:
            camera.play = True

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
            self.enable_camera()
        else:
            print("Error: Camera permission not granted.")
            self.show_permission_popup()


Main().run()
