from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import M
from kivymd.uix.screenmanager import MDScreenManager

class MainMenu(MDScreen):
    pass

class InGame(MDScreen):
    pass

class Settings(MDScreen):
    pass

class GoFish(MDApp):
    def build(self):
        self.use_material3 = True
        self.theme_cls.primary_palette = "Teal"
        sm = MDScreenManager()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Settings(name="Settings"))
        return sm


if __name__ == "__main__":
    GoFish().run()

def colour(colour):
    print(get_color_from_hex(colour))

colour('#8fcaca')