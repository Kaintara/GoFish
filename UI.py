from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.lang.builder import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import FontContextManager as FCM


#Custom Buttons/Cards
class RoundedButton(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

#Screens
class SM(ScreenManager):
    pass

class MainMenu(Screen):
    pass

class InGame(Screen):
    pass

class Settings(Screen):
    pass


#App Bulid
class GoFishApp(App):
    def build(self):
        sm = SM()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Settings(name="Settings"))
        sm.current = "Menu"
        return sm

#Running App
if __name__ == "__main__":
    GoFishApp().run()

def colour(colour):
    print(get_color_from_hex(colour))