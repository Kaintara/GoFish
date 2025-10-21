#Imports
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp

#Custom Buttons/Cards
class Playing_Card(MDButton):
    pass

#Screens
class SM(MDScreenManager):
    pass

class MainMenu(MDScreen):
    pass

class InGame(MDScreen):
    pass

class Settings(MDScreen):
    pass

class Rules(MDScreen):
    pass


#App Bulid
class GoFishApp(MDApp):
    
    def build(self):

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "1000"

        Window.set_icon(("icon.png"))

        LabelBase.register(
            name="cataway",
            fn_regular="Catways.ttf",
        )

        self.theme_cls.font_styles["cataway"] = {
            "large" : {
                "line-height": 1.64,
                "font-name": "cataway",
                "font-size": sp(50),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "cataway",
                "font-size": sp(45),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "cataway",
                "font-size": sp(36),
            },
        }

        sm = SM()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Rules(name="Rules"))
        sm.add_widget(Settings(name="Settings"))
        sm.current = "Menu"
        return sm

#Running App
if __name__ == "__main__":
    GoFishApp().run()