# -*- coding: utf-8 -*-
# dict1 = {'0.0': [[1, 0, 6, 7, 0, 0, 0, 0.3490658503988659, 0, 0, False, 1115.0, ['1', '减小两肩的高低距离']], [2, 6, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, True, 1115.0, ['减小左小腿的最大角度', '', '增大左小腿的最大角度', '']], [2, 8, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, True, 1115.0, ['减小右小腿的最大角度', '', '增大右小腿的最大角度', '']]], '5.0': [[2, 5, 0, 0, 0, 0, 0, 1.5707963267948966, 0, 1.0471975511965976, True, 2110.0, ['减小左大腿的最大角度', '1', '增大左大腿的最大角度', '2']], [2, 7, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, True, 2110.0, ['减小右大腿的最大角度', '', '增大右大腿的最大角度', '']]]}

# 数据库 MySql引用
from MySql.connect_mysql import *
import json

# 从云数据库提取video数据
data_sql_data = VIDEO_data()
# 从云数据库提取video的基础参数数据
video_play_data = VIDEO_data2()

# 将提取到的数据种纠错文字信息进行处理
correction_tips = data_sql_data[13::14]
# print(correction_tips)

# 将数据拆分成
data_sql_data= [data_sql_data[i:i+14] for i in range(0, len(data_sql_data), 14)]
# print(data_sql)

# 元组转换为列表
for i in range(len(data_sql_data)):
    data_sql_data[i] = list(data_sql_data[i])
print(data_sql_data)
print(data_sql_data[0][13])
print(data_sql_data[0][13].split(sep = '-'))
print(json.dumps(data_sql_data[0][13].split(sep = '-')))
print(data_sql_data)



# 生成数据字典
# data_dict = dict()
# for i in range(len(data_sql)):
#     index = str("%.1f"%(int(data_sql[i][-3])))
#     if index not in data_dict:
#         data_dict[index] = []
#     if data_sql[i][1] != 0:
#         data_dict[index].append([2, int(data_sql[i][1]),int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]), int(data_sql[i][5]),
#                                  float(data_sql[i][6]),float(data_sql[i][7]),float(data_sql[i][8]),float(data_sql[i][9]),bool(int(data_sql[i][10])),
#                                  float("%.1f"%(int(data_sql[i][12]))), json.dumps(data_sql[i][13].split(sep = '-'))])
#     if data_sql[i][1] == 0 and data_sql[i][2] != 0 and data_sql[i][3] != 0:
#         data_dict[index].append([1, int(data_sql[i][1]),int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]), int(data_sql[i][5]),
#                                  float(data_sql[i][6]),float(data_sql[i][7]),float(data_sql[i][8]),float(data_sql[i][9]),bool(int(data_sql[i][10])),
#                                  float("%.1f"%(int(data_sql[i][12]))), json.dumps(data_sql[i][13].split(sep = '-'))])
#     if data_sql[i][4] != 0 and data_sql[i][5] != 0:
#         data_dict[index].append([3, int(data_sql[i][1]),int(data_sql[i][2]), int(data_sql[i][3]), int(data_sql[i][4]), int(data_sql[i][5]),
#                                  float(data_sql[i][6]),float(data_sql[i][7]),float(data_sql[i][8]),float(data_sql[i][9]),bool(int(data_sql[i][10])),
#                                  float("%.1f"%(int(data_sql[i][12]))), json.dumps(data_sql[i][13].split(sep = '-'))])




# [{"0.0": [[1, 0, 6, 7, 0, 0, 0, 0.3490658503988659, 0, 0, false, 1115.0, ["1", "\u51cf\u5c0f\u4e24\u80a9\u7684\u9ad8\u4f4e\u8ddd\u79bb"]], [2, 6, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]], [2, 8, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]], "5.0": [[2, 5, 0, 0, 0, 0, 0, 1.5707963267948966, 0, 1.0471975511965976, true, 2110.0, ["\u51cf\u5c0f\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "1", "\u589e\u5927\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "2"]], [2, 7, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 2110.0, ["\u51cf\u5c0f\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]]}, "video1.mp4", 10.0]
# print(data_dict)

# data_sql= [data_sql[i:i+14] for i in range(0, len(data_sql), 14)]
# print(data_sql)
# dict_json = json.dumps(dict1)



