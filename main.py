import struct
import io
import os
from PIL.Image import Image
import numpy as np
import cv2
from tqdm import tqdm
import threading
import random
import time

def convertImg(fileList):
    for file in tqdm(fileList):
        if file.endswith(".bin"):
            binPath = os.path.join(filepath, file)
            binfile = open(binPath, 'rb')  # 打开二进制文件
            size = os.path.getsize(filepath)  # 获得文件大小
            # print(size)
            h = int(binPath.split("/")[-1].split("_")[1][1:])
            w = int(binPath.split("/")[-1].split("_")[2][1:])
            # print("h:", h, " w:", w)
            array_img = np.zeros(shape=(h, w))
            for i in range(h):
                for j in range(w):
                    data = binfile.read(1)  # 每次输出一个字节
                    num = struct.unpack('B', data)
                    # print(num[0])
                    array_img[i][j] = num[0]
            jpgPath = filepath.replace("/bin/", "/jpg/")
            if not os.path.exists(jpgPath):
                os.makedirs(jpgPath)
            imgName = jpgPath + binPath.split("/")[-1].split(".")[0] + ".jpg"
            cv2.imwrite(imgName, array_img)

def subset(alist, idxs):
    '''
        用法：根据下标idxs取出列表alist的子集
        alist: list
        idxs: list
    '''
    sub_list = []
    for idx in idxs:
        sub_list.append(alist[idx])

    return sub_list

def split_list(alist, group_num=4, shuffle=True, retain_left=True):
    '''
        用法：将alist切分成group个子列表，每个子列表里面有len(alist)//group个元素
        shuffle: 表示是否要随机切分列表，默认为True
        retain_left: 若将列表alist分成group_num个子列表后还要剩余，是否将剩余的元素单独作为一组
    '''

    index = list(range(len(alist)))  # 保留下标

    # 是否打乱列表
    if shuffle:
        random.shuffle(index)

    elem_num = len(alist) // group_num  # 每一个子列表所含有的元素数量
    sub_lists = []

    # 取出每一个子列表所包含的元素，存入字典中
    for idx in range(group_num):
        start, end = idx * elem_num, (idx + 1) * elem_num
        sub_lists.append(subset(alist, index[start:end]))

    # 是否将最后剩余的元素作为单独的一组
    if retain_left and group_num * elem_num != len(index):  # 列表元素数量未能整除子列表数，需要将最后那一部分元素单独作为新的列表
        sub_lists.append(subset(alist, index[end:]))

    return sub_lists


if __name__ == '__main__':
    # filepath='./smoke/03/bin/'
    filepath = "./binTemp9/bin/"
    if os.path.isfile(filepath):
        binfile = open(filepath, 'rb') #打开二进制文件
        size = os.path.getsize(filepath) #获得文件大小
        print(size)
        h = int(filepath.split("_")[1][1:])
        w = int(filepath.split("_")[2][1:])
        print("h:", h, " w:", w)
        array_img = np.zeros(shape=(h, w))
        for i in range(h):
            for j in range(w):
                data = binfile.read(1) #每次输出一个字节
                num = struct.unpack('B', data)
                # print(num[0])
                array_img[i][j] = num[0]
        print("end\n")
        imgName = "./bin/" + filepath.split("/")[-1].split(".")[0] + ".jpg"
        cv2.imwrite(imgName, array_img)
    else:
        T1 = time.time()
        all_file_list = os.listdir(filepath)
        sub_lists = split_list(all_file_list, group_num=4)
        for i in range(len(sub_lists)):
            t = threading.Thread(target=convertImg, args=(sub_lists[i],))
            t.start()
        # for file in tqdm(os.listdir(filepath)):
        #     if file.endswith(".bin"):
        #         binPath = os.path.join(filepath, file)
        #         binfile = open(binPath, 'rb')  # 打开二进制文件
        #         size = os.path.getsize(filepath)  # 获得文件大小
        #         # print(size)
        #         h = int(binPath.split("/")[-1].split("_")[1][1:])
        #         w = int(binPath.split("/")[-1].split("_")[2][1:])
        #         # print("h:", h, " w:", w)
        #         array_img = np.zeros(shape=(h, w))
        #         for i in range(h):
        #             for j in range(w):
        #                 data = binfile.read(1)  # 每次输出一个字节
        #                 num = struct.unpack('B', data)
        #                 # print(num[0])
        #                 array_img[i][j] = num[0]
        #         jpgPath = filepath.replace("/bin/", "/jpg/")
        #         if not os.path.exists(jpgPath):
        #             os.makedirs(jpgPath)
        #         imgName = jpgPath + binPath.split("/")[-1].split(".")[0] + ".jpg"
        #         cv2.imwrite(imgName, array_img)
        T2 = time.time()
        print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))