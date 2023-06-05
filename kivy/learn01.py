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

# #: import Factory kivy.factory.Factory
#
# <MyPopup@Popup>:
# 	auto_dismiss:False
# 	title:'Hello Popup'
# 	on_dismiss:print('on_dismiss is running')
# 	on_open:print('on_open is running')
# 	size_hint:.8,.8
#
# 	AnchorLayout:
# 		anchor_x:'center'
# 		anchor_y:'bottom'
# 		Button:
# 			text:'Close Popup'
# 			size_hint:None,None
# 			size:100,100
# 			on_release:root.dismiss()
# Button:
# text: 'Login'
# size_hint_max: ("100dp", "40dp")
# pos: (120, 30)
# color: (0, 0, 0, 1)
# background_color: (1, 0.5, 0.7, 0.95)
# on_release: Factory.MyPopup().open()
