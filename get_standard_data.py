# 该文件用来制定各种动作中的标准
# 通过
# 大体框架： 1. 点点间(两个关节点间)  主要是评估两个点所成的角度 一个肢节于竖直夹角
#           2. 线段间(两个肢节间的夹角)    前者是制定该肢节的上下标准，后者是判断角度是否达标。
point = 0
import numpy as np
import pyttsx3 as pyttsx

func_dict = {}
# 偶数点为左手边，奇数点为右手边
line_dict = {"1":[6, 8], "2":[8, 10], "3":[7,9], "4":[9, 11], "5":[12, 14], "6":[14, 16], "7":[13,15], "8":[15, 17]}
class standard_func(object):
    def __init__(self, keypoints):
        self.keypoints = keypoints.numpy()



    # 该函数识别人体两个关节点，通过计算两关节点连线与水平面角度并于标准数据进行比较
    # 角度过大或者过小都会进行提醒，故tips列表中需有两个提醒字符串
    def point_angle(self, pt1 , pt2, min_angle, max_angle, tips , Q):
        global point
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
        if real_angle < min_angle:
            index = 1


        elif real_angle > max_angle:
            index = 2

        if len(Q) < 30:
            Q.append(index)
        elif len(Q) == 30:
            Q.pop(0)
            Q.append(index)


        if Q.count(1) >= 8:

            # 调用初始化方法，获取讲话对象
            engine = pyttsx.init()
            engine.say(tips[0])
            engine.runAndWait()
            print(tips[0])
            Q.__init__()

        elif Q.count(2) >= 8:
            # 调用初始化方法，获取讲话对象
            engine = pyttsx.init()
            engine.say(tips[1])
            engine.runAndWait()
            print(tips[1])
            Q.__init__()
        else:
            point += 1



    # 该函数识别单肢节，通过计算角度并于标准数据进行比较
    # 角度过大或者过小都会进行提醒，故tips列表中需有四个提醒字符串（动态）/两个提醒字符串（静态）
    def line_angle(self, line, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move, tips, Q, ):
            global point
            # 判断最大角度区间
            # print(line)
            # print(str(line))
            pt1_pos = self.keypoints[line_dict[str(line)][0] - 1]
            pt2_pos = self.keypoints[line_dict[str(line)][1] - 1]

            vector1 = pt2_pos - pt1_pos
            vector2 = [0, 1]

            real_angle = np.arccos(
                (np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))


            if line_is_move:  # 单肢节动态，用于识别评价肢节摆动的角度

                # 评判角度是否达到标准
                index1,index2 = 0, 0
                if max_angle_up != max_angle_down:
                    if real_angle > max_angle_up:
                        index1 = 1
                    elif real_angle >= max_angle_down:
                        index1 = 3

                if min_angle_up != min_angle_down:
                    if real_angle < min_angle_down:
                        index2 = 2
                    elif real_angle <= min_angle_up:
                        index2 = 4

                if len(Q) < 60:
                    Q.append(index1)
                    Q.append(index2)
                elif len(Q) == 60:
                    Q.pop(0)
                    Q.pop(0)
                    Q.append(index1)
                    Q.append(index2)


                if len(Q) == 60:

                    if max_angle_up != max_angle_down:
                        if Q.count(1) >= 8:
                            engine = pyttsx.init()
                            engine.say(tips[0])
                            engine.runAndWait()
                            # print(tips[0])
                            Q.__init__()
                        elif Q.count(3) <= 2:
                            engine = pyttsx.init()
                            engine.say(tips[3])
                            engine.runAndWait()
                            # print(tips[2])
                            Q.__init__()
                        else:
                            point += 1

                    if min_angle_up != min_angle_down:
                        if Q.count(2) >= 8:
                            engine = pyttsx.init()
                            engine.say(tips[1])
                            engine.runAndWait()
                            # print(tips[1])
                            Q.__init__()
                        elif Q.count(4) <= 5:
                            engine = pyttsx.init()
                            engine.say(tips[2])
                            engine.runAndWait()
                            # print(tips[3])
                            Q.__init__()
                        else:
                            point += 1



            else: # 单肢节静态，用于识别评价肢节静止的角度
                index = 0
                if real_angle > max_angle_up:
                    index = 1
                elif real_angle < min_angle_down:
                    index = 2

                if len(Q) < 30:
                    Q.append(index)

                elif len(Q) == 30:

                    Q.pop(0)
                    Q.append(index)


                if len(Q) == 30:
                    if Q.count(1) >= 8:
                        engine = pyttsx.init()
                        engine.say(tips[1])
                        engine.runAndWait()
                        # print(tips[0])
                        Q.__init__()

                    elif Q.count(2) >= 8:
                        engine = pyttsx.init()
                        engine.say(tips[0])
                        engine.runAndWait()
                        # print(tips[1])
                        Q.__init__()
                    else:
                        point += 1

    # 1:左手上(6,8) 2：左手下(8,10) 3：右手上 4：右手下
    # 该函数识别双肢节，通过计算角度并于标准数据进行比较
    # 角度过大或者过小都会进行提醒，故tips列表中需有两个提醒字符串
    def lines_angle(self, line1, line2, min_angle, max_angle, tips, Q):
        global point
        line1 = line_dict[str(line1)]
        line2 = line_dict[str(line2)]
        vector1 = self.keypoints[line1[0] - 1] - self.keypoints[line1[1] - 1]
        vector2 = self.keypoints[line2[0] - 1] - self.keypoints[line2[1] - 1]
        real_angle = np.arccos((np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))

        # 评判角度是否达到标准
        index = 0
        if real_angle < min_angle:
            index = 1


        elif real_angle > max_angle:
            index = 2

        if len(Q) < 30:
            Q.append(index)
        elif len(Q) == 30:
            Q.pop(0)
            Q.append(index)


        if Q.count(1) >= 8:
            engine = pyttsx.init()
            engine.say(tips[0])
            engine.runAndWait()
            # print(tips[0])
            Q.__init__()
        elif Q.count(2) >= 8:
            engine = pyttsx.init()
            engine.say(tips[1])
            engine.runAndWait()
            # print(tips[1])
            Q.__init__()
        elif len(Q) == 30:
            point += 1


def give_standard( line, pt1, pt2, line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move, time_start, time_end, tips): # time_start, time_end精确0.1
    # 该函数用于教练制定标准，生成一个字典存放标准规范所需的参数

    if line != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[2, line, pt1, pt2,line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move , time_end, tips]]
        else:
            func_dict[str(time_start)].append([2, line, pt1, pt2,line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move ,time_end, tips])
    elif line == 0 and pt1 != 0 and pt2 != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[1, line, pt1, pt2,line1, line2,min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move , time_end, tips]]
        else:
            func_dict[str(time_start)].append([1,  line, pt1, pt2,line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move ,  time_end, tips])
    elif line1 != 0 and line2 != 0:
        if str(time_start) not in func_dict:
            func_dict[str(time_start)] = [[3, line, pt1, pt2,line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move , time_end, tips]]
        else:
            func_dict[str(time_start)].append([3,  line, pt1, pt2,line1, line2, min_angle_down, max_angle_up, min_angle_up,  max_angle_down, line_is_move , time_end, tips])

def end():
    return point


