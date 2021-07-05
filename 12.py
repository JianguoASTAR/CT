#将同一文件夹中的多个series文件分别存储到单独的文件夹
import os
import pydicom
from pydicom.fileset import FileSet
import SimpleITK as sitk
from pydicom.dataset import Dataset
import pandas as pd

filepath = r"../data3/patientScanImageCount10.csv"
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

saveSeries(patientList,pathList)
