#读取所有Patient下的每个Series下的所有DICOM文件的元数据
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
def batchReadMetaData(filePath, saveBasePath):
    df = pd.read_csv(filePath, header=0, sep=",")  #PatientID,ScanID,Imagecount,Path
    i=2
    for index, row in df.iterrows():
        pID = df.loc[index, "PatientID"]
        dicompath = df.loc[index, "Path"]
        #读取元数据
        # 设置序列读取器
        series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(dicompath)
        # print("series ids:", series_ids)

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

            image_array = sitk.GetArrayFromImage(image3D)

            keylist = list(['0008|0030', '0008|0031', '0008|0032',
                            '0008|0033'])  # 只需要,,StudyTime, SeriesTime, AcquisitionTime和ContentTime

            metaDataList = list()
            metaDataList.append(keylist)
            # 遍历每个slice
            for slice_num in range(len(series_file_names)):
                metaData = list()
                metaData.append(series_file_names[slice_num])
                for tag in keylist:
                    # print(tag)
                    if (series_reader.HasMetaDataKey(slice_num, tag)):
                        metaData.append(series_reader.GetMetaData(slice_num, tag))
                    else:
                        metaData.append('')
                metaDataList.append(metaData)

            seriedescription = series_reader.GetMetaData(0, '0008|103e')  # 读取对应的Tag，0002开头的不能读写
            seriedescription = seriedescription.replace("/", "")  # 有些描述有"/"符号

            # 保存元数据
            savePath = os.path.join(saveBasePath, pID + "_" + seriedescription + ".csv")
            # 有的患者有两个相同的序列名称seriedescription，则防止被覆盖
            if (os.path.exists(savePath)):
                savePath = os.path.join(saveBasePath, pID + "_" + seriedescription + "_" + str(i) + ".csv")
                i = i + 1
            df_meta = pd.DataFrame(metaDataList)
            df_meta.to_csv(savePath, header=0, index=None)
            print("read meta data success:", savePath)


#2 批量执行元数据读取
batchReadMetaData(filePath, saveBasePath)


