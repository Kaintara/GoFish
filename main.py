#Imports

import random
from Game import Game
g = Game(2)

#Kivy
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale, Translate


#KivyMD
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.label import MDLabel


#Custom Buttons/Cards
class Theme_Playing_Card(MDCard):
    def __init__(self,suit="",**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.suit = suit
        self.bind(on_release = lambda x:app.change_theme(self.colour))
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
        )
        self.layout.add_widget(self.icon)
        self.add_widget(self.layout)
    def change_colour(self):
        app = MDApp.get_running_app()
        self.layout.remove_widget(self.icon)
        self.icon = MDButtonIcon(
            icon = self.suit,
            size_hint = (None,None),
            theme_font_size = "Custom",
            font_size = "50sp",
            theme_icon_color= "Custom",
            icon_color = app.colours_map[self.colour],
            pos_hint = {"center_x":0.5, "center_y":0.5}
        )
        self.layout.add_widget(self.icon)

class Card_Label(MDLabel):
     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rotate = Rotate(angle=180, origin=self.center)
        with self.canvas.after:
            PopMatrix()
            
class Playing_Card(MDCard):
    def __init__(self,suit_rank,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.suit = suit_rank[0]
        app = MDApp.get_running_app()
        if self.suit == "cards-diamond" or self.suit == "cards-heart":
            self.colour = app.theme_cls.inversePrimaryColor
        else:
            self.colour = app.theme_cls.primaryColor
        self.layout = RelativeLayout(
            size = ("64dp", "89dp")
        )
        self.up_text = MDLabel(
            text = suit_rank[1],
            font_style= "cataway",
            role= "small",
            halign= 'left',
            pos_hint= {"top":1, "center_x":0.2},
            theme_font_size= "Custom",
            font_size= dp(30),
            adaptive_size= True
        )
        self.down_text = Card_Label(
            pos_hint= {"top":1.1, "center_x":0.8},
            text= suit_rank[1],
            font_style= "cataway",
            role= "small",
            halign= "right",
            theme_font_size= "Custom",
            font_size= dp(30),
            adaptive_size= True
        )

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
        self.layout.add_widget(self.up_text)
        self.layout.add_widget(self.down_text)
        self.add_widget(self.layout)

        

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

class Themes(MDScreen):
    pass

class Stats(MDScreen):
    pass


#App Bulid
class GoFishApp(MDApp):

    def __init__(self, **kwargs):
        self.sm_stack = []
        self.colours = ['Lightpink', 'Pink', 'Crimson', 'Palevioletred', 'Lavenderblush', 'Hotpink', 'Deeppink', 'Mediumvioletred', 'Orchid', 'Fuchsia', 'Magenta', 'Darkmagenta', 'Purple', 'Violet', 'Plum', 'Thistle', 'Mediumorchid', 'Darkviolet', 'Darkorchid', 'Indigo', 'Blueviolet', 'Mediumpurple', 'Mediumslateblue', 'Darkslateblue', 'Slateblue', 'Blue', 'Mediumblue', 'Darkblue', 'Navy', 'Midnightblue', 'Lavender', 'Ghostwhite', 'Royalblue', 'Cornflowerblue', 'Lightsteelblue', 'Lightslategray', 'Lightslategrey', 'Slategray', 'Slategrey', 'Dodgerblue', 'Aliceblue', 'Steelblue', 'Lightskyblue', 'Skyblue', 'Deepskyblue', 'Lightblue', 'Powderblue', 'Cadetblue', 'Darkturquoise', 'Aqua', 'Cyan', 'Darkcyan', 'Teal', 'Darkslategray', 'Darkslategrey', 'Paleturquoise', 'Lightcyan', 'Azure', 'Mediumturquoise', 'Lightseagreen', 'Turquoise', 'Aquamarine', 'Mediumaquamarine', 'Mediumspringgreen', 'Springgreen', 'Mintcream', 'Mediumseagreen', 'Seagreen', 'Lime', 'Green', 'Darkgreen', 'Limegreen', 'Forestgreen', 'Lightgreen', 'Palegreen', 'Darkseagreen', 'Honeydew', 'Lawngreen', 'Chartreuse', 'Greenyellow', 'Darkolivegreen', 'Yellowgreen', 'Olivedrab', 'Yellow', 'Olive', 'Lightgoldenrodyellow', 'Lightyellow', 'Beige', 'Ivory', 'Darkkhaki', 'Palegoldenrod', 'Khaki', 'Lemonchiffon', 'Gold', 'Cornsilk', 'Goldenrod', 'Darkgoldenrod', 'Floralwhite', 'Oldlace', 'Wheat', 'Orange', 'Moccasin', 'Papayawhip', 'Blanchedalmond', 'Navajowhite', 'Antiquewhite', 'Tan', 'Burlywood', 'Darkorange', 'Bisque', 'Linen', 'Peru', 'Peachpuff', 'Sandybrown', 'Seashell', 'Saddlebrown', 'Chocolate', 'Sienna', 'Lightsalmon', 'Orangered', 'Coral', 'Darksalmon', 'Tomato', 'Salmon', 'Mistyrose', 'Red', 'Darkred', 'Maroon', 'Firebrick', 'Brown', 'Indianred', 'Lightcoral', 'Rosybrown', 'Snow', 'White', 'Whitesmoke', 'Gainsboro', 'Lightgray', 'Lightgrey', 'Silver', 'Darkgray', 'Darkgrey', 'Gray', 'Grey', 'Dimgray', 'Dimgrey', 'Black']
        self.colours_map = {
    "Aliceblue": (0.941, 0.973, 1.0, 1.0),
    "Antiquewhite": (0.980, 0.922, 0.843, 1.0),
    "Aqua": (0.0, 1.0, 1.0, 1.0),
    "Aquamarine": (0.498, 1.0, 0.831, 1.0),
    "Azure": (0.941, 1.0, 1.0, 1.0),
    "Beige": (0.961, 0.961, 0.863, 1.0),
    "Bisque": (1.0, 0.894, 0.769, 1.0),
    "Black": (0.0, 0.0, 0.0, 1.0),
    "Blanchedalmond": (1.0, 0.922, 0.804, 1.0),
    "Blue": (0.0, 0.0, 1.0, 1.0),
    "Blueviolet": (0.541, 0.169, 0.886, 1.0),
    "Brown": (0.647, 0.165, 0.165, 1.0),
    "Burlywood": (0.871, 0.722, 0.529, 1.0),
    "Cadetblue": (0.373, 0.620, 0.627, 1.0),
    "Chartreuse": (0.498, 1.0, 0.0, 1.0),
    "Chocolate": (0.824, 0.412, 0.118, 1.0),
    "Coral": (1.0, 0.498, 0.314, 1.0),
    "Cornflowerblue": (0.392, 0.584, 0.929, 1.0),
    "Cornsilk": (1.0, 0.973, 0.863, 1.0),
    "Crimson": (0.863, 0.078, 0.235, 1.0),
    "Cyan": (0.0, 1.0, 1.0, 1.0),
    "Darkblue": (0.0, 0.0, 0.545, 1.0),
    "Darkcyan": (0.0, 0.545, 0.545, 1.0),
    "Darkgoldenrod": (0.722, 0.525, 0.043, 1.0),
    "Darkgray": (0.663, 0.663, 0.663, 1.0),
    "Darkgrey": (0.663, 0.663, 0.663, 1.0),
    "Darkgreen": (0.0, 0.392, 0.0, 1.0),
    "Darkkhaki": (0.741, 0.718, 0.420, 1.0),
    "Darkmagenta": (0.545, 0.0, 0.545, 1.0),
    "Darkolivegreen": (0.333, 0.420, 0.184, 1.0),
    "Darkorange": (1.0, 0.549, 0.0, 1.0),
    "Darkorchid": (0.6, 0.196, 0.8, 1.0),
    "Darkred": (0.545, 0.0, 0.0, 1.0),
    "Darksalmon": (0.914, 0.588, 0.478, 1.0),
    "Darkseagreen": (0.561, 0.737, 0.561, 1.0),
    "Darkslateblue": (0.282, 0.239, 0.545, 1.0),
    "Darkslategray": (0.184, 0.310, 0.310, 1.0),
    "Darkslategrey": (0.184, 0.310, 0.310, 1.0),
    "Darkturquoise": (0.0, 0.808, 0.820, 1.0),
    "Darkviolet": (0.580, 0.0, 0.827, 1.0),
    "Deeppink": (1.0, 0.078, 0.576, 1.0),
    "Deepskyblue": (0.0, 0.749, 1.0, 1.0),
    "Dimgray": (0.412, 0.412, 0.412, 1.0),
    "Dimgrey": (0.412, 0.412, 0.412, 1.0),
    "Dodgerblue": (0.118, 0.565, 1.0, 1.0),
    "Firebrick": (0.698, 0.133, 0.133, 1.0),
    "Floralwhite": (1.0, 0.980, 0.941, 1.0),
    "Forestgreen": (0.133, 0.545, 0.133, 1.0),
    "Fuchsia": (1.0, 0.0, 1.0, 1.0),
    "Gainsboro": (0.863, 0.863, 0.863, 1.0),
    "Ghostwhite": (0.973, 0.973, 1.0, 1.0),
    "Gold": (1.0, 0.843, 0.0, 1.0),
    "Goldenrod": (0.855, 0.647, 0.125, 1.0),
    "Gray": (0.502, 0.502, 0.502, 1.0),
    "Grey": (0.502, 0.502, 0.502, 1.0),
    "Green": (0.0, 0.502, 0.0, 1.0),
    "Greenyellow": (0.678, 1.0, 0.184, 1.0),
    "Honeydew": (0.941, 1.0, 0.941, 1.0),
    "Hotpink": (1.0, 0.412, 0.706, 1.0),
    "Indianred": (0.804, 0.361, 0.361, 1.0),
    "Indigo": (0.294, 0.0, 0.510, 1.0),
    "Ivory": (1.0, 1.0, 0.941, 1.0),
    "Khaki": (0.941, 0.902, 0.549, 1.0),
    "Lavender": (0.902, 0.902, 0.980, 1.0),
    "Lavenderblush": (1.0, 0.941, 0.961, 1.0),
    "Lawngreen": (0.486, 0.988, 0.0, 1.0),
    "Lemonchiffon": (1.0, 0.980, 0.804, 1.0),
    "Lightblue": (0.678, 0.847, 0.902, 1.0),
    "Lightcoral": (0.941, 0.502, 0.502, 1.0),
    "Lightcyan": (0.878, 1.0, 1.0, 1.0),
    "Lightgoldenrodyellow": (0.980, 0.980, 0.824, 1.0),
    "Lightgreen": (0.565, 0.933, 0.565, 1.0),
    "Lightgray": (0.827, 0.827, 0.827, 1.0),
    "Lightgrey": (0.827, 0.827, 0.827, 1.0),
    "Lightpink": (1.0, 0.714, 0.757, 1.0),
    "Lightsalmon": (1.0, 0.627, 0.478, 1.0),
    "Lightseagreen": (0.125, 0.698, 0.667, 1.0),
    "Lightskyblue": (0.529, 0.808, 0.980, 1.0),
    "Lightslategray": (0.467, 0.533, 0.600, 1.0),
    "Lightslategrey": (0.467, 0.533, 0.600, 1.0),
    "Lightsteelblue": (0.690, 0.769, 0.871, 1.0),
    "Lightyellow": (1.0, 1.0, 0.878, 1.0),
    "Lime": (0.0, 1.0, 0.0, 1.0),
    "Limegreen": (0.196, 0.804, 0.196, 1.0),
    "Linen": (0.980, 0.941, 0.902, 1.0),
    "Magenta": (1.0, 0.0, 1.0, 1.0),
    "Maroon": (0.502, 0.0, 0.0, 1.0),
    "Mediumaquamarine": (0.400, 0.804, 0.667, 1.0),
    "Mediumblue": (0.0, 0.0, 0.804, 1.0),
    "Mediumorchid": (0.729, 0.333, 0.827, 1.0),
    "Mediumpurple": (0.576, 0.439, 0.859, 1.0),
    "Mediumseagreen": (0.235, 0.702, 0.443, 1.0),
    "Mediumslateblue": (0.482, 0.408, 0.933, 1.0),
    "Mediumspringgreen": (0.0, 0.980, 0.604, 1.0),
    "Mediumturquoise": (0.282, 0.820, 0.800, 1.0),
    "Mediumvioletred": (0.780, 0.082, 0.522, 1.0),
    "Midnightblue": (0.098, 0.098, 0.439, 1.0),
    "Mintcream": (0.961, 1.0, 0.980, 1.0),
    "Mistyrose": (1.0, 0.894, 0.882, 1.0),
    "Moccasin": (1.0, 0.894, 0.710, 1.0),
    "Navajowhite": (1.0, 0.871, 0.678, 1.0),
    "Navy": (0.0, 0.0, 0.502, 1.0),
    "Oldlace": (0.992, 0.961, 0.902, 1.0),
    "Olive": (0.502, 0.502, 0.0, 1.0),
    "Olivedrab": (0.420, 0.557, 0.137, 1.0),
    "Orange": (1.0, 0.647, 0.0, 1.0),
    "Orangered": (1.0, 0.271, 0.0, 1.0),
    "Orchid": (0.855, 0.439, 0.839, 1.0),
    "Palegoldenrod": (0.933, 0.910, 0.667, 1.0),
    "Palegreen": (0.596, 0.984, 0.596, 1.0),
    "Paleturquoise": (0.686, 0.933, 0.933, 1.0),
    "Palevioletred": (0.859, 0.439, 0.576, 1.0),
    "Papayawhip": (1.0, 0.937, 0.835, 1.0),
    "Peachpuff": (1.0, 0.855, 0.725, 1.0),
    "Peru": (0.804, 0.522, 0.247, 1.0),
    "Pink": (1.0, 0.753, 0.796, 1.0),
    "Plum": (0.867, 0.627, 0.867, 1.0),
    "Powderblue": (0.690, 0.878, 0.902, 1.0),
    "Purple": (0.502, 0.0, 0.502, 1.0),
    "Red": (1.0, 0.0, 0.0, 1.0),
    "Rosybrown": (0.737, 0.561, 0.561, 1.0),
    "Royalblue": (0.255, 0.412, 0.882, 1.0),
    "Saddlebrown": (0.545, 0.271, 0.075, 1.0),
    "Salmon": (0.980, 0.502, 0.447, 1.0),
    "Sandybrown": (0.957, 0.643, 0.376, 1.0),
    "Seagreen": (0.180, 0.545, 0.341, 1.0),
    "Seashell": (1.0, 0.961, 0.933, 1.0),
    "Sienna": (0.627, 0.322, 0.176, 1.0),
    "Silver": (0.753, 0.753, 0.753, 1.0),
    "Skyblue": (0.529, 0.808, 0.922, 1.0),
    "Slateblue": (0.416, 0.353, 0.804, 1.0),
    "Slategray": (0.439, 0.502, 0.565, 1.0),
    "Slategrey": (0.439, 0.502, 0.565, 1.0),
    "Snow": (1.0, 0.980, 0.980, 1.0),
    "Springgreen": (0.0, 1.0, 0.498, 1.0),
    "Steelblue": (0.275, 0.510, 0.706, 1.0),
    "Tan": (0.824, 0.706, 0.549, 1.0),
    "Teal": (0.0, 0.502, 0.502, 1.0),
    "Thistle": (0.847, 0.749, 0.847, 1.0),
    "Tomato": (1.0, 0.388, 0.278, 1.0),
    "Turquoise": (0.251, 0.878, 0.816, 1.0),
    "Violet": (0.933, 0.510, 0.933, 1.0),
    "Wheat": (0.961, 0.871, 0.702, 1.0),
    "White": (1.0, 1.0, 1.0, 1.0),
    "Whitesmoke": (0.961, 0.961, 0.961, 1.0),
    "Yellow": (1.0, 1.0, 0.0, 1.0),
    "Yellowgreen": (0.604, 0.804, 0.196, 1.0)}
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
        sm.add_widget(Themes(name="Themes"))
        sm.add_widget(Stats(name="Stats"))
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
        grid = self.get_widget("grid","Themes")
        for colour in self.colours:
            int = random.randint(0,3)
            card = Theme_Playing_Card(self.suits[int])
            #card.md_bg_color = colour.lower() Needs to be fixed!!!
            card.colour = colour
            card.change_colour()
            grid.add_widget(card)
        return super().on_start()
    
    def card_type(self,card):
        if card[1] == "S":
            suit = "cards-spade"
        elif card[1] == "D":
            suit = "cards-diamond"
        elif card[1] == "C":
            suit = "cards-club"
        elif card[1] == "H":
            suit = "cards-heart"
        if card[0] == "1":
            rank = "10"
        else:
            rank = card[0]
        return (suit,rank)
    
    def output_cards(self):
        widget = self.get_widget("test","InGame")
        widget.add_widget(Playing_Card(self.card_type("AH")))
        
#Running App
if __name__ == "__main__":
    GoFishApp().run()