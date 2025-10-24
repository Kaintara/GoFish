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