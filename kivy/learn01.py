from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color,Ellipse,Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

# Window.size = (400, 300)
# print(Metrics.density)

class MyApp(App):

    # def build(self): # 创建画布
    #     w = Widget()
    #     with w.canvas:
    #         Color(0,0,1,1)
    #         Rectangle(pos=(100,100),size=[100,100])
    #         Ellipse(pos=(300,300),size=[200,200])
    #
    #
    # def build2(self): # FloatLayout布局
    #     layout = FloatLayout()
    #     btn = Button(text="Click me", size_hint_max=("400dp", "300dp"))
    #     layout.add_widget(btn)
    #     return layout


    def build(self): # BoxLayout()布局
        layout = BoxLayout(orientation="vertical")
        title_bar = BoxLayout(size_hint_max_y = "30dp")

        # layout.add_widget(Button(text="Button1"))
        # layout.add_widget(Button(text="Button2"))
        title_bar.add_widget(Button(text="Button1"))
        title_bar.add_widget(Button(text="Button2"))
        layout.add_widget(title_bar)
        layout.add_widget(TextInput(text="Hello World"))
        return layout


if __name__ == '__main__':
    MyApp().run()