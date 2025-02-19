from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.relativelayout import RelativeLayout

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


class RootWidget(RelativeLayout):
    pass

class PeakMeasureApp(MDApp):

    # def on_start(self):
    #     self.fps_monitor_start()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "White"

        if platform not in ["android", "ios"]:
            Window.size = (360, 640)

        return RootWidget()


PeakMeasureApp().run()
