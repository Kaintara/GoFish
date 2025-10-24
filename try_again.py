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