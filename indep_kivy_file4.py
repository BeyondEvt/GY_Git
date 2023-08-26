from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class saved_video_window(GridLayout):
    def __init__(self):
        super(saved_video_window, self).__init__()
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 40
        self.window = Popup(title="select your video",
                            content=self,
                            size_hint=(None, None),
                            size=(900, 700))
        self.window.open()
        # 第一行
        self.add_widget(Label(text="已存在的视频",
                              font_name='Font_Hanzi'))
        # 右上角关闭页面按钮
        self.add_widget(Button(text="×",
                               font_size=21,
                               background_color=[1, 0, 0, 1],
                               on_press=self.window.dismiss))
        # 第二行
        self.add_widget(Label(text="视频名称",
                              font_name='Font_Hanzi'))
        self.add_widget(Label(text="视频时长",
                              font_name='Font_Hanzi'))
        # 获取video相关数据
        from MySql.connect_sql import VIDEO_data # 详细数据
        from MySql.connect_sql import VIDEO_data2 # 基础数据
        video_basic_data = VIDEO_data2()
        video_name = video_basic_data[0::2]
        video_time = video_basic_data[1::2]
        # 罗列所有视频
        for i in range(len(video_name)):
            self.add_widget(Label(text=video_name[i],
                                  font_name='Font_Hanzi'))
            self.add_widget(Label(text=video_time[i],
                                  font_name='Font_Hanzi'))
        self.add_widget(Label(text=''))
        self.add_widget(Label(text=''))
        self.Vname1 = TextInput(multiline=False,
                                hint_text='请输入要编辑的视频编号',
                                font_name='Font_Hanzi')
        self.add_widget(self.Vname1)
        self.Vname2 = TextInput(multiline=False,
                                hint_text='请输入要删除的视频编号',
                                font_name='Font_Hanzi')
        self.add_widget(self.Vname2)
        self.add_widget(Button(text='编辑',
                               font_name='Font_Hanzi',
                               background_color=[148 / 155, 242 / 155, 249 / 155]))
        self.add_widget(Button(text="删除",
                               font_name='Font_Hanzi',
                               background_color=[1, 0, 0, 1],
                               )) # on_press还未设置
        self.add_widget(Button(text="新建",
                               font_name='Font_Hanzi',
                               background_color=[148 / 155, 242 / 155, 249 / 155],
                               on_press=self.input_num_window))
        self.add_widget(Button(text="刷新",
                               font_name='Font_Hanzi',
                               background_color=[148 / 155, 242 / 155, 249 / 155],
                               on_press=self.refresh))

    # 用于前往"input_num_window"页面
    def input_num_window(self, *args):
        from indep_kivy_file2 import input_num_window
        self.root = input_num_window()

    def delete(self, key, *args):
        from MySql.connect_sql import delete_VIDEO_data2
        print(key)
        delete_VIDEO_data2(key)
        self.root = saved_video_window()
        self.window.dismiss()

    def refresh(self, *args):
        self.root = saved_video_window()
        self.window.dismiss()