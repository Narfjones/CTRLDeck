import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import kivy.properties as prop
from kivy.vector import Vector
from kivy.clock import Clock


class Buttons(GridLayout):
    pass

class Boxes(GridLayout):
    pass
"""    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b13 = Button(text="F13")
        b14 = Button(text="F14")
        b15 = Button(text="F15")
        b16 = Button(text="F16")
        b17 = Button(text="F17")
        b18 = Button(text="F18")
        b19 = Button(text="F19")
        b20 = Button(text="F20")
        b21 = Button(text="F21")
        b22 = Button(text="F22")
        b23 = Button(text="F23")
        b24 = Button(text="F24")
        self.add_widget(b13)
        self.add_widget(b14)
        self.add_widget(b15)
        self.add_widget(b16)
        self.add_widget(b17)
        self.add_widget(b18)
        self.add_widget(b19)
        self.add_widget(b20)
        self.add_widget(b21)
        self.add_widget(b22)
        self.add_widget(b23)
        self.add_widget(b24)
"""

class CTRLdeck(Widget):
    pass


class CTRLdeckApp(App):
    def build(self):
        return Boxes()


if __name__ == '__main__':
    CTRLdeckApp().run()