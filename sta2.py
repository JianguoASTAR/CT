import SimpleITK as sitk
import pandas as pd
import os

#3 批量执行元数据读取
def batchReadMetaData(p2p3Path, saveBasePath):
    df = pd.read_csv(p2p3Path, header=0, sep=",")  #PatientID,ScanID,Imagecount,Path
    for index, row in df.iterrows():
        pID = df.loc[index, "PatientID"]
        dicompath = df.loc[index, "Path"]
        #读取元数据
        metaDataList, seriedescription = readMetaDatafromDICOMSeries2(dicompath)  #只读取一部分元数据
        #保存元数据
        savPath = os.path.join(saveBasePath, pID +"_"+ seriedescription+".csv")
        df_meta = pd.DataFrame(metaDataList)
        df_meta.to_csv(savPath, header=0, index=None)


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
        for tag in keylist:
            print(tag)
            if (series_reader.HasMetaDataKey(slice_num, tag)):
                metaData.append(series_reader.GetMetaData(slice_num, tag))
            else:
                metaData.append('')
        metaDataList.append(metaData)

    seriedescription = series_reader.GetMetaData('0008|103e')  # 读取对应的Tag，0002开头的不能读写
    seriedescription = seriedescription.replace("/", "")  # 有些描述有"/"符号
    return metaDataList, seriedescription



#先执行sta7_splitP2P3，得到P2P3复制患者的路径列表，然后执行批量读取元数据
p2p3Path = r"G:\SMART\PySMART\data4_batch2\Path_P2P3.csv"
saveBasePath=r"G:\SMART\PySMART\data4_batch2"
#3 批量执行元数据读取
batchReadMetaData(p2p3Path, saveBasePath)
