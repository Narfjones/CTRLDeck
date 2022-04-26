import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
import kivy.properties as prop
from kivy.vector import Vector
from kivy.clock import Clock


class Fader(Widget):
    velocity_x = prop.NumericProperty(0)
    velocity_y = prop.NumericProperty(0)
    velocity = prop.ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class CTRLdeck(Widget):
    pass


class CTRLdeckApp(App):
    def build(self):
        return CTRLdeck()


if __name__ == '__main__':
    CTRLdeckApp().run()