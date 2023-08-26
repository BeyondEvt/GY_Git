from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class save_basic_data_window(FloatLayout):
    def __init__(self, _, **kwargs):
        super(save_basic_data_window, self).__init__(**kwargs)
        # “视频名称”标签和输入框
        self.add_widget(Label(text="视 频 名 称",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.23, "top": 0.62}))
        self.Vname = TextInput(multiline=False,
                               font_name='Font_Hanzi',
                               size_hint=(0.3, 0.15),
                               pos_hint={"x": 0.1, "top": 0.85})
        self.add_widget(self.Vname) # 此处Vname输入框必须分开写，不然会影响后续的插入操作
        # "视频时长"标签和输入框
        self.add_widget(Label(text="视 频 时 长",
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.73, "top": 0.62}))
        self.Vtime = TextInput(multiline=False,
                               font_name='Font_Hanzi',
                               size_hint=(0.3, 0.15),
                               pos_hint={"x": 0.6, "top": 0.85})
        self.add_widget(self.Vtime) # 此处Vtime输入框必须分开写，不然会影响后续的插入操作
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
                               pos_hint={"x": 0.6, "top": 0.45},
                               on_press=self.insert))
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
    def insert(self, *args):
        from MySql.connect_sql import insert_mysql3
        # 获取video相关数据
        from MySql.connect_sql import VIDEO_data2
        video_play_data = VIDEO_data2()
        video_id = video_play_data[0::2]
        video_name = video_play_data[1::2]
        print(video_name)
        print(self.Vname.text)
        if self.Vname.text not in video_name:
            print("here")
            insert_mysql3(self.Vname.text, self.Vtime.text)
            self.window.dismiss()
        else:
            from Exception_Popup import Exception_Pupup
            Exception_Pupup("视频编号已存在")
            self.Vname.text = ''
            self.Vtime.text = ''