import win32api
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer  ##引入控件
from kivy.factory import Factory
import subprocess
# 统一中文字体
LabelBase.register(name='Font_Hanzi', fn_regular='kvcn.ttc')  # 导入字体文件
Window.size = (1200, 900)

# ************************************************************************************
from opt import opt

from dataloader_webcam import WebcamLoader, DetectionLoader, DetectionProcessor, DataWriter, crop_from_dets, Mscoco
from yolo.darknet import Darknet
from yolo.util import write_results, dynamic_write_results
from SPPE.src.main_fast_inference import *

from SPPE.src.utils.img import im_to_torch
import sys
from tqdm import tqdm
from fn import getTime
import cv2
import time
from pPose_nms import write_json
from get_standard_data import *
import os

# 该文件为程序主界面文件，界面开发采用了kivy框架
# 结合了教练制定标准数据的功能和用户提取视频标准数据并开始人体识别的功能

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

# give_standard(0, 6, 7, 0, 0, 0, np.pi / 6, 0, 0, False, 0.0, 5, ["", "减小两肩的高低距离"])


# give_standard( 6, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 0.0, 1115.0, ["减小左小腿的最大角度","","增大左小腿的最大角度",""])
# give_standard( 8, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 0.0, 1115.00,["减小右小腿的最大角度","","增大右小腿的最大角度",""])
# give_standard(5, 0, 0, 0, 0, 0, np.pi/2, 0, np.pi/3, True, 5.0, 2110.0, ["减小左大腿的最大角度","1","增大左大腿的最大角度","2"])
# give_standard( 7, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 5.0, 2110.0, ["减小右大腿的最大角度","","增大右大腿的最大角度",""])
# get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
# get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
# get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
# get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
# **************************************************************************************
class VideoPlayerTest(BoxLayout):  ##布局类
    def __init__(self, **kwargs):  ##初始化
        super(VideoPlayerTest, self).__init__(**kwargs)

        player = VideoPlayer(source='video1.mp4', state='play', options={'allow_stretch': True, 'eos': 'loop'})
        self.add_widget(player)



class VideoPlayerApp(App):  ##实现App类的build()方法（继承自App类）
    def build(self):
        return VideoPlayerTest()  ##返回根控件



class UserInput(TextInput):  # 一个基类为TextInput的类


    def __init__(self, **kwargs):
        super(UserInput, self).__init__(**kwargs)


class ExeMainWindow(App):  # app主窗口界面
    def build(self):
        self.layout = FloatLayout()
        # 打开教练输入标准数据的窗口界面的按钮
        self.input_button = Button(text = "录入标准数据",
                                   font_name='kvcn.ttc',
                                   font_size = 18,
                                   background_color=[148 / 155, 242 / 155, 249 / 155],
                                   size_hint = (0.15,0.1),
                                   pos_hint = {"x": 0.1, "top":0.8}
                                   )
        self.layout.add_widget(self.input_button)
        self.input_button.bind(on_press = self.Input_num_Window)

        # 用户开始的按钮
        self.start_button = Button(text="开 始",
                                   font_name='kvcn.ttc',
                                   font_size=18 ,
                                   background_color=[148 / 155, 242 / 155, 249 / 155],
                                   size_hint=(0.15, 0.1),
                                   pos_hint={"x": 0.1, "top": 0.6}
                                   )


        self.layout.add_widget(self.start_button)
        self.start_button.bind(on_press=self.SelectVideo_window)
        return self.layout




    def Input_num_Window(self, button):  # 教练输入视频基础参数的的窗口
        layout = FloatLayout()
        self.num = UserInput(multiline=False,
                             font_name='Font_Hanzi',
                              size_hint=(0.3, 0.15),
                              pos_hint={"x": 0.1, "top": 0.85})
        layout.add_widget(self.num)
        self.Vname = UserInput(multiline=False,
                               font_name='Font_Hanzi',
                              size_hint=(0.3, 0.15),
                              pos_hint={"x": 0.6, "top": 0.85})
        layout.add_widget(self.Vname)
        self.Vtime = UserInput(multiline=False,
                              size_hint=(0.3, 0.15),
                              pos_hint={"x": 0.1, "top": 0.45})
        layout.add_widget(self.Vtime)

        layout.add_widget(Label(text="视 频 编 号",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.23, "top": 0.62}))
        layout.add_widget(Label(text="视 频 名 称",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.73, "top": 0.62}))
        layout.add_widget(Label(text="视 频 时 长",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.23, "top": 0.21}))
        layout.add_widget(Label(text="(视频存储编号自定义且不可重复)",
                                font_name='Font_Hanzi',
                                size_hint=(0.03, 0.04),
                                pos_hint={"x": 0.49, "top": 0.10}))

        confirm_button = Button(text="确 认",
                                           font_name='Font_Hanzi',
                                           background_color=(148 / 155, 242 / 155, 249 / 155),
                                           size_hint=(0.3, 0.2),
                                           pos_hint={"x": 0.6, "top": 0.45}
                                           )
        layout.add_widget(confirm_button)

        confirm_button.bind(on_press=self.Input_Window)

        closeButton = Button(text="×",
                             font_size=21,
                             background_color=[1, 0, 0, 1],
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.95, "top": 1})

        layout.add_widget(closeButton)
        popup = Popup(title="Input The Data Number",
                      content=layout,
                      size_hint=(None, None),
                      size=(500, 300))
        popup.open()
        closeButton.bind(on_press=popup.dismiss)


    # 用户选择视频的界面
    def SelectVideo_window(self, button):  # 教练输入视频基础参数的的窗口
        layout = FloatLayout()


        # 输入选择视频的id
        self.video_id = UserInput(multiline=False,
                             size_hint=(0.15, 0.04),
                             pos_hint={"x": 0.75, "top": 0.85})
        layout.add_widget(self.video_id)

        # 确认并开始视频
        confirm_button = Button(text="确 认",
                                           font_name='Font_Hanzi',
                                           background_color=(148 / 155, 242 / 155, 249 / 155),
                                           size_hint=(0.15, 0.04),
                                           pos_hint={"x": 0.75, "top": 0.8}
                                           )
        layout.add_widget(confirm_button)


        confirm_button.bind(on_press=self.webcam_start2)


        closeButton = Button(text="×",
                             font_size=21,
                             background_color=[1, 0, 0, 1],
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.95, "top": 1})

        layout.add_widget(closeButton)
        popup = Popup(title="Input The Data Number",
                      content=layout,
                      size_hint=(None, None),
                      size=(1080, 900)
                      )
        popup.open()
        closeButton.bind(on_press=popup.dismiss)


        layout.add_widget(Label(text="请 输 入 视 频 编 号",
                                font_name='Font_Hanzi',
                                size_hint=(0.15, 0.04),
                                pos_hint={"x": 0.75, "top": 0.9}))

        layout.add_widget(Label(text="视 频 编 号：",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.1, "top": 0.95}))
        layout.add_widget(Label(text="视 频 名 称",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.4, "top": 0.95}))
        for i in range(len(video_id)):
            layout.add_widget(Label(text=video_id[i],
                                    font_name='Font_Hanzi',
                                    size_hint=(0.045, 0.05),
                                    pos_hint={"x": 0.1, "top": 0.95-(i+1)*0.03}))
        for i in range(len(video_name)):
            layout.add_widget(Label(text=video_name[i],
                                    font_name='Font_Hanzi',
                                    size_hint=(0.045, 0.05),
                                    pos_hint={"x": 0.4, "top": 0.95-(i+1)*0.03}))



    def Input_Window(self, button):  # 教练输入标准数据的窗口
        layout = FloatLayout()

        VIDEO_data_num = VIDEO_data2()[0::3]

        if (self.num.text.strip() == '' or self.num.text is  None) or (self.Vname.text.strip() == '' or self.Vname.text
                is  None) or (self.Vtime.text.strip() == '' or self.Vtime.text is  None):
            layout.add_widget(Label(text="视频信息不能为空，请重新填写！",
                                    font_name='Font_Hanzi',
                                    size_hint=(0.045, 0.05),
                                    pos_hint={"x": 0.5, "top": 0.5}))
            closeButton = Button(text="×",
                                 font_size=21,
                                 background_color=[1, 0, 0, 1],
                                 size_hint=(0.05, 0.05),
                                 pos_hint={"x": 0.95, "top": 1})
            layout.add_widget(closeButton)
            # 设置弹窗的属性
            popup = Popup(title="Error",
                          content=layout,
                          size_hint=(None, None),
                          size=(300, 240))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)  # 关闭按钮绑定关闭popup窗口的功能


        else:

            if self.num.text not in VIDEO_data_num:             # 对其进行查找
                # 将视频基础参数存入数据库
                insert_mysql3(self.num.text, self.Vname.text, self.Vtime.text)
                self.line = UserInput(multiline=False,
                                      size_hint=(0.05, 0.05),
                                      pos_hint={"x": 0.05, "top": 0.9})
                layout.add_widget(self.line)
                self.pt1 = UserInput(multiline=False,
                                     size_hint=(0.05, 0.05),
                                     pos_hint={"x": 0.12, "top": 0.9})
                layout.add_widget(self.pt1)
                self.pt2 = UserInput(multiline=False,
                                     size_hint=(0.05, 0.05),
                                     pos_hint={"x": 0.19, "top": 0.9})
                layout.add_widget(self.pt2)
                self.line1 = UserInput(multiline=False,
                                       size_hint=(0.05, 0.05),
                                       pos_hint={"x": 0.26, "top": 0.9})
                layout.add_widget(self.line1)
                self.line2 = UserInput(multiline=False,
                                       size_hint=(0.05, 0.05),
                                       pos_hint={"x": 0.33, "top": 0.9})
                layout.add_widget(self.line2)
                self.min_angle_down = UserInput(multiline=False,
                                                size_hint=(0.05, 0.05),
                                                pos_hint={"x": 0.40, "top": 0.9})
                layout.add_widget(self.min_angle_down)
                self.max_angle_up = UserInput(multiline=False,
                                              size_hint=(0.05, 0.05),
                                              pos_hint={"x": 0.47, "top": 0.9})
                layout.add_widget(self.max_angle_up)
                self.min_angle_up = UserInput(multiline=False,
                                              size_hint=(0.05, 0.05),
                                              pos_hint={"x": 0.54, "top": 0.9})
                layout.add_widget(self.min_angle_up)
                self.max_angle_down = UserInput(multiline=False,
                                                size_hint=(0.05, 0.05),
                                                pos_hint={"x": 0.61, "top": 0.9})
                layout.add_widget(self.max_angle_down)
                self.line_is_move = UserInput(multiline=False,
                                              size_hint=(0.05, 0.05),
                                              pos_hint={"x": 0.68, "top": 0.9})
                layout.add_widget(self.line_is_move)
                self.time_start = UserInput(multiline=False,
                                            size_hint=(0.05, 0.05),
                                            pos_hint={"x": 0.75, "top": 0.9})
                layout.add_widget(self.time_start)
                self.time_end = UserInput(multiline=False,
                                          size_hint=(0.05, 0.05),
                                          pos_hint={"x": 0.82, "top": 0.9})
                layout.add_widget(self.time_end)
                self.tips = UserInput(multiline=False,
                                    font_name='Font_Hanzi',
                                      size_hint=(0.7, 0.05),
                                      pos_hint={"x": 0.05, "top": 0.8})
                layout.add_widget(self.tips)


                save_in_mysql_button = Button(text="保 存",
                                                   font_name='Font_Hanzi',
                                                   background_color=(148 / 155, 242 / 155, 249 / 155),
                                                   size_hint=(0.05, 0.05),
                                                   pos_hint={"x": 0.77, "top": 0.8}
                                                   )
                layout.add_widget(save_in_mysql_button)
                save_in_mysql_button.bind(on_press=self.save_data_in_mysql)

                save_over_button = Button(text="结 束",
                                              font_name='Font_Hanzi',
                                              background_color=(148 / 155, 242 / 155, 249 / 155),
                                              size_hint=(0.05, 0.05),
                                              pos_hint={"x": 0.83, "top": 0.8}
                                              )
                layout.add_widget(save_over_button)
                save_over_button.bind(on_press=self.save_over)


                closeButton = Button(text="×",
                                     font_size = 21,
                                     background_color=[1, 0, 0, 1],
                                     size_hint = (0.05,0.05),
                                     pos_hint = {"x": 0.95, "top": 1})


                layout.add_widget(closeButton)
                popup = Popup(title="Save In Standard Data Window",
                              content=layout,
                              size_hint=(None, None),
                              size=(1000, 800))
                popup.open()
                closeButton.bind(on_press=(popup.dismiss))

                layout.add_widget(Label(text = "line", size_hint = (0.05, 0.05), pos_hint = {"x": 0.05, "top": 0.95}))
                layout.add_widget(Label(text = "pt1", size_hint = (0.05, 0.05), pos_hint = {"x": 0.12, "top": 0.95}))
                layout.add_widget(Label(text = "pt2", size_hint = (0.05, 0.05), pos_hint = {"x": 0.19, "top": 0.95}))
                layout.add_widget(Label(text = "line1", size_hint = (0.05, 0.05), pos_hint = {"x": 0.26, "top": 0.95}))
                layout.add_widget(Label(text = "line2", size_hint = (0.05, 0.05), pos_hint = {"x": 0.33, "top": 0.95}))
                layout.add_widget(Label(text = "min_d", size_hint = (0.05, 0.05), pos_hint = {"x": 0.40, "top": 0.95}))
                layout.add_widget(Label(text = "max_u", size_hint = (0.05, 0.05), pos_hint = {"x": 0.47, "top": 0.95}))
                layout.add_widget(Label(text = "min_u", size_hint = (0.05, 0.05), pos_hint = {"x": 0.54, "top": 0.95}))
                layout.add_widget(Label(text = "max_d", size_hint = (0.05, 0.05), pos_hint = {"x": 0.61, "top": 0.95}))
                layout.add_widget(Label(text = "move", size_hint = (0.05, 0.05), pos_hint = {"x": 0.68, "top": 0.95}))
                layout.add_widget(Label(text = "start", size_hint = (0.05, 0.05), pos_hint = {"x": 0.75, "top": 0.95}))
                layout.add_widget(Label(text = "end", size_hint = (0.05, 0.05), pos_hint = {"x": 0.82, "top": 0.95}))
                layout.add_widget(Label(text = "tips", size_hint = (0.05, 0.05), pos_hint = {"x": 0.05, "top": 0.85}))
                layout.add_widget(Label(text = "line", size_hint = (0.05, 0.05), pos_hint = {"x": 0.05, "top": 0.95}))
                layout.add_widget(Label(text = "line", size_hint = (0.05, 0.05), pos_hint = {"x": 0.05, "top": 0.95}))

            else: # 若视频编号已存在
                self.num.text = ''
                self.Vtime.text = ''
                self.Vname.text = ''
                layout.add_widget(Label(text="该编号已存在",
                                        font_name='Font_Hanzi',
                                        size_hint=(0.045, 0.05),
                                        pos_hint={"x": 0.5, "top": 0.5}))
                closeButton = Button(text="×",
                                     font_size=21,
                                     background_color=[1, 0, 0, 1],
                                     size_hint=(0.05, 0.05),
                                     pos_hint={"x": 0.95, "top": 1})
                layout.add_widget(closeButton)
                # 设置弹窗的属性
                popup = Popup(title="Error",
                              content=layout,
                              size_hint=(None, None),
                              size=(300, 240))
                popup.open()
                closeButton.bind(on_press=popup.dismiss)  # 关闭按钮绑定关闭popup窗口的功能

    def save_over(self,_):
        self.num.text = ''
        self.Vtime.text = ''
        self.Vname.text = ''



    def save_data_in_mysql(self,_):
        if (self.num.text.strip() != '' or self.num.text is not None) and (
                self.line.text.strip() != '' or self.line.text is not None)and (
                self.pt1.text.strip() != '' or self.pt1.text is not None)and (
                self.pt2.text.strip() != '' or self.pt2.text is not None)and (
                self.line1.text.strip() != '' or self.line1.text is not None)and (
                self.line2.text.strip() != '' or self.line2.text is not None)and (
                self.min_angle_down.text.strip() != '' or self.min_angle_down.text is not None)and (
                self.max_angle_up.text.strip() != '' or self.max_angle_up.text is not None)and (
                self.min_angle_up.text.strip() != '' or self.min_angle_up.text is not None)and (
                self.max_angle_down.text.strip() != '' or self.max_angle_down.text is not None)and (
                self.line_is_move.text.strip() != '' or self.line_is_move.text is not None)and (
                self.time_start.text.strip() != '' or self.time_start.text is not None)and (
                self.time_end.text.strip() != '' or self.time_end.text is not None)and (
                self.tips.text.strip() != '' or self.tips.text is not None):


            insert_mysql2(self.num.text, self.line.text,self.pt1.text, self.pt2.text, self.line1.text, self.line2.text,
                self.min_angle_down.text, self.max_angle_up.text, self.min_angle_up.text, self.max_angle_down.text,
                self.line_is_move.text, self.time_start.text, self.time_end.text, self.tips.text)
            self.line.text=''
            self.pt1.text=''
            self.pt2.text=''
            self.line1.text=''
            self.line2.text=''
            self.min_angle_down.text=''
            self.max_angle_up.text=''
            self.min_angle_up.text=''
            self.max_angle_down.text=''
            self.line_is_move.text=''
            self.time_start.text=''
            self.time_end.text=''
            self.tips.text=''

    def webcam_start2(self, button):
        #
        import json

        videoid = self.video_id.text
        video_file = videoid+".mp4"
        print(video_file)
        # video_name = video_play_data[video_play_data.index(videoid) + 1 ]
        video_time = float(video_play_data[video_play_data.index(videoid) + 2 ])

        # 生成数据字典
        data_dict = dict()
        data_sql=[]
        for i in range(len(data_sql_data)):
            if data_sql_data[i][0] == self.video_id.text:
                data_sql.append(data_sql_data[i])
        print("这是data_sql",data_sql)
        for i in range(len(data_sql)):
            index = str("%.1f" % (int(data_sql[i][-3])))
            if index not in data_dict:
                data_dict[index] = []
            print("data_sql[i][1]",data_sql[i][1],type(data_sql[i][1]))
            if int(data_sql[i][1]) != 0:
                data_dict[index].append(
                    [2, int(data_sql[i][1]), int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]),
                     int(data_sql[i][5]),
                     float(data_sql[i][6]), float(data_sql[i][7]), float(data_sql[i][8]), float(data_sql[i][9]),
                     bool(int(data_sql[i][10])),
                     float("%.1f" % (int(data_sql[i][12]))), data_sql[i][13].split(sep='-')])


            elif int(data_sql[i][1]) == 0 and data_sql[i][2] != 0 and data_sql[i][3] != 0:
                data_dict[index].append(
                    [1, int(data_sql[i][1]), int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]),
                     int(data_sql[i][5]),
                     float(data_sql[i][6]), float(data_sql[i][7]), float(data_sql[i][8]), float(data_sql[i][9]),
                     bool(int(data_sql[i][10])),
                     float("%.1f" % (int(data_sql[i][12]))), data_sql[i][13].split(sep='-')])
            elif int(data_sql[i][4]) != 0 and data_sql[i][5] != 0:
                data_dict[index].append(
                    [3, int(data_sql[i][1]), int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]),
                     int(data_sql[i][5]),
                     float(data_sql[i][6]), float(data_sql[i][7]), float(data_sql[i][8]), float(data_sql[i][9]),
                     bool(int(data_sql[i][10])),
                     float("%.1f" % (int(data_sql[i][12]))), data_sql[i][13].split(sep='-')])

        print("这是data_dict", data_dict)
        with open("dict.json", "w") as f:
            json_dict = json.dumps([data_dict, video_file, video_time])
            f.write(json_dict)

        from subprocess import Popen, PIPE, STDOUT

        p = Popen([sys.executable, "webcam_demo.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

if __name__ == '__main__':
    ExeMainWindow().run()




