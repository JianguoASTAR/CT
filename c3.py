#读取每个Patient下的每个Series下的所有DICOM文件的元数据
#功能与sta5类似

import SimpleITK as sitk
import pandas as pd
import os
import sys

#1 先运行sta1_image count，得到各个类的patient文件路径

filePath = r"G:\SMART\PySMART\data4_batch2\Path_HCC.csv"
#filePath = r"G:\SMART\PySMART\data4_batch2\Path_HCC Surveillance.csv"
#filePath = r"G:\SMART\PySMART\data4_batch2\Path_Non-HCC.csv"
saveBasePath = r"G:\SMART\PySMART\data4_batch2\Metadata\HCC"

#2 批量执行元数据读取
def batchReadMetaData(patientlist, pathlist, saveBasePath):
    df = pd.read_csv(filePath, header=0, sep=",")  #PatientID,ScanID,Imagecount,Path
    for index, row in df.iterrows():
        pID = df.loc[index, "PatientID"]
        dicompath = df.loc[index, "Path"]
        #读取元数据
        metaDataList, seriedescription = readMetaDatafromDICOMSeries2(dicompath)  #只读取一部分元数据
        #保存元数据
        savePath = os.path.join(saveBasePath, pID +"_"+ seriedescription+".csv")
        df_meta = pd.DataFrame(metaDataList)
        df_meta.to_csv(savePath, header=0, index=None)
        print("read meta data success:", savePath)

#3 加载DICOM切片序列文件的元数据
def readMetaDatafromDICOMSeries2(dicompath):
    # 设置序列读取器
    series_reader = sitk.ImageSeriesReader()
    # 获取所有图像文件名
    fileNames = series_reader.GetGDCMSeriesFileNames(dicompath)
    # 将图像文件名列表载入序列读取器中
    series_reader.SetFileNames(fileNames)
    series_reader.MetaDataDictionaryArrayUpdateOn()
    series_reader.LoadPrivateTagsOn()
    images = series_reader.Execute()

    keylist = list(['0008|0030','0008|0031','0008|0032','0008|0033'])  #只需要,,StudyTime, SeriesTime, AcquisitionTime和ContentTime
    metaDataList=list()
    metaDataList.append(keylist)
    #遍历每个slice
    for slice_num in range(len(fileNames)):
        metaData = list()
        metaData.append(fileNames[slice_num])
        for tag in keylist:
            #print(tag)
            if (series_reader.HasMetaDataKey(slice_num, tag)):
                metaData.append(series_reader.GetMetaData(slice_num, tag))
            else:
                metaData.append('')
        metaDataList.append(metaData)

    seriedescription = series_reader.GetMetaData(0, '0008|103e')  # 读取对应的Tag，0002开头的不能读写
    seriedescription = seriedescription.replace("/", "")  # 有些描述有"/"符号
    return metaDataList, seriedescription

#2 批量执行元数据读取
batchReadMetaData(filePath, saveBasePath)


