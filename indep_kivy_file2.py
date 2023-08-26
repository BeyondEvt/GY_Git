from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class basic_video_window(FloatLayout):
    def __init__(self, text1=None, text2=None, **kwargs): # 设置两个参数text1，text2，默认为None
        super(basic_video_window, self).__init__(**kwargs)
        "以下四行均为演示参数的传递而使用，可删除"
        self.text1 = text1
        self.text2 = text2
        print(self.text1)
        print(self.text2)
        # “视频编号”标签和输入框
        self.add_widget(Label(text="视 频 编 号",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.23, "top": 0.62}))
        self.add_widget(TextInput(multiline=False,
                                  font_name='Font_Hanzi',
                                  size_hint=(0.3, 0.15),
                                  pos_hint={"x": 0.1, "top": 0.85}))
        # "视频名称"标签和输入框
        self.add_widget(Label(text="视 频 名 称",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.73, "top": 0.62}))
        self.add_widget(TextInput(multiline=False,
                                  font_name='Font_Hanzi',
                                  size_hint=(0.3, 0.15),
                                  pos_hint={"x": 0.6, "top": 0.85}))
        # "视频时长"标签和输入框
        self.add_widget(Label(text="视 频 时 长",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.23, "top": 0.21}))
        self.add_widget(TextInput(multiline=False,
                                  font_name='Font_Hanzi',
                                  size_hint=(0.3, 0.15),
                                  pos_hint={"x": 0.1, "top": 0.45}))
        # 窗口底部的提示标签
        self.add_widget(Label(text="(视频存储编号自定义且不可重复)",
                              font_name='Font_Hanzi',
                              size_hint=(0.03, 0.04),
                              pos_hint={"x": 0.49, "top": 0.10}))
        # “确认”按钮
        self.add_widget(Button(text="确 认",
                               font_name='Font_Hanzi',
                               background_color=(148 / 155, 242 / 155, 249 / 155),
                               size_hint=(0.3, 0.2),
                               pos_hint={"x": 0.6, "top": 0.45}))
        # 显示弹窗
        self.window = Popup(title="input the basic information of the video",
                            content=self,
                            size_hint=(None, None),
                            size=(500, 300))
        self.window.open()
        # 右上角关闭页面按钮
        self.add_widget(Button(text="×",
                               font_size=21,
                               background_color=[1, 0, 0, 1],
                               size_hint=(0.05, 0.05),
                               pos_hint={"x": 0.95, "top": 1},
                               on_press=self.window.dismiss))