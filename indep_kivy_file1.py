from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix import widget
from kivy.graphics import Color, Rectangle
from indep_kivy_file2 import basic_video_window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer  ##引入控件
# 统一中文字体
LabelBase.register(name='Font_Hanzi', fn_regular='kvcn.ttc')  # 导入字体文件
Window.size = (900, 700)
from opt import opt
import sys
# 获取视频基础数据
from MySql.connect_mysql import VIDEO_data2
video_play_data = VIDEO_data2()


video_id = video_play_data[0::3]
video_name = video_play_data[1::3]

from dict_base import *

args = opt
args.dataset = 'coco'
q = []  # (存放30帧实时数据)
L = []  # 存放已执行函数

list_father = []
class main_window(FloatLayout):
    def __init__(self, **kwargs):
        super(main_window, self).__init__(**kwargs)
        # "录入标准数据"按钮
        self.add_widget(Button
                        (text="录 入 标 准 数 据",
                         font_name='kvcn.ttc',
                         font_size=18,
                         background_color=[148 / 155, 242 / 155, 249 / 155],
                         size_hint=(0.17, 0.1),
                         pos_hint={"x": 0.1, "top": 0.8},
                         on_press=self.basic_video_window))
        # "选择视频"按钮
        self.add_widget(Button(text="选 择 视 频",
                               font_name='kvcn.ttc',
                               font_size=18,
                               background_color=[148 / 155, 242 / 155, 249 / 155],
                               size_hint=(0.17, 0.1),
                               pos_hint={"x": 0.1, "top": 0.6}))
    # 用于前往"basic_video_window"页面
    def basic_video_window(self, *args):
        self.root = basic_video_window(1, 2) # 此处1 2仅供参数传递测试使用，可删除

class main_App(App):
    def __init__(self, **kwargs):
        super(main_App, self).__init__(**kwargs)
        self.root = main_window()
        self.title = "主页面"


if __name__ == '__main__':
    main_App().run()
