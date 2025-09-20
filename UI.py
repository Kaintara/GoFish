from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex

class SM(ScreenManager):
    pass

class MainMenu(Screen):
    pass

class InGame(Screen):
    pass

class Settings(Screen):
    pass

class GoFish(App):
    def build(self):
        sm = SM()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Settings(name="Settings"))
        return sm


if __name__ == "__main__":
    GoFish().run()

def colour(colour):
    print(get_color_from_hex(colour))

colour('#8fcaca')