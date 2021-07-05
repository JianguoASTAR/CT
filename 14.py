import glob
#根据Multiple-Phases的文件清单，对各个患者的Nrrd文件进行重命名，并删除多余文件
import os
import csv

nrrdPath=r"G:\SMART\Datasets\NRRDFiles_MultiPhases"
#nrrdPath=r"G:\SMART\Datasets\NRRDFiles_Contrast_MultiPhases"
csvPath=r"G:\SMART\PySMART\data\MultiplePhasesList.csv"

#1 获取各个nrrd文件名
def readNrrdFileName(basePath):
    pList = list()
    # 判断路径是否存在
    if (os.path.exists(basePath)):
        dirs_type = os.listdir(basePath)
        #print(dirs_type)
        # 遍历每一个类别(HCC, Non-HCC)
        for dir_type in dirs_type:
            dirs_patient = os.listdir(os.path.join(basePath,dir_type))
            #print(dirs_patient)
            # 遍历每个患者
            for dir_patient in dirs_patient:
                nrrdPath = os.path.join(basePath, dir_type, dir_patient)
                print(nrrdPath)
                fileList = glob.glob(nrrdPath + "/*.nrrd")
                for f in fileList:
                    fname = os.path.basename(f)
                    pList.append([dir_type, dir_patient, f, fname])
    print(pList)
    return pList

#3 保存CT扫描文件路径
# 将List列表内容保存为csv文件
def writeData2CSV(data, filename):
    f = open(filename,'w')
    for d in data:
        f.write(str(d).replace('[','').replace(']','').replace(' ','').replace('\'',''))
        f.write("\n")
    f.close()

basePath=r"G:\SMART\PySMART\data3\NRRD"
csvPath = r"G:\SMART\PySMART\data3\NrrdFileList.csv"
pList = readNrrdFileName(basePath)
writeData2CSV(pList, csvPath)
