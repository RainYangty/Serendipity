# From: https://blog.csdn.net/weixin_45067072/article/details/108923077
from cgitb import grey
import cv2
import numpy as np
import imutils

def fixed_pos(imgans):
    # img=cv2.imread(pos)
    try:
        y,x = imgans.shape
    except ValueError:
        y,x,z = imgans.shape
    if(x > y):
        imgans = imutils.rotate_bound(imgans, 90)
    # 缩放 + 灰度处理
    img = imgans.copy()
    img = cv2.resize(img, (1036, 1473))
    try:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    except:
        img = img
    rate = [0.0, 0.0]
    for to in range(0, 2, 1):
        #这一步裁剪指定区域图片。
        s = img[1440:1473, 990:1096] # y_start : y_end, x_start : x_end
        #起始x,y坐标，终止x,y坐标，而非加上宽和高
        # 和之前用到的cv2.boundingRect()函数定位法不同
        
        # cv2.imshow('res',img)

        #答题卡右下角蓝色定位黑色处理
        re, s = cv2.threshold(s, 200, 255,cv2.THRESH_BINARY)# 这里的第二个参数要调，是阈值！！  # From: https://blog.csdn.net/qq_36584673/article/details/121398502
        # cv2.imshow('ss' + str(to),s)
        #注意这里s已经是单通道，此时不返回通道值。
        x,y = s.shape

        bk = 0
        wt = 0
        #遍历二值图，为0则bk+1，否则wt+1
        for i in range(x):
            for j in range(y):
                if s[i,j]==0:
                    bk+=1
        rate[to] = bk/(x*y)
        # cv2.rectangle(img,(990, 1440),(1096, 1473),(0,0,255),3)
        # cv2.imshow("res"+ str(to),img)
        # round()第二个值为保留几位有效小数。
        # # print("黑色占比:", round(rate[to]*100,2),'%')
        img = imutils.rotate_bound(img, 180)
    # print(rate)

    # 作出修正图像
    if(rate[0] < rate[1] and rate[1] > 0.5):
        imgans = imutils.rotate_bound(imgans, 180)
        cv2.rectangle(imgans,(990, 1440),(1096, 1473),(0,0,255),3)
    else:
        if(rate[0] > 0.5):
            cv2.rectangle(imgans,(990, 1440),(1096, 1473),(0,0,255),3)
    # cv2.imshow('ans',imgans)
    return imgans
    
