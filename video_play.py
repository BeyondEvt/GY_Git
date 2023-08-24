from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer  ##引入控件
from kivy.clock import Clock
from MySql.connect_mysql import VIDEO_data2
# 该文件用来打开训练的标准视频

video_play_data = VIDEO_data2()

import json

with open("dict.json", 'r+') as f:
	res_list = json.load(f)
video_name = res_list[1]
end_time = res_list[2]
print(res_list)

class VideoPlayerTest(BoxLayout):  ##布局类
    def __init__(self, **kwargs):  ##初始化
        super(VideoPlayerTest, self).__init__(**kwargs)

        player = VideoPlayer(source=res_list[1], state='play', options={'allow_stretch': True, 'eos': 'loop'})
        print(res_list)
        self.add_widget(player)


class VideoPlayerApp(App):  ##实现App类的build()方法（继承自App类）
    def build(self):
        return VideoPlayerTest()  ##返回根控件


Clock.schedule_once(App().get_running_app().stop, end_time+2)
from kivy.core.window import Window

Window.clearcolor = [.8, .8, .8, 1]
VideoPlayerApp().run()  ##启动应用程序
