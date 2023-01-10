# main.py
import MySQLdb
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.button import Button

Window.size = (500, 300) # 窗口大小
Builder.load_string('''
<FloatLayout>
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            source: 'BorderImage.png'
                    
            pos: (0, 0)
            size: (500, 300)      

''')

class RegisterLoginWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(RegisterLoginWindow, self).__init__(**kwargs)
        # with self.canvas:
        #     Color(0,0,1,1)
        self.pos = (0,0)
        self.add_widget(Label(text='User Name', size_hint_max=("100dp", "50dp"), pos=(95,110), texture_size = (10,10), color = (0,0,0,1))) # 用户名输入框标签
        self.user_name = TextInput(multiline = False, size_hint_max=("200dp", "30dp"), pos=(200,120))
        self.add_widget(self.user_name)          # 用户名输入框
        self.add_widget(Label(text='Password', size_hint_max=("100dp", "50dp"), pos=(95,70), color = (0,0,0,1))) # 密码输入框标签
        self.user_password = TextInput(password = True,  multiline = False, size_hint_max=("200dp", "30dp"), pos=(200,80))
        self.add_widget(self.user_password)          # 密码输入框
        self.add_widget(Button(text='Login', size_hint_max=("100dp", "40dp"), pos=(120,30), color = (0,0,0,1),
                               background_color = (1, 0.5, 0.7, 0.95)))
        self.add_widget(Button(text='Register', size_hint_max=("100dp", "40dp"), pos=(280, 30), color=(0, 0, 0, 1),
                               background_color = (1, 0.5, 0.7, 0.95)))
class MyApp(App):
    def build(self):
        return RegisterLoginWindow()



if __name__ == '__main__':
    MyApp().run()
