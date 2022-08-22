# From https://www.jb51.net/article/232536.htm
import cv2 as cv
import numpy as np
from log_write import log_write

def edge(pos):
    # 输入图像
    log_write("info", "reding image from: " + pos)
    try:
        img = cv.imread(pos)
        img_copy = img.copy()
        img_gray = img # cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    except AttributeError:
        log_write("warning", "Get download file Error...")
        return False
    # cv.imshow('img-gray', img_gray)

    # 图像预处理
    # 高斯降噪
    log_write("info", "img gaussian...")
    img_gaussian = cv.GaussianBlur(img_gray, (5, 5), 1)
    #cv.imshow('gaussianblur', img_gaussian)
    # canny边缘检测
    log_write("info", "img canny...")
    img_canny = cv.Canny(img_gaussian, 80, 150)
    # cv.imshow('canny', img_canny)

    # 轮廓识别——答题卡边缘识别
    log_write("info", "cv find card and ans")
    cnts, hierarchy = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_copy, cnts, -1, (0, 0, 255), 3)
    # cv.imshow('contours-show', img_copy)

    docCnt = None
    
    # 确保检测到了
    if len(cnts) > 0:
        # 根据轮廓大小进行排序
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    
        # 遍历每一个轮廓
        for c in cnts:
            # 近似
            peri = cv.arcLength(c, True)
            # arclength 计算一段曲线的长度或者闭合曲线的周长；
            # 第一个参数输入一个二维向量，第二个参数表示计算曲线是否闭合
    
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            # 用一条顶点较少的曲线/多边形来近似曲线/多边形，以使它们之间的距离<=指定的精度；
            # c是需要近似的曲线，0.02*peri是精度的最大值，True表示曲线是闭合的
    
            # 准备做透视变换
            if len(approx) == 4:
                docCnt = approx
                break

    def four_point_transform(img, four_points):
        rect = order_points(four_points)
        (tl, tr, br, bl) = rect
    
        # 计算输入的w和h的值
        widthA = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)
        widthB = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
        maxWidth = max(int(widthA), int(widthB))
    
        heightA = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
        heightB = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
        maxHeight = max(int(heightA), int(heightB))
    
        # 变换后对应的坐标位置
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype='float32')
    
        # 最主要的函数就是 cv2.getPerspectiveTransform(rect, dst) 和 cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        M = cv.getPerspectiveTransform(rect, dst)
        warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))
        return warped
    
    def order_points(points):
        res = np.zeros((4, 2), dtype='float32')
        # 按照从前往后0，1，2，3分别表示左上、右上、右下、左下的顺序将points中的数填入res中
    
        # 将四个坐标x与y相加，和最大的那个是右下角的坐标，最小的那个是左上角的坐标
        sum_hang = points.sum(axis=1)
        res[0] = points[np.argmin(sum_hang)]
        res[2] = points[np.argmax(sum_hang)]
    
        # 计算坐标x与y的离散插值np.diff()
        diff = np.diff(points, axis=1)
        res[1] = points[np.argmin(diff)]
        res[3] = points[np.argmax(diff)]
    
        # 返回result
        return res

    # 透视变换——提取答题卡主体
    docCnt = docCnt.reshape(4, 2)
    warped = four_point_transform(img_gray, docCnt)
    # cv.imshow('warped', warped)
    # cv.waitKey(0)
    return warped

def real_time_edge(pos):
    # 输入图像
    try:
        img = pos
        img_copy = pos.copy()
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    except AttributeError:
        return False
    # cv.imshow('img-gray', img_gray)

    # 图像预处理
    # 高斯降噪
    img_gaussian = cv.GaussianBlur(img_gray, (5, 5), 1)
    #cv.imshow('gaussianblur', img_gaussian)
    # canny边缘检测
    img_canny = cv.Canny(img_gaussian, 80, 150)
    # cv.imshow('canny', img_canny)

    # 轮廓识别——答题卡边缘识别
    cnts, hierarchy = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_copy, cnts, -1, (0, 0, 255), 3)
    # cv.imshow('contours-show', img_copy)

    docCnt = None
    
    # 确保检测到了
    if len(cnts) > 0:
        # 根据轮廓大小进行排序
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)
    
        # 遍历每一个轮廓
        for c in cnts:
            # 近似
            peri = cv.arcLength(c, True)
            # arclength 计算一段曲线的长度或者闭合曲线的周长；
            # 第一个参数输入一个二维向量，第二个参数表示计算曲线是否闭合
    
            approx = cv.approxPolyDP(c, 0.02 * peri, True)
            # 用一条顶点较少的曲线/多边形来近似曲线/多边形，以使它们之间的距离<=指定的精度；
            # c是需要近似的曲线，0.02*peri是精度的最大值，True表示曲线是闭合的
    
            # 准备做透视变换
            if len(approx) == 4:
                docCnt = approx
                break

        def four_point_transform(img, four_points):
            rect = order_points(four_points)
            (tl, tr, br, bl) = rect
        
            # 计算输入的w和h的值
            widthA = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)
            widthB = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
            maxWidth = max(int(widthA), int(widthB))
        
            heightA = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
            heightB = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
            maxHeight = max(int(heightA), int(heightB))
        
            # 变换后对应的坐标位置
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype='float32')
        
            # 最主要的函数就是 cv2.getPerspectiveTransform(rect, dst) 和 cv2.warpPerspective(image, M, (maxWidth, maxHeight))
            M = cv.getPerspectiveTransform(rect, dst)
            warped = cv.warpPerspective(img, M, (maxWidth, maxHeight))
            return warped
        
        def order_points(points):
            res = np.zeros((4, 2), dtype='float32')
            # 按照从前往后0，1，2，3分别表示左上、右上、右下、左下的顺序将points中的数填入res中
        
            # 将四个坐标x与y相加，和最大的那个是右下角的坐标，最小的那个是左上角的坐标
            sum_hang = points.sum(axis=1)
            res[0] = points[np.argmin(sum_hang)]
            res[2] = points[np.argmax(sum_hang)]
        
            # 计算坐标x与y的离散插值np.diff()
            diff = np.diff(points, axis=1)
            res[1] = points[np.argmin(diff)]
            res[3] = points[np.argmax(diff)]

            # 返回result
            return res

        # 透视变换——提取答题卡主体
        try:
            docCnt = docCnt.reshape(4, 2)
            warped = four_point_transform(img_gray, docCnt)
            return warped
        except AttributeError:
            return False
        # cv.imshow('warped', warped)
        # cv.waitKey(0)
        
    else:
        return False