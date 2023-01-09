# 该文件用来制定各种动作中的标准
# 大体框架： 1. 点点间(两个关节点间)  主要是评估两个点所成的角度 一个肢节于竖直夹角
#           2. 线段间(两个肢节间的夹角)    前者是制定该肢节的上下标准，后者是判断角度是否达标。

import numpy as np
func_dict = {}
line_dict = {"1":[6, 8], "2":[8, 10], "3":[7,9], "4":[9, 11], "5":[12, 14], "6":[14, 16], "7":[13,15], "8":[15, 17]}
class standard_func(object):
    def __init__(self, keypoints):
        self.keypoints = keypoints.numpy()



    def point_angle(self,min_angle, max_angle, Q, line = 0, pt1 = 0, pt2 = 0 ):
        if line == 0:
            pt1_pos = self.keypoints[pt1 - 1]
            pt2_pos = self.keypoints[pt2 - 1]
            if pt1_pos[1] >= pt2_pos[1]:
                vector1 = pt1_pos - pt2_pos
                vector2 = [pt1_pos[0] - pt2_pos[0], 0]
            else:
                vector1 = pt2_pos - pt1_pos
                vector2 = [pt2_pos[0] - pt1_pos[0], 0]

            real_angle = np.arccos(abs((np.dot(vector1, vector2)/(np.linalg.norm(vector1) * np.linalg.norm(vector2)))))

            # 评判角度是否达到标准
            index = 0
            if real_angle < min_angle or real_angle > max_angle:
                index = 1
            if len(Q) < 30:
                Q.append(index)
            if len(Q) == 30:
                Q.pop(0)
                Q.append(index)

            if Q.count(1) >= 8:
                print("你的两肩高低距离适当减小￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥")
                Q.__init__()
            else:
                print("OK")

        if line != 0:

            pt1_pos = self.keypoints[line_dict[str(line)][0] - 1]
            pt2_pos = self.keypoints[line_dict[str(line)][1] - 1]
            if pt1_pos[1] >= pt2_pos[1]:
                vector1 = pt2_pos - pt1_pos
                vector2 = [0, pt1_pos[1] - pt2_pos[1]]
            else:
                vector1 = pt2_pos - pt1_pos
                vector2 = [0, pt2_pos[1] - pt1_pos[1]]

            real_angle = np.arccos(
                abs((np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))))

            # 评判角度是否达到标准
            index = 0
            if real_angle < min_angle or real_angle > max_angle:
                index = 1
            if len(Q) < 30:
                Q.append(index)
            if len(Q) == 30:
                Q.pop(0)
                Q.append(index)

            if Q.count(1) >= 8:
                print("肢节向外角度适当减小￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥")
                Q.__init__()
            else:
                print("OJBK")


    # 1:左手上(6,8) 2：左手下(8,10) 3：右手上 4：右手下
    def line_angle(self, line1, line2, min_angle, max_angle, Q):
        line1 = line_dict[str(line1)]
        line2 = line_dict[str(line2)]
        vector1 = self.keypoints[line1[0] - 1] - self.keypoints[line1[1] - 1]
        vector2 = self.keypoints[line2[0] - 1] - self.keypoints[line2[1] - 1]
        real_angle = np.arccos((np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))

        # 评判角度是否达到标准
        index = 0
        if real_angle < min_angle or real_angle > max_angle:
            index = 1
        if len(Q) < 30:
            Q.append(index)
        if len(Q) == 30:
            Q.pop(0)
            Q.append(index)

        if Q.count(1) >= 8:
            print("你的两个肢节角度不当$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            Q.__init__()
        else:
            print("OK")



def give_standard( line, pt1, pt2, line1, line2, min_angle, max_angle, time_start, time_end): # time_start, time_end精确0.1
    if line != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[2, line, pt1, pt2,line1, line2, min_angle, max_angle, time_end]]
        else:
            func_dict[str(time_start)].append([2, line, pt1, pt2,line1, line2, min_angle, max_angle, time_end])
    elif line == 0 and pt1 != 0 and pt2 != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[1, line, pt1, pt2,line1, line2, min_angle, max_angle, time_end]]
        else:
            func_dict[str(time_start)].append([1,  line, pt1, pt2,line1, line2, min_angle, max_angle, time_end])
    elif line1 != 0 and line2 != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[3, line, pt1, pt2,line1, line2, min_angle, max_angle, time_end]]
        else:
            func_dict[str(time_start)].append([3,  line, pt1, pt2,line1, line2, min_angle, max_angle, time_end])












#
# def get_standard_data():
#     order = input()
#     while(order != "#"):
#
# # 点点间 -> 规定一个角度



