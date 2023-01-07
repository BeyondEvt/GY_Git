import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torchvision.transforms as transforms

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

from pPose_nms import write_json
from standard_data import *

args = opt
args.dataset = 'coco'

q = []  # (存放30帧实时数据)

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
# *********************************************************
#                     option1 = standard_data(keypoints)
#                     option1.point_angle(6,7,0, np.pi/6,q)
# *********************************************************

                    option2 = standard_data(keypoints)
                    option2.line_angle(1,3, np.pi/6, np.pi/3, q )


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
                    dt=np.mean(runtime_profile['dt']), pt=np.mean(runtime_profile['pt']), pn=np.mean(runtime_profile['pn']))
                )
        except KeyboardInterrupt:
            break

    # print("This is runtime_profile", runtime_profile)
    print(' ')
    print('===========================> Finish Model Running.')
    if (args.save_img or args.save_video) and not args.vis_fast:
        print('===========================> Rendering remaining images in the queue...')
        print('===========================> If this step takes too long, you can enable the --vis_fast flag to use fast rendering (real-time).')
    while(writer.running()):
        pass
    writer.stop()
    # final_result = writer.results()
    # write_json(final_result, args.outputpath)
