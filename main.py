import struct
import io
import os
from PIL.Image import Image
import numpy as np
import cv2

if __name__ == '__main__':
    filepath='./bin/1655962672608_h720_w1280_mIsLeaving.bin'
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