# from  PIL import ImageColor
# # print(ImageColor.getcolor('black', 'RGB'))
# # main.py
import MySQLdb
from kivy.app import App
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
from kivy.factory import Factory

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
import os
import sys
from tqdm import tqdm
import time
from fn import getTime
import cv2
import time
from pPose_nms import write_json
from standard_data import *
from get_standard_data import *
# **************************************************************************************





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
        self.input_button.bind(on_press = self.Input_Window)

        # 用户开始的按钮
        self.start_button = Button(text="开 始",
                                   font_name='kvcn.ttc',
                                   font_size=18 ,
                                   background_color=[148 / 155, 242 / 155, 249 / 155],
                                   size_hint=(0.15, 0.1),
                                   pos_hint={"x": 0.1, "top": 0.6}
                                   )


        self.layout.add_widget(self.start_button)
        self.start_button.bind(on_press=self.webcam_start)
        return self.layout





    def Input_Window(self, button):  # 教练输入标准数据的窗口
        layout = FloatLayout()

        line = UserInput(multiline=False,
                              size_hint=(0.05, 0.05),
                              pos_hint={"x": 0.05, "top": 0.9})
        layout.add_widget(line)
        pt1 = UserInput(multiline=False,
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.12, "top": 0.9})
        layout.add_widget(pt1)
        pt2 = UserInput(multiline=False,
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.19, "top": 0.9})
        layout.add_widget(pt2)
        line1 = UserInput(multiline=False,
                               size_hint=(0.05, 0.05),
                               pos_hint={"x": 0.26, "top": 0.9})
        layout.add_widget(line1)
        line2 = UserInput(multiline=False,
                               size_hint=(0.05, 0.05),
                               pos_hint={"x": 0.33, "top": 0.9})
        layout.add_widget(line2)
        min_angle_down = UserInput(multiline=False,
                                        size_hint=(0.05, 0.05),
                                        pos_hint={"x": 0.40, "top": 0.9})
        layout.add_widget(min_angle_down)
        max_angle_up = UserInput(multiline=False,
                                      size_hint=(0.05, 0.05),
                                      pos_hint={"x": 0.47, "top": 0.9})
        layout.add_widget(max_angle_up)
        min_angle_up = UserInput(multiline=False,
                                      size_hint=(0.05, 0.05),
                                      pos_hint={"x": 0.54, "top": 0.9})
        layout.add_widget(min_angle_up)
        max_angle_down = UserInput(multiline=False,
                                        size_hint=(0.05, 0.05),
                                        pos_hint={"x": 0.61, "top": 0.9})
        layout.add_widget(max_angle_down)
        line_is_move = UserInput(multiline=False,
                                      size_hint=(0.05, 0.05),
                                      pos_hint={"x": 0.68, "top": 0.9})
        layout.add_widget(line_is_move)
        time_start = UserInput(multiline=False,
                                    size_hint=(0.05, 0.05),
                                    pos_hint={"x": 0.75, "top": 0.9})
        layout.add_widget(time_start)
        time_end = UserInput(multiline=False,
                                  size_hint=(0.05, 0.05),
                                  pos_hint={"x": 0.82, "top": 0.9})
        layout.add_widget(time_end)
        tips = UserInput(multiline=False,
                         font_name='Font_Hanzi',
                              size_hint=(0.7, 0.05),
                              pos_hint={"x": 0.05, "top": 0.8})
        layout.add_widget(tips)

        save_in_mysql_button = Button(text="保 存",
                                           font_name='Font_Hanzi',
                                           background_color=(148 / 155, 242 / 155, 249 / 155),
                                           size_hint=(0.1, 0.06),
                                           pos_hint={"x": 0.77, "top": 0.8}
                                           )
        layout.add_widget(save_in_mysql_button)


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
        closeButton.bind(on_press=popup.dismiss)

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

    def webcam_start(self, button):
        args = opt
        args.dataset = 'coco'
        q = []  # (存放30帧实时数据)
        L = []  # 存放已执行函数

        list_father = []

        give_standard(0, 6, 7, 0, 0, 0, np.pi / 6, 0, 0, False, 0.0, 1115.0, ["", "减小两肩的高低距离"])
        # give_standard( 6, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 0.0, 1115.0, ["减小左小腿的最大角度","","增大左小腿的最大角度",""])
        # give_standard( 8, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 0.0, 1115.00,["减小右小腿的最大角度","","增大右小腿的最大角度",""])
        # give_standard(5, 0, 0, 0, 0, 0, np.pi/2, 0, np.pi/3, True, 5.0, 2110.0, ["减小左大腿的最大角度","1","增大左大腿的最大角度","2"])
        # give_standard( 7, 0, 0, 0, 0, 0, np.pi/3, 0, 0, 5.0, 2110.0, ["减小右大腿的最大角度","","增大右大腿的最大角度",""])
        # get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
        # get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
        # get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)
        # get_standard.give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end)

        count = 0
        for item in func_dict.keys():
            for j in range(len(func_dict[item])):
                list_father.append([])

        def loop():
            n = 0
            while True:
                yield n
                n += 1

        if __name__ == "__main__":
            webcam = args.webcam
            mode = args.mode
            if not os.path.exists(args.outputpath):
                os.mkdir(args.outputpath)

            # Load input video
            data_loader = WebcamLoader(webcam).start()
            (fourcc, fps, frameSize) = data_loader.videoinfo()  # fourcc: 22, fps: 30.0, frameSize: (640, 480)

            # Load detection loader
            print('Loading YOLO model..')
            sys.stdout.flush()
            det_loader = DetectionLoader(data_loader, batchSize=args.detbatch).start()
            det_processor = DetectionProcessor(det_loader).start()

            # Load pose model
            pose_dataset = Mscoco()
            if args.fast_inference:
                pose_model = InferenNet_fast(4 * 1 + 1, pose_dataset)
            else:
                pose_model = InferenNet(4 * 1 + 1, pose_dataset)
            pose_model.cuda()
            pose_model.eval()

            # Data writer
            save_path = os.path.join(args.outputpath, 'AlphaPose_webcam' + webcam + '.avi')
            # save_path: examples/res\AlphaPose_webcam0.avi
            writer = DataWriter(args.save_video, save_path, cv2.VideoWriter_fourcc(*'XVID'), fps, frameSize).start()

            runtime_profile = {
                'dt': [],
                'pt': [],
                'pn': []
            }

            print('Starting webcam demo, press Ctrl + C to terminate...')
            sys.stdout.flush()
            im_names_desc = tqdm(loop())
            batchSize = args.posebatch

            # 计时器开始
            start_0 = time.time()
            start = start_0

            for i in im_names_desc:
                try:
                    start_time = getTime()
                    with torch.no_grad():
                        (inps, orig_img, im_name, boxes, scores, pt1, pt2) = det_processor.read()
                        """
                        im_name: 100.jpg
                        boxes: tensor([[1, 2, 3, 4]])
                        scores: tensor([0.9907])  靠近1
                        pt1: tensor([1, 2]) boxes的前两位
                        pt2: tensor([3, 4]) boxes的后两位
                        """
                        # print("This is inps", inps)
                        # print("This is orig_img", orig_img)
                        if boxes is None or boxes.nelement() == 0:
                            writer.save(None, None, None, None, None, orig_img, im_name.split('/')[-1])
                            continue

                        ckpt_time, det_time = getTime(start_time)
                        # print('This is ckpt_time', ckpt_time)
                        # print('This is det_time', det_time)
                        runtime_profile['dt'].append(det_time)
                        # Pose Estimation

                        datalen = inps.size(0)
                        leftover = 0
                        if datalen % batchSize:
                            leftover = 1
                        num_batches = datalen // batchSize + leftover
                        hm = []
                        for j in range(num_batches):
                            inps_j = inps[j * batchSize:min((j + 1) * batchSize, datalen)].cuda()
                            hm_j = pose_model(inps_j)
                            hm.append(hm_j)
                        hm = torch.cat(hm)
                        ckpt_time, pose_time = getTime(ckpt_time)
                        runtime_profile['pt'].append(pose_time)

                        hm = hm.cpu().data
                        writer.save(boxes, scores, hm, pt1, pt2, orig_img, im_name.split('/')[-1])

                        ckpt_time, post_time = getTime(ckpt_time)
                        runtime_profile['pn'].append(post_time)

                        while (writer.running2()):
                            pass
                        time.sleep(0.02)
                        result_ = writer.results()
                        writer.__init__()

                        if len(result_) == 1:
                            keypoints = result_[-1]['result'][0]['keypoints']
                            point_6 = keypoints[5].numpy()
                            point_8 = keypoints[7].numpy()
                            point_10 = keypoints[9].numpy()
                            vector_up = point_6 - point_8
                            vector_down = point_10 - point_8
                            angle_ = np.dot(vector_up, vector_down) / \
                                     (np.linalg.norm(vector_up) * np.linalg.norm(vector_down))
                            angle_land = np.dot(vector_up, [0, -1]) / \
                                         (np.linalg.norm(vector_up))

                            standard_num = -1 / 2

                            # 存储规定时间段内的函数
                            now = time.time()
                            if str(np.floor(now - start_0)) in func_dict:
                                for i in range(len(func_dict[str(np.floor(now - start_0))])):
                                    L.append(func_dict[str(np.floor(now - start_0))][i])
                                del func_dict[str(np.floor(now - start_0))]

                            option = standard_func(keypoints)
                            # 执行函数
                            for i in range(len(L)):
                                if L[i][0] == 1:
                                    option.point_angle(L[i][2], L[i][3], L[i][6], L[i][7], L[i][-1], list_father[i])

                                if L[i][0] == 2:
                                    option.line_angle(L[i][1], L[i][6], L[i][7], L[i][8], L[i][9], L[i][-4],
                                                      L[i][-1], list_father[i])

                                if L[i][0] == 3:
                                    option.lines_angle(L[i][4], L[i][5], L[i][6], L[i][7], L[i][-1], list_father[i])

                            # print(L)
                            # 结束函数
                            pop_list = []  # 临时存放要pop的函数
                            for i in range(len(L)):
                                if (now - start_0) >= L[i][-2]:
                                    pop_list.append(i)

                            pop_list = pop_list[::-1]  # 将要pop的函数序号颠倒，避免列表长度减少导致索引出错

                            for i in pop_list:
                                L.pop(i)  # 将不再执行的命令pop出L
                                list_father.pop(i)

                    # ************************************* ********************
                    #                     option1 = standard_data(keypoints)
                    #                     option1.point_angle(7, 6,0, np.pi/6,q)
                    # *********************************************************

                    # option2 = standard_data(keypoints)
                    # option2.line_angle(1,3, np.pi/6, np.pi/3, q )
                    # ***********************************************************

                    # ### 正面左手下方
                    # # 左手外侧
                    # if vector_up[0] < 0:
                    #     if np.arccos(angle_land) - np.arccos(standard_num) > np.pi/18:
                    #         print("左手向外角度适当减小")
                    #         index = 1
                    #     elif np.arccos(angle_land) - np.arccos(standard_num) < -np.pi/18:
                    #         print("左手向外角度适当增大")
                    #         index = 2
                    #     else:
                    #         print("ok")
                    #         index = 3
                    # # 左手内侧
                    # if vector_up[0] >= 0:
                    #     if np.arccos(angle_land) - np.arccos(standard_num) > np.pi/18:
                    #         print("左手往外伸")
                    #         index = 4
                    #     elif np.arccos(angle_land) - np.arccos(standard_num) < -np.pi/18:
                    #         print("左手往里收")
                    #         index = 5
                    #     else:
                    #         print("ok")
                    #         index = 6
                    #
                    # ## 动态评估---区间来回变化(与上下标准比较)
                    #
                    # if len(q) < 30:
                    #     q.append(index)
                    #
                    # if len(q) == 30:
                    #     q.pop(0)
                    #     q.append(index)
                    #
                    # std_down_side = True # 外侧
                    # std_down_value = 0.5 # cos值
                    # ## 与下标准比较
                    # # 判断幅度是否过大
                    # # 下标准在外侧
                    # if std_down_side:
                    #     if q.count(2) >= 8:
                    #         print("左手摆动下幅度减小*****************************************")
                    #         q.__init__()
                    #
                    # # 判断幅度是否过小
                    # if len(q) == 30:
                    #      if q.count(3) <= 5:
                    #         print("左手摆动下幅度增大￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥")
                    #         q.__init__()
                    #

                    # 最大角和最小角的评估

                    #     else:
                    #         print("直角")
                    #     if abs(angle_land - 0) > 0.2:
                    #         print("手臂不够平")
                    #
                    #
                    # if abs(angle_ - 0) > 0.2:
                    #     print("你的手臂不是直角")
                    # else:
                    #     print("直角")
                    # if abs(angle_land - 0) > 0.2:
                    #     print("手臂不够平")

                    # ***************************************************************************************************************************
                    # writer2 = DataWriter(args.save_video, save_path, cv2.VideoWriter_fourcc(*'XVID'), fps, frameSize).start()
                    # if boxes is None or boxes.nelement() == 0:
                    #     writer2.save(None, None, None, None, None, orig_img, im_name.split('/')[-1])
                    #     continue
                    # writer2.save(boxes, scores, hm, pt1, pt2, orig_img, im_name.split('/')[-1])
                    # while (writer2.running2()):
                    #     pass
                    # writer2.stop()
                    # final = writer2.results()
                    # # print(final)
                    # keypoints = final[0]['result'][0]['keypoints']
                    # point_6 = keypoints[5].numpy()
                    # point_8 = keypoints[7].numpy()
                    # point_10 = keypoints[9].numpy()
                    # vector_up = point_6 - point_8
                    # vector_down = point_10 - point_8
                    # angle_ = np.dot(vector_up, vector_down)/ \
                    #          (np.linalg.norm(vector_up) * np.linalg.norm(vector_down))
                    # angle_land = np.dot(vector_up, [0, 1])/ \
                    #          (np.linalg.norm(vector_up))
                    # if abs(angle_ - 0) > 0.2:
                    #     print("你的手臂不是直角")
                    # else:
                    #     print("直角")
                    # if abs(angle_land - 0) > 0.2:
                    #     print("手臂不够平")

                    if args.profile:
                        # TQDM
                        im_names_desc.set_description(
                            'det time: {dt:.3f} | pose time: {pt:.2f} | post processing: {pn:.4f}'.format(
                                dt=np.mean(runtime_profile['dt']), pt=np.mean(runtime_profile['pt']),
                                pn=np.mean(runtime_profile['pn']))
                        )
                except KeyboardInterrupt:
                    break

            # print("This is runtime_profile", runtime_profile)
            print(' ')
            print('===========================> Finish Model Running.')
            if (args.save_img or args.save_video) and not args.vis_fast:
                print('===========================> Rendering remaining images in the queue...')
                print(
                    '===========================> If this step takes too long, you can enable the --vis_fast flag to use fast rendering (real-time).')
            while (writer.running()):
                pass
            writer.stop()












    # def onButtonPress(self, button):
    #     layout = FloatLayout()
    #     popupLabel = Label(text = "11")
    #     closeButton = Button(text = "11",
    #                          background_color = [1,0,0,1])
    #
    #     layout.add_widget(popupLabel)
    #     layout.add_widget(closeButton)
    #     popup = Popup(title = "44",
    #                   content = layout,
    #                   size_hint = (None, None),
    #                   size = (400,400))
    #     popup.open()
    #     closeButton.bind(on_presss = popup.dismiss)








# class InputWindow(App):
#
#     def build(self):
#         self.layout = FloatLayout()
#
#         self.line = UserInput(multiline=False,
#                               size_hint=(0.05, 0.05),
#                               pos_hint={"x": 0.05, "top": 0.9})
#         self.layout.add_widget(self.line)
#         self.pt1 = UserInput(multiline=False,
#                              size_hint=(0.05, 0.05),
#                              pos_hint={"x": 0.12, "top": 0.9})
#         self.layout.add_widget(self.pt1)
#         self.pt2 = UserInput(multiline=False,
#                              size_hint=(0.05, 0.05),
#                              pos_hint={"x": 0.19, "top": 0.9})
#         self.layout.add_widget(self.pt2)
#         self.line1 = UserInput(multiline=False,
#                                size_hint=(0.05, 0.05),
#                                pos_hint={"x": 0.26, "top": 0.9})
#         self.layout.add_widget(self.line1)
#         self.line2 = UserInput(multiline=False,
#                                size_hint=(0.05, 0.05),
#                                pos_hint={"x": 0.33, "top": 0.9})
#         self.layout.add_widget(self.line2)
#         self.min_angle_down = UserInput(multiline=False,
#                                         size_hint=(0.05, 0.05),
#                                         pos_hint={"x": 0.40, "top": 0.9})
#         self.layout.add_widget(self.min_angle_down)
#         self.max_angle_up = UserInput(multiline=False,
#                                       size_hint=(0.05, 0.05),
#                                       pos_hint={"x": 0.47, "top": 0.9})
#         self.layout.add_widget(self.max_angle_up)
#         self.min_angle_up = UserInput(multiline=False,
#                                       size_hint=(0.05, 0.05),
#                                       pos_hint={"x": 0.54, "top": 0.9})
#         self.layout.add_widget(self.min_angle_up)
#         self.max_angle_down = UserInput(multiline=False,
#                                         size_hint=(0.05, 0.05),
#                                         pos_hint={"x": 0.61, "top": 0.9})
#         self.layout.add_widget(self.max_angle_down)
#         self.line_is_move = UserInput(multiline=False,
#                                       size_hint=(0.05, 0.05),
#                                       pos_hint={"x": 0.68, "top": 0.9})
#         self.layout.add_widget(self.line_is_move)
#         self.time_start = UserInput(multiline=False,
#                                     size_hint=(0.05, 0.05),
#                                     pos_hint={"x": 0.75, "top": 0.9})
#         self.layout.add_widget(self.time_start)
#         self.time_end = UserInput(multiline=False,
#                                   size_hint=(0.05, 0.05),
#                                   pos_hint={"x": 0.82, "top": 0.9})
#         self.layout.add_widget(self.time_end)
#         self.tips = UserInput(multiline=False,
#                               size_hint=(0.7, 0.05),
#                               pos_hint={"x": 0.05, "top": 0.8})
#         self.layout.add_widget(self.tips)
#
#         self.save_in_mysql_button = Button(text="保 存",
#                                            font_name='Font_Hanzi',
#                                            background_color=(148 / 155, 242 / 155, 249 / 155),
#                                            size_hint=(0.1, 0.06),
#                                            pos_hint={"x": 0.77, "top": 0.8}
#                                            )
#         self.layout.add_widget(self.save_in_mysql_button)
#
#
#
#
#     def save_in_mysql(self):
#         pass

#
# class MainExeWindow(FloatLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# class MainExeWindow(FloatLayout):
#     def open_input_popup(self):
#         pops = InputWindow()
#         pops.open()



# class ExeApp(App):
#     def build(self):
#         return InputWindow()


#
# def Show_Input_Popup():
#     show = InputWindow()
#     PopurWindow = Popup(title = "标准数据输入窗口",
#                          font_name = 'Font_Hanzi',
#                          content = show,
#                          size_hint = (None, None),
#                          size = (400, 400))
#     PopurWindow.open()

if __name__ == '__main__':
    ExeMainWindow().run()

# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.12, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.19, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.26, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.33, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.40, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.47, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.54, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.61, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.68, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.05, 0.05
# pos_hint: {"x": 0.75, "top": 0.9}
# TextInput:
# multiline: False
# size_hint: 0.7, 0.05
# pos_hint: {"x": 0.05, "top": 0.8}

# <MainExeWindow>:
#     Button:
#         text:"open Popup"
#         pos_hint: {"x":0, "y":0}
#         size_hint:0.3, 0.3
#         on_press:root.open_input_popup()

#     id: pop
#     size_hint:1, 1
#     auto_dismiss: False
#     title:'Popup Window'

# Button:
# text: "11"
# size_hint: 0.05, 0.05
# on_press: pop.dismiss()