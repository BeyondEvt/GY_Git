


# 该文件为Alphapose框架文件，通过调用摄像头，获取人体关节点数据，
# 通过不同关节点数据实现不同的人体动作识别算法
# 将被主程序“Main_kivy”文件所调用
import json
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torchvision.transforms as transforms
from get_standard_data import *
import torch.nn as nn
import torch.utils.data
import numpy as np
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
# from get_standard_data import *
args = opt
args.dataset = 'coco'



q = []  # (存放30帧实时数据)
L = []  # 存放已执行函数
#
# import pyttsx3 as pyttsx
#
# # 调用初始化方法，获取讲话对象
# engine = pyttsx.init()
# engine.say('我叼你妈的')
# engine.runAndWait()

list_father = []
import json
# 读取字典数据
with open("dict.json", 'r+') as f:
	res_list = json.load(f)

print("res_list:",res_list)
func_dict = res_list[0]
print(func_dict)
end_time = res_list[2] + 2


for item in func_dict.keys():
    for j in range(len(func_dict[item])):
        list_father.append([])


def loop():
    n = 0
    while True:
        yield n
        n += 1

# if __name__ == "__main__":
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
save_path = os.path.join(args.outputpath, 'AlphaPose_webcam'+webcam+'.avi')
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

from subprocess import Popen, PIPE, STDOUT

p = Popen([sys.executable, "video_play.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
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
                inps_j = inps[j*batchSize:min((j + 1)*batchSize, datalen)].cuda()
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
                # 获取每帧的人体关节点数据并计算各肢节所形成的角度
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

                standard_num = -1/2


                # 存储规定时间段内所需执行的人体动作识别函数，将函数存于一个栈（列表）中，供后续执行
                now = time.time()
                if int(now - start_0) % 10 == 0:
                    engine = pyttsx.init()
                    engine.say("目前得分为{}分".format(end()))
                    engine.runAndWait()


                if now - start_0 >=  end_time:
                    print(now - start_0, end_time)
                    print("退出")
                    os._exit(0)
                if str(np.floor(now - start_0)) in func_dict:
                    for i in range(len(func_dict[str(np.floor(now - start_0))])):
                        L.append(func_dict[str(np.floor(now - start_0))][i])
                    del func_dict[str(np.floor(now - start_0))]
                # print(point)
                # engine = pyttsx.init()
                # engine.say(point)
                # engine.runAndWait()

                option = standard_func(keypoints)

                # 执行上述存储在栈中的人体动作识别函数
                for i in range(len(L)):
                    # 通过列表每个元素第一个数据来决定采用哪个识别函数
                    if L[i][0] == 1:
                        option.point_angle(L[i][2],L[i][3],L[i][6],L[i][7],L[i][-1],list_father[i])

                    if L[i][0] == 2:
                        option.line_angle(L[i][1],L[i][6],L[i][7],L[i][8],L[i][9],L[i][-4],L[i][-1],list_father[i])

                    if L[i][0] == 3:
                        option.lines_angle(L[i][4],L[i][5],L[i][6],L[i][7],L[i][-1],list_father[i])

                # print(L)
                # 结束函数
                pop_list = []  # 临时存放要pop的函数
                for i in range(len(L)):
                    if (now - start_0) >= L[i][-2]:
                        pop_list.append(i)

                pop_list = pop_list[::-1]  # 将要pop的函数序号颠倒，避免列表长度减少导致索引出错


                for i in pop_list:
                    L.pop(i)               # 将不再执行的命令pop出L
                    list_father.pop(i)


        if args.profile:
            # TQDM
            im_names_desc.set_description(
            'det time: {dt:.3f} | pose time: {pt:.2f} | post processing: {pn:.4f}'.format(
                dt=np.mean(runtime_profile['dt']), pt=np.mean(runtime_profile['pt']), pn=np.mean(runtime_profile['pn']))
            )
    except KeyboardInterrupt:
        break
print(end())
engine = pyttsx.init()
engine.say("您的总得分为{}分".format(end()))
engine.runAndWait()
# print("This is runtime_profile", runtime_profile)
print(' ')
print('===========================> Finish Model Running.')
if (args.save_img or args.save_video) and not args.vis_fast:
    print('===========================> Rendering remaining images in the queue...')
    print('===========================> If this step takes too long, you can enable the --vis_fast flag to use fast rendering (real-time).')
while(writer.running()):
    pass
writer.stop()
final_result = writer.results()
write_json(final_result, args.outputpath)
