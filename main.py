#Imports

#Kivy
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.animation import Animation


#KivyMD
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.boxlayout import MDBoxLayout



#Custom Buttons/Cards
class Playing_Card(MDButton):
    pass

class Settings_Btn(RotateBehavior, MDBoxLayout):
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
        #App Theming
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "100"
        self.theme_cls.theme_style_switch_animation_duration = 0.4

        Window.set_icon(("icon.png"))
        #App Default Font & Font Styles
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
        #Assigning Screens to Screen Manager
        sm = SM()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Rules(name="Rules"))
        sm.add_widget(Settings(name="Settings"))
        sm.current = "Menu"
        return sm

    def settings(self,widget):
        current = self.root.current
        self.root.transition.duration = 0

        if current == "Menu": #Opening Settings
            
            anim = Animation(rotate_value_angle=90, d=0.3)
            anim.bind(on_complete=lambda *x: self.switch_screen("Settings"))
            anim.start(widget)

        else: #Close Settings
            anim = Animation(rotate_value_angle=0, d=0.3)
            anim.bind(on_complete=lambda *x: self.switch_screen("Menu"))
            anim.start(widget)

    def switch_screen(self, screen_name):
        self.root.current = screen_name

#Running App
if __name__ == "__main__":
    GoFishApp().run()