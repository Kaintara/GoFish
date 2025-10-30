#Imports

from math import sin, cos, radians
import time
import random
from Game import Game

#Kivy
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale, Translate
from kivy.clock import Clock


#KivyMD
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon, MDIconButton, MDButtonText
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogIcon, MDDialogContentContainer, MDDialogSupportingText


#Custom Buttons/Cards
class HandLayout(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(width=self.update_spacing, children=self.update_spacing)

    def update_spacing(self, *args):
        n = len(self.children)
        if n <= 1:
            self.spacing = 0
        else:
            required = n * dp(64)
            avail = self.width
            desired = (avail - required) / (n - 1)
            max_overlap = -dp(64) * 0.75   
            max_spread = dp(64) * 0.5 
            if desired < max_overlap:
                desired = max_overlap
            elif desired > max_spread:
                desired = max_spread
            self.spacing = desired

class Playing_Card_Back(MDCard): #Back of the Playing Cards
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.layout = FitImage(
            size = ("64dp", "89dp"),
            source = "Card_Back.png",
        )
        self.add_widget(self.layout)

class Theme_Playing_Card(MDCard): #Playing Cards for the theme menu only
    def __init__(self,suit="",**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.suit = suit
        self.bind(on_release = lambda x:app.change_theme(self.colour)) #Changes the theme of the UI when this card is clicked
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
    def change_colour(self): #Changes the Colour of the different theme cards
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

class Card_Label(MDLabel): #Rotates the text on the playing cards
     def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rotate = Rotate(angle=180, origin=self.center)
        with self.canvas.after:
            PopMatrix()
            
class Playing_Card(MDCard): #Actual playing card for gameplay
    def __init__(self,suit_rank,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.suit = suit_rank[0]
        self.rank = suit_rank[1]
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
            font_size = dp(30),
            adaptive_size= True
        )
        self.down_text = Card_Label(
            pos_hint= {"top":1.1, "center_x":0.8},
            text= self.rank,
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
        self.highlight = FitImage(
            source='glow.png',
            size_hint=(1.2,1.2),
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.layout.add_widget(self.highlight)
        self.layout.add_widget(self.icon)
        self.layout.add_widget(self.up_text)
        self.layout.add_widget(self.down_text)
        self.add_widget(self.layout)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            if app.player_turn:
                if app.selected_card != self:
                    if app.selected_card:
                        app.selected_card.highlight.opacity = 0
                        app.selected_card = self
                    else:
                        app.selected_card = self
                    app.selected_rank = self.rank
                    app.selected = True
                    self.highlight.opacity = 1
                else:
                    app.selected_rank = ''
                    app.selected = False
                    self.highlight.opacity = 0
        return super().on_touch_down(touch)


class Deck_Cards(RelativeLayout):
    def __init__(self,suit_rank,**kwargs):
        super().__init__(**kwargs)
        self.card = suit_rank
        self.size_hint = (None,None)
        self.size = (dp(64),dp(89))
        self.pos_hint = {"center_x": 0.5, "center_y":0.5}
        self.card_front = Playing_Card(self.card)
        self.card_back = Playing_Card_Back()
        self.buffer = Playing_Card_Back()
        self.add_widget(self.buffer)
        self.add_widget(self.card_front)
        self.add_widget(self.card_back)
        self.remove_widget(self.buffer)
        self.is_front_visible = False


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            g = app.game_instance
            if app.player_draw:
                parent = self.parent
                parent.remove_widget(self)
                parent.add_widget(self, index=0)
                self.flip()
        return super().on_touch_down(touch)


    def flip(self, *args):
        if getattr(self, "_is_animating", False):
            return
        self._is_animating = True
        original_width = self.width

        anim1 = Animation(width=0, duration=0.2, t="out_quad")
        anim2 = Animation(width=original_width, duration=0.2, t="out_quad")

        def halfway_callback(*_):
            self.clear_widgets()
            if self.is_front_visible:
                self.add_widget(self.card_back)
            else:
                self.add_widget(self.card_front)
            self.is_front_visible = not self.is_front_visible

        def finish_callback(*_):
            self._is_animating = False

        anim1.bind(on_complete=lambda *_: halfway_callback())
        anim2.bind(on_complete=lambda *_: finish_callback())

        (anim1 + anim2).start(self)

        app = MDApp.get_running_app()
        g = app.game_instance
        try:
            g.shuffled_deck.remove(app.suit_rank(self.card))
        except:
            print(f"Apparently {g.shuffled_deck} doesn't have {app.suit_rank(self.card)}")
        g.hands[g.turn].append(app.suit_rank(self.card))
        g.check_for_sets()
        g.history.append((f'player{g.turn + 1}',g.hands[g.turn][-1],'draw'))
        g.Update_GameState()
        g.turn = g.next_vaild_player(g.turn)
        app.player_draw = False
        app.update_widgets()
        app.end_player_turn()

    def rotate(self, *args):
        with self.canvas.before:
            PushMatrix()
            self.angle = random.randint(0,360)
            self.rotate = Rotate(angle=self.angle, origin=self.center)
        with self.canvas.after:
            PopMatrix()
 

class Bot_Icon(MDCard):
    def __init__(self,name,playernum,**kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        g = app.game_instance
        self.id = name
        self.player = playernum
        self.size = (dp(100),dp(100))
        self.size_hint = (None, None)
        self.radius = [dp(75)]
        self.padding = (0, 0, 0, 0)
        self.label = MDLabel(
            text=f"B{name[3]}",
            halign="center",
            valign="middle",
            font_style = "cataway",
            size=self.size,
            size_hint=(None, None),
            theme_font_size = "Custom",
            font_size = dp(40),
            text_size=self.size,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            g = app.game_instance
            if app.selected and app.players[g.turn] != self.id:
                if app.selected_rank == "10":
                    app.selected_rank = "1"
                move = (self.player,app.selected_rank,'ask') 
                print(move)
                self.md_bg_color = app.theme_cls.inversePrimaryColor   
                moves = g.game_turn_player(move)
                if not moves:
                    app.player_turn = False        
                    if g.shuffled_deck:
                        app.player_draw = True
                    else:
                        g.Update_GameState()
                        g.turn = g.next_vaild_player(g.turn)
                        app.update_widgets()
                        app.end_player_turn()
                app.update_widgets()
                app.selected_rank = ''
                app.selected_card = None
                app.selected = False
            else:
                g = app.game_instance
                MDDialog(MDDialogIcon(icon="account-circle"),
            MDDialogHeadlineText(
                text=self.id,
                halign="center",
                font_style= "cataway",
                role="medium",
            ),
            MDDialogSupportingText(
                text=f"- Set Count: {len(g.state["sets"][self.player])}\n- No. of Cards in Hand: {len(g.state["hands"][self.player])}",
                halign="left",
                font_style= "cataway",
                theme_font_size = "Custom",
                font_size = dp(20),
                markup = True,
            )).open()
        return super().on_touch_down(touch)
    
    def highlight(self):
        app = MDApp.get_running_app()
        anim = Animation(md_bg_color=app.theme_cls.inversePrimaryColor, duration=2)
        anim.start(self)


class Player_Icon(MDCard): #How to ask for cards.
    def __init__(self,name,playernum,**kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        g = app.game_instance
        self.turn = False
        self.id = name
        self.player = playernum
        self.size = (dp(100),dp(100))
        self.size_hint = (None, None)
        self.radius = [dp(75)]
        self.padding = (0, 0, 0, 0)
        self.label = MDLabel(
            text=f"{name[0]}",
            halign="center",
            valign="middle",
            font_style = "cataway",
            size=self.size,
            size_hint=(None, None),
            theme_font_size = "Custom",
            font_size = dp(40),
            text_size=self.size,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            g = app.game_instance
            if app.selected and app.players[g.turn] != self.id and app.current_player_view != self.id:
                move = (self.player,app.selected_rank,'ask') 
                self.md_bg_color = app.theme_cls.inversePrimaryColor   
                moves = g.game_turn_player(move)
                if not moves:
                    app.player_turn = False        
                    app.player_draw = True
                app.update_widgets()
                app.selected_rank = ''
                app.selected_card = None
                app.selected = False
            else:
                MDDialog(MDDialogIcon(icon="account-circle"),
            MDDialogHeadlineText(
                text=self.id,
                halign="center",
                font_style= "cataway",
                role="medium",
            ),
            MDDialogSupportingText(
                text=f"- Set Count: {len(g.state["sets"][self.player])}\n- No. of Cards in Hand: {len(g.state["hands"][self.player])}",
                halign="left",
                font_style= "cataway",
                theme_font_size = "Custom",
                font_size = dp(20),
                markup = True,
            )).open()
            return super().on_touch_down(touch)
    
    def highlight(self):
        app = MDApp.get_running_app()
        anim = Animation(md_bg_color=app.theme_cls.inversePrimaryColor, duration=2)
        anim.start(self)

        

#Screens
class SM(MDScreenManager):
    pass

class MainMenu(MDScreen):
    pass

class NewGame(MDScreen):
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
        self.game_instance = None
        self.sm_stack = [] #Stack that stores what screens the player has been to go back
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
        self.playerandbots = []
        self.players = []
        self.player_turn = False
        self.player_draw = False
        self.player_num_map = {}
        self.selected_rank = ''
        self.selected_card = None
        self.selected = False
        self.current_player_view = ''
        self.player_widget_map = {}
        self.dialog = ''
        self.the_player = ''
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
        sm.add_widget(NewGame(name="NewGame"))
        sm.add_widget(InGame(name="InGame"))
        sm.add_widget(Rules(name="Rules"))
        sm.add_widget(Settings(name="Settings"))
        sm.add_widget(Themes(name="Themes"))
        sm.add_widget(Stats(name="Stats"))
        sm.current = "Menu"
        return sm
    
    #Function to get the widget instance from a particular screen
    def get_widget(self, widget, screen):
        return self.root.get_screen(screen).ids[widget]
    
    def get_runtime_widget(self, widget):
        if hasattr(self, "player_widget_map") and widget in self.player_widget_map:
            return self.player_widget_map[widget]
        try:
            screen = self.root.get_screen("InGame")
        except Exception:
            return None
        for child in screen.walk():
            # match by id or name string
            if getattr(child, "id", None) == widget or getattr(child, "name", None) == widget:
                return child
        return None
    
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

    def switch_icon(self,widget): #Switches the Dark/Light Mode icon based on which mode is selected
        if widget.name == "light":
            widget.icon = "weather-night"
            widget.name = "dark"
        else:
            widget.name = "light"
            widget.icon = "white-balance-sunny"
        
    def change_theme(self,colour): #Changes the main colour theme
        self.theme_cls.primary_palette = colour

    def on_start(self): #When the app starts this is run, preloads the theme section
        grid = self.get_widget("grid","Themes")
        for colour in self.colours:
            int = random.randint(0,3)
            card = Theme_Playing_Card(self.suits[int])
            card.colour = colour
            card.change_colour()
            grid.add_widget(card)
        return super().on_start()
    
    def card_type(self,card): #Coverts cards to icon names for making playing cards
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
    
    def suit_rank(self,card):
        if card[0] == "cards-spade":
            suit = "S"
        elif card[0] == "cards-diamond":
            suit = "D"
        elif card[0] == "cards-club":
            suit = "C"
        elif card[0] == "cards-heart":
            suit = "H"
        if card[1] == "10":
            rank = "1"
        else:
            rank = card[1]
        return f"{rank}{suit}"
    
    def left(self): #Goes left in the carousel
        Carou = self.get_widget("loop","Settings")
        Carou.load_previous()

    def right(self): #Goes right in the carousel
        Carou = self.get_widget("loop","Settings")
        Carou.load_next()

    def assign_player_num(self): #Gives each player a player name which is used frequently in the Game.py code
        g = self.game_instance
        for i in range(g.amount_of_players):
            try:
                self.player_num_map[self.players[i]] = f"player{i+1}"
            except:
                self.player_num_map[f"Bot{(i-(g.amount_of_players-g.amount_of_bots-1))}"] = f"player{i+1}"

    def output_deck(self): #Outputs all the cards in the deck into the middle of the screen
        g = self.game_instance
        widget = self.get_widget("deck","InGame")
        for card in g.shuffled_deck:
            Card = Deck_Cards(self.card_type(card))
            Card.pos_hint = {"center_x":(random.randint(0,100) / 100),"center_y":(random.randint(0,100) / 100)} 
            Card.rotate()
            widget.add_widget(Card)
    
    def output_players(self): #Outputs all the player & bot icons around the deck
        g = self.game_instance
        angle_step = 180 / (g.amount_of_players-1)
        for player in range(g.amount_of_players-g.amount_of_bots):
            angle = radians(player * angle_step)
            center_x = 0.5 + 0.4 * cos(angle)
            center_y = 0.5 + 0.4 * sin(angle)
            if self.players[player] == self.current_player_view:
                contain = self.get_widget("playerview","InGame")
                Player = Player_Icon(self.players[player],self.player_num_map[self.players[player]])
                Player.pos_hint = {"center_x": center_x,"center_y": center_y}
                Player.id = self.players[player]
                contain.add_widget(Player)
                self.player_widget_map[Player.id] = Player
            else:
                display = self.root.get_screen("InGame")
                Player = Player_Icon(self.players[player],self.player_num_map[self.players[player]])
                Player.id = self.players[player]
                Player.pos_hint = {"center_x": 0.2,"center_y":0.5}
                display.add_widget(Player)
                self.player_widget_map[Player.id] = Player
            
        for bot in range(g.amount_of_bots):
            angle = radians((bot + ((g.amount_of_players-g.amount_of_bots)-1)) * angle_step)
            center_x = 0.5 + 0.35 * cos(angle)
            center_y = 0.5 + 0.35 * sin(angle)
            display = self.root.get_screen("InGame")
            Bot = Bot_Icon(f"Bot{bot + 1}",self.player_num_map[f"Bot{bot + 1}"])
            Bot.id = f"Bot{bot + 1}"
            Bot.pos_hint = {"center_x": center_x,"center_y": center_y}
            display.add_widget(Bot)
            self.player_widget_map[Bot.id] = Bot

    def deal_cards(self): #Deals hand cards to the current player view
        g = self.game_instance
        hand = self.get_widget("hand","InGame")
        g.Update_GameState()
        for card in g.hands[self.players.index(self.current_player_view)]:
            Card = Playing_Card(self.card_type(card))
            hand.add_widget(Card)

    def determine_turn_dialog(self):
        g = self.game_instance
        print("Dialog Text:", g.dialog_text, "The player:", self.the_player)
        Correct = any(i[2] == 'took' for i in g.dialog_text)
        if Correct:
            title = f"{self.the_player} was successful!"
            text = ''
            for i in range(len(g.dialog_text)):
                notes = f"- Asked for {g.dialog_text[i][1]}s\n"
                if notes not in text:
                    text += notes
        else:
            title = f"{self.the_player} was unsuccessful!"
            text = f"- Asked for {g.dialog_text[0][1]}s"
        g.dialog_text = []
        self.the_player = ''
        self.dialog = [title,text]

    def close_turn_dialog(self):
        if hasattr(self, "turn_dialog") and self.turn_dialog:
            self.turn_dialog.dismiss()
            self.turn_dialog = None
            Clock.schedule_once(self.next_turn, 0.5)

    def show_turn_dialog(self):
        if hasattr(self, "turn_dialog") and self.turn_dialog:
            self.turn_dialog.dismiss()

        self.determine_turn_dialog()
        self.turn_dialog = MDDialog(
            MDDialogIcon(icon="script-text-outline"),
            MDDialogHeadlineText(text=self.dialog[0],
                halign="center",
                font_style= "cataway",
                role="medium",),
            MDDialogSupportingText(text=self.dialog[1],
                halign="left",
                font_style= "cataway",
                theme_font_size = "Custom",
                font_size = dp(20),
                markup = True,),
                MDDialogButtonContainer(MDButton(
                    MDButtonText(text="Got it!", font_style = "cataway", role = "small"),
                    MDButtonIcon(icon="check-outline"),
                    style = "tonal",
                    pos_hint = {"center_x":0.5},
                    on_release = lambda x:self.close_turn_dialog()
                )),
            auto_dismiss = False
        )
        self.turn_dialog.open()

    def make_move(self,icon):
        g = self.game_instance
        if isinstance(icon,Bot_Icon):
            print(g.state)
            self.the_player = self.playerandbots[g.turn]
            Carou = self.get_widget("loop","Settings")
            difficulty = Carou.current_slide.text
            if difficulty == "Beginner":
                g.game_turn_bot(g.beginner_call())
                self.update_widgets()
            elif difficulty == "Easy":
                g.game_turn_bot(g.easy_call())
                self.update_widgets()
            elif difficulty == "Medium":
                g.game_turn_bot(g.medium_call())
                self.update_widgets()
            elif difficulty == "Hard":
                g.game_turn_bot(g.hard_call())
                self.update_widgets()
            elif difficulty == "Expert":
                g.game_turn_bot(g.expert_call())
                self.update_widgets()
            g.Update_GameState()
            self.show_turn_dialog()
        else:
            moves = g.get_valid_moves(self.players.index(self.current_player_view))
            if not moves:
                self.player_draw = True
            else:
                self.player_turn = True
            return None

    def update_widgets(self):
        dis = self.get_widget("deck","InGame")
        hand = self.get_widget("hand","InGame")
        dis.clear_widgets()
        hand.clear_widgets()
        self.deal_cards()
        self.output_deck()

    def end_player_turn(self):
        g = self.game_instance
        g.Update_GameState()
        Clock.schedule_once(self.next_turn, 0.5)

    def go_to_menu(self, *args):
        self.game_over_dialog.dismiss()
        self.root.current = "Menu"

    def game_over(self):
        g = self.game_instance
        dialog_text = ''
        max = ['player',0]
        for i, s in enumerate(g.sets):
            dialog_text += (f"{self.playerandbots[i]} got {len(s)} sets.\n")
            size = len(s)
            if max[1] < size:
                max = [self.playerandbots[i],size]
        self.game_over_dialog = MDDialog(
            MDDialogIcon(icon="crown"),
            MDDialogHeadlineText(text=f"Game Over! {max[0]} won!",
                halign="center",
                font_style= "cataway",
                role="medium",),
            MDDialogSupportingText(text=dialog_text,
                halign="left",
                font_style= "cataway",
                theme_font_size = "Custom",
                font_size = dp(20),
                markup = True,),
                MDDialogButtonContainer(MDButton(
                    MDButtonText(text="Good Game!", font_style = "cataway", role = "small"),
                    MDButtonIcon(icon="check-outline"),
                    style = "tonal",
                    pos_hint = {"center_x":0.5},
                    on_release = lambda x:self.go_to_menu()
                )),
            auto_dismiss = False
        )
        self.game_over_dialog.open()

    def next_turn(self, *args):
        g = self.game_instance
        if g.is_game_over() or not g.hands[0]:
            print("Game Over!")
            self.game_over()
            return
        elif g.turn == None:
            print("no Vaild player LOL")
        
        print(f"Turn {g.turn} — {self.playerandbots[g.turn]}")
        
        icon = self.get_runtime_widget(self.playerandbots[g.turn])
        icon.highlight()
        self.make_move(icon)

    def game_loop_solo(self):
        print("Game Started!")
        g = self.game_instance
        g.turn = random.randint(0,len(self.playerandbots) - 1)
        self.next_turn()

    def multi(self):
        self.multi_dialog = MDDialog(
            MDDialogIcon(icon="script-text-outline"),
            MDDialogHeadlineText(text="Not Available :( ",
                halign="center",
                font_style= "cataway",
                role="medium",),
            MDDialogSupportingText(text="This is my first version so at the moment the game is only playable with bots... Not pass and play sorry :(",
                halign="left",
                font_style= "cataway",
                theme_font_size = "Custom",
                font_size = dp(20),
                markup = True,),
                MDDialogButtonContainer(MDButton(
                    MDButtonText(text="It's okay, I understand", font_style = "cataway", role = "small"),
                    MDButtonIcon(icon="check-outline"),
                    style = "tonal",
                    pos_hint = {"center_x":0.5},
                    on_release = lambda x:self.go_to_menu()
                )),
            auto_dismiss = False
        )
        self.multi_dialog.open()

    def solo(self):
        self.current_player_view = self.players[0]
        g = self.game_instance
        g.shuffle_cards()
        g.distribute_cards()
        g.check_for_sets()
        g.sort_cards()
        self.output_deck()
        self.assign_player_num()
        g.Update_GameState()
        self.output_players()
        self.deal_cards()
        print(g.state)
        self.game_loop_solo()
        

    def start(self): #Starts the game
        if len(self.players) == 1:
            self.game_instance = Game(4,3)
            self.playerandbots = [self.players[0],"Bot1","Bot2","Bot3"]
            self.solo()
        elif len(self.players) < 4:
            self.game_instance = Game(4,(4-len(self.players)))
            for x in self.players:
                self.playerandbots.append(x)
            for i in range(4-len(self.players)):
                self.playerandbots.append(f"Bot{i+1}")
            self.multi()
        else:
            self.game_instance = Game(len(self.players),0)
            self.playerandbots = self.players
            self.multi()
    
    def remove(self,widget): #Removes the name of the player if it is incorrect/they are not playing etc..
        player = self.get_widget('Players','NewGame')
        self.players.remove(widget.children[1].text)
        player.remove_widget(widget)

    def all_players(self,instance): #Outputs the name inputted w/ a remove button if needed
        name = instance.text.strip()
        if not name:
            return
        player = self.get_widget('Players','NewGame')
        entry_box = MDBoxLayout(size_hint_y=None, height="40dp")
        label = MDLabel(text=name, halign="center")
        removebtn = MDIconButton(icon="close",on_release=lambda x: self.remove(entry_box))
        entry_box.add_widget(label)
        entry_box.add_widget(removebtn)
        player.add_widget(entry_box, index=0)
        self.players.append(name)
        
        
#Running App
if __name__ == "__main__":
    GoFishApp().run()