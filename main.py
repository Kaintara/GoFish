#Imports

import random

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
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import RelativeLayout


#Custom Buttons/Cards
class Playing_Card(MDCard):
    def __init__(self,suit="",rank="",**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.suit = suit
        app = MDApp.get_running_app()
        if self.suit == "cards-diamond" or self.suit == "cards-heart":
            self.colour = app.theme_cls.inversePrimaryColor
        else:
            self.colour = app.theme_cls.primaryColor
        self.layout = RelativeLayout()
        self.icon = MDButtonIcon(
            icon = self.suit,
            size_hint = (None,None),
            theme_font_size = "Custom",
            font_size = "50sp",
            theme_icon_color= "Custom",
            icon_color = self.colour, 
            pos_hint = {"center_x":0.5, "center_y":0.5},
            on_release = lambda x:app.change_theme(self.colour)
        )
        self.layout.add_widget(self.icon)
        self.add_widget(self.layout)
    def change_colour(self):
        self.layout.remove_widget(self.icon)
        self.icon = MDButtonIcon(
            icon = self.suit,
            size_hint = (None,None),
            theme_font_size = "Custom",
            font_size = "50sp",
            theme_icon_color= "Custom",
            icon_color = self.colour, 
            pos_hint = {"center_x":0.5, "center_y":0.5}
        )
        self.layout.add_widget(self.icon)
        

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
        self.colours = ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet', 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral', 'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan', 'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta', 'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen', 'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet', 'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick', 'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink', 'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen', 'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow', 'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen', 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow', 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue', 'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen', 'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose', 'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange', 'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred', 'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']
        self.suits = ["cards-spade","cards-diamond","cards-heart","cards-club"]
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
    
    def get_widget(self, widget, screen):
        return self.root.get_screen(screen).ids[widget]
    
    def back(self): #Back button
        sm = self.root
        if self.sm_stack[0] == sm.current:
            self.sm_stack.remove(sm.current)
            sm.current = self.sm_stack[0]
        elif sm.previous:
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
        self.theme_cls.primary_palette = colour

    def on_start(self):
        grid = self.get_widget("grid","Settings")
        for colour in self.colours:
            int = random.randint(0,3)
            card = Playing_Card(self.suits[int],"")
            #card.md_bg_color = colour.lower() Needs to be fixed!!!
            card.colour = colour.lower()
            card.change_colour()
            grid.add_widget(card)
        return super().on_start()
        
#Running App
if __name__ == "__main__":
    GoFishApp().run()