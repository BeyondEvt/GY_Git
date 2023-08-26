from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class video_start_window(FloatLayout):
    def __init__(self, _, **kwargs):
        super(video_start_window, self).__init__(**kwargs)
        # “请输入视频编号”标签和输入框
        self.add_widget(Label(text="请 输 入 视 频 编 号",
                              font_name='Font_Hanzi',
                              size_hint=(0.15, 0.04),
                              pos_hint={"x": 0.75, "top": 0.9}))
        self.add_widget(TextInput(multiline=False,
                                  size_hint=(0.15, 0.04),
                                  pos_hint={"x": 0.75, "top": 0.85}))
        # “确认”按钮
        self.add_widget(Button(text="确 认",
                               font_name='Font_Hanzi',
                               background_color=(148 / 155, 242 / 155, 249 / 155),
                               size_hint=(0.15, 0.04),
                               pos_hint={"x": 0.75, "top": 0.8}
                               )) # 此处缺少on_press=
        # 左侧“视频编号”和“视频名称”标签
        self.add_widget(Label(text="视 频 编 号：",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.1, "top": 0.95}))
        self.add_widget(Label(text="视 频 名 称",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.4, "top": 0.95}))
        # 左侧“视频编号”和“视频名称”标签
        self.add_widget(Label(text="视 频 编 号：",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.1, "top": 0.95}))
        self.add_widget(Label(text="视 频 名 称",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.4, "top": 0.95}))
        # 获取video相关数据
        from MySql.connect_sql import VIDEO_data2
        video_play_data = VIDEO_data2()
        video_id = video_play_data[0::2]
        video_name = video_play_data[1::2]
        # 罗列所有视频
        for i in range(len(video_id)):
            self.add_widget(Label(text=video_id[i],
                                  font_name='Font_Hanzi',
                                  size_hint=(0.045, 0.05),
                                  pos_hint={"x": 0.1, "top": 0.95 - (i + 1) * 0.03}))
            self.add_widget(Label(text=video_name[i],
                                  font_name='Font_Hanzi',
                                  size_hint=(0.045, 0.05),
                                  pos_hint={"x": 0.4, "top": 0.95 - (i + 1) * 0.03}))

        # 显示弹窗
        self.window = Popup(title="select your video",
                            content=self,
                            size_hint=(None, None),
                            size=(880, 700))
        self.window.open()
        # 右上角关闭页面按钮
        self.add_widget(Button(text="×",
                               font_size=21,
                               background_color=[1, 0, 0, 1],
                               size_hint=(0.05, 0.05),
                               pos_hint={"x": 0.95, "top": 1},
                               on_press=self.window.dismiss))