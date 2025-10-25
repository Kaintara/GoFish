'''
class Settings_Btn(RotateBehavior, MDBoxLayout):
    pass


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

'''

''''
MDLabel:
                    text: "J"
                    pos_hint: {"y":1, "x":0}
                    font_style: "cataway"
                    role: "small"
                MDLabel:
                    pos_hint: {"x":1,"y":0}
                    text: "J"
                    font_style: "cataway"
                    role: "small"
                    halign: "right"
                    valign: "bottom"
                    canvas.before:
                        PushMatrix
                        Rotate:
                            angle: 180
                            origin: self.center
                    canvas.after:
                        PopMatrix
'''
from matplotlib import colors

colours = ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet', 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral', 'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan', 'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta', 'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen', 'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet', 'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick', 'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink', 'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen', 'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow', 'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen', 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow', 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue', 'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen', 'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose', 'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange', 'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred', 'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']
colours_map = {
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


def hsv_sort(color_name): #To sort the colours 
            r, g, b, a = colours_map[color_name]
            h, s, v = colors.rgb_to_hsv((r, g, b))
            return (h, s, v)

sorted_colours = sorted(colours, key=hsv_sort,reverse=True)

print(sorted_colours)