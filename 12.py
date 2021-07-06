#将同一文件夹中的多个series文件分别存储到单独的文件夹
import os
import pydicom
from pydicom.fileset import FileSet
import SimpleITK as sitk
from pydicom.dataset import Dataset
import pandas as pd
import sys
import numpy as np

filepath = r"../data3/H1_patientScanImageCount10.csv"
#1 读取患者扫描信息及文件路径
def loadScanPaths(filepath):
    df = pd.read_csv(filepath,header=0, sep=',')
    print(df.columns)
    patientList = df["PatientID"]
    scanList = df["ScanID"]
    imagecountList = df["Imagecount"]
    pathList= df["Path"]
    print(patientList)
    #print(pathList)
    #print(pathList)
    # print(pathList)

    return patientList, scanList, imagecountList, pathList

patientList, scanList, imagecountList, pathList = loadScanPaths(filepath)

#根据每个患者的扫描文件目录,将一个目录中有多个series的给分别存储
def saveSeries(patientList,pathList):
    for i in range(len(pathList)):
        dicompath= pathList[i]
        slices = [pydicom.filereader.dcmread(dicompath + '/' + s) for s in os.listdir(dicompath)]

        try:
            #创建一个序列列表
            fs = FileSet()
            for s in slices:
                #print(s[0x0008, 0x103E])
                fs.add(s)

            print(fs.find_values("PatientID"))   #['34958019', 'D010']
            fs.write("../data3/"+patientList[i])    #将多个序列保存为多个文件夹
            print("cover success:", pathList[i])
        except:
            print("cover failed:", pathList[i])

#saveSeries(patientList,pathList)


#3 生成NRRD文件
def saveNRRDBySimpleITK(patientList,scanList, pathList):
    for i in range(len(pathList)):
        dicompath= pathList[i].strip() #要去掉两边的空格
        print(dicompath)
        series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(dicompath)
        #print("series ids:", series_ids)

        if not series_ids:
            print("ERROR: given directory dose not a DICOM series.")
            sys.exit(1)
        for serie in series_ids:
            series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dicompath, serie)
            series_reader = sitk.ImageSeriesReader()
            series_reader.SetFileNames(series_file_names)
            image3D = series_reader.Execute()
            reader = sitk.ImageFileReader()
            reader.SetFileName(series_file_names[0])
            reader.ReadImageInformation()
            size = image3D.GetSize()
            print("Image size:", size[0], size[1], size[2])

            image_array = sitk.GetArrayFromImage(image3D)

            # SimpleITK读取的图像数据的坐标顺序为zyx，即从多少张切片到单张切片的宽和高；
            # 而据SimpleITK Image获取的origin和spacing的坐标顺序则是xyz

            origin = image3D.GetOrigin()
            spacing = image3D.GetSpacing()
            print("origin:", origin, " spacing:", spacing)
            img2 = sitk.GetImageFromArray(image_array)
            img2.SetOrigin(origin)
            s2 = spacing[2] * 1.5
            spacing2 = (spacing[0], spacing[1], s2)
            print(s2)
            img2.SetSpacing(spacing2)
            print(img2.GetSpacing())

            for k in reader.GetMetaDataKeys():
                v = reader.GetMetaData(k)
                img2.SetMetaData(k, v)

            seriedescription = reader.GetMetaData('0008|103e')  # 读取对应的Tag，0002开头的不能读写
            seriedescription = seriedescription.replace("/","")   #有些描述有"/"符号
            print(seriedescription)
            #ImageType = reader.GetMetaData('0008|0008')  # 读取对应的Tag，0002开头的不能读写
            ##img2.EraseMetaData('0008|0008')  # 删除Tag，更改的话可以不写
            #img2.SetMetaData('0008|0008', ImageType)  # 更改新dcm的Tag值
            #SOPClassUID = reader.GetMetaData('0008|0016')
            #img2.SetMetaData('0008|0016', SOPClassUID)

            #img2.SetMetaData('0008|0018', reader.GetMetaData('0008|0018'))

            #SeriesInstanceUID = reader.GetMetaData('0020|000e')  # 这个Tag改不了，保存时貌似会随机赋值
            #img2.SetMetaData('0020|000e', SeriesInstanceUID)
            if (not os.path.samestat('../data3/NRRD/'+patientList[i])):
                os.mkdir('../data3/NRRD/'+patientList[i])

            sitk.WriteImage(img2, '../data3/NRRD/'+patientList[i] +"/" +seriedescription+".nrrd")


saveNRRDBySimpleITK(patientList,scanList, pathList)


