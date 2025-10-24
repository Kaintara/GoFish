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

    def __init__(self, **kwargs):
        self.sm_stack = []
        super().__init__(**kwargs)
    
    def build(self):
        #App Theming
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "900"
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
    
    def back(self): #Back button
        sm = self.root
        if sm.previous:
            sm.current = self.sm_stack[0]
        else:
            sm.current = "Menu"

    def sm_stacky(self,widget): #Stores order of screens visited for back button
        if widget in self.sm_stack:
            self.sm_stack.remove(widget)
            self.sm_stack.insert(0, widget)
        else:
            self.sm_stack.insert(0, widget)

    def switch_icon(self,widget):
        if widget.name == "light":
            widget.icon = "weather-night"
            widget.name = "dark"
        else:
            widget.name = "light"
            widget.icon = "white-balance-sunny"
        

    def change_theme(self,colour):
        pass
        
#Running App
if __name__ == "__main__":
    GoFishApp().run()