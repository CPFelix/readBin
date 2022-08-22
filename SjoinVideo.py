# coding: utf-8
import os
import cv2
import numpy as np
from tqdm import tqdm

def video2image(videopath):
    if os.path.isfile(videopath):
        videoname = videopath.split("/")[-1]
        mp4 = cv2.VideoCapture(videopath)  # 读取视频
        is_opened = mp4.isOpened()  # 判断是否打开
        print(is_opened)
        fps = mp4.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
        sumps = mp4.get(cv2.CAP_PROP_FRAME_COUNT)  # 总帧数
        print(fps, sumps, "帧")
        widght = mp4.get(cv2.CAP_PROP_FRAME_WIDTH)  # 获取视频的宽度
        height = mp4.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 获取视频的高度
        print(str(widght) + "x" + str(height))
        i = 0
        while is_opened:
            i += 1
            (flag, frame) = mp4.read()  # 读取图片
            if flag == False:
                break
            file_name = "video_" + videoname.split(".")[0].split("-")[-1] + "_" + str(i) + ".jpg"
            imgpath = videopath.split("/")[0]
            if not os.path.exists(imgpath):
                os.makedirs(imgpath)
            imgfile = os.path.join(imgpath, file_name)
            cv2.imwrite(imgfile, frame, [cv2.IMWRITE_JPEG_QUALITY])  # 保存图片
    else:
        for v in os.listdir(videopath):
            if v.split(".")[-1] in ["mp4", "avi"]:
                videofile = os.path.join(videopath, v)
                mp4 = cv2.VideoCapture(videofile)  # 读取视频
                is_opened = mp4.isOpened()  # 判断是否打开
                print(is_opened)
                fps = mp4.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
                sumps = mp4.get(cv2.CAP_PROP_FRAME_COUNT)  # 总帧数
                print(fps, sumps, "帧")
                widght = mp4.get(cv2.CAP_PROP_FRAME_WIDTH)  # 获取视频的宽度
                height = mp4.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 获取视频的高度
                print(str(widght) + "x" + str(height))
                i = 0
                while is_opened:
                    i += 1
                    print("{} % {}".format(i, sumps))
                    (flag, frame) = mp4.read()  # 读取图片
                    if flag == False:
                        break
                    file_name = "video_" + v.split(".")[0].split("-")[-1] + "_" + str(i) + ".jpg"
                    imgpath = videofile.split(".")[0]
                    if not os.path.exists(imgpath):
                        os.makedirs(imgpath)
                    imgfile = os.path.join(imgpath, file_name)
                    # cv2.imwrite(imgfile, frame)  # 保存图片
                    cv2.imencode('.jpg', frame)[1].tofile(imgfile)
    print("视频拆帧完成！")


def image2video(imgdir, fps, save_path):
    files = os.listdir(imgdir)
    files.sort(key=lambda x: int(x.split(".")[0].split("_")[0]))
    # 获取图像宽高
    img0 = os.path.join(imgdir, files[0])
    h, w, _ = cv2.imread(img0).shape
    # h, w, _ = cv2.imdecode(np.fromfile(img0, dtype=np.uint8), -1).shape  # 读取
    # 设置帧数
    fps = fps
    # 保存视频路径和名称
    save_path = save_path  # 保存视频路径和名称 MP4格式
    # 准备写入视频
    vid = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    # 写入
    for file in tqdm(files):
        img = cv2.imread(os.path.join(imgdir, file))
        # img = cv2.imdecode(np.fromfile(os.path.join(imgdir, file), dtype=np.uint8), -1)
        vid.write(img)
    vid.release()

if __name__ == "__main__":
    # videopath = "F:/中石油DSM难例视频收集/分心驾驶/20220718"
    # video2image(videopath)

    videoname = "02_65_6504_4_22040610008-20220716151743-04137"
    imgdir = "E:/pycharm-projects/readBin/" + videoname + "/jpg"
    save_path = "E:/pycharm-projects/readBin/" + videoname + "/" + videoname + "_draw.mp4"
    image2video(imgdir, 16, save_path)
