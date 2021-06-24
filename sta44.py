#将DICOM
import os
import SimpleITK as sitk
import numpy as np
import cv2
import pandas as pd
import glob

#批量转换
def batchCovert(p2p3Path2):
    # 打开文件,获取路径
    #0460dc48,BP3R5QO1,219,C:\ct-raw-scan\De-identified scan images\Non-HCC\0460dc48\W5TQRF1G\BP3R5QO1
    df = pd.read_csv(p2p3Path2, header=0, sep=",")
    for index, row in df.iterrows():
        dicompath = df.iloc[index, 3]  # 获取第0行第0列(路径)
        jpgpath= dicompath+"_jpg"
        if( not os.path.exists(jpgpath)):
            os.mkdir(jpgpath)

def dicom2jpg(dicompath, jpgpath):
    if (os.path.exists(dicompath)):
       fileList = glob.glob(dicompath + "/*")
       for file in fileList:
           ds_array = sitk.ReadImage(file)  # 读取dicom文件的相关信息
           img_array = sitk.GetArrayFromImage(ds_array)  # 获取array
           # SimpleITK读取的图像数据的坐标顺序为zyx，即从多少张切片到单张切片的宽和高，此处我们读取单张，因此img_array的shape
           # 类似于 （1，height，width）的形式
           shape = img_array.shape
           img_array = np.reshape(img_array, (shape[1], shape[2]))  # 获取array中的height和width
           high_window = np.max(img_array)
           low_window = np.min(img_array)

           lungwin = np.array([low_window * 1., high_window * 1.])
           newimg = (img_array - lungwin[0]) / (lungwin[1] - lungwin[0])  # 归一化
           newimg = (newimg * 255).astype('uint8')  # 将像素值扩展到[0,255]

           filename = os.path.split(file)[-1]
           jpgpath2 = os.path.join(jpgpath, filename+".jpg")
           cv2.imwrite(jpgpath2, newimg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

p2p3Path2 = r"Path_P2P3-NonHCC40.csv"
dicompath=r"G:\SMART\PySMART\data3\DICOM\A001_353"
jpgpath = r"G:\SMART\PySMART\data3\DICOM\A001_353_Jpg"

dicom2jpg(dicompath, jpgpath)
