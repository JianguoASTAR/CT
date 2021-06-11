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

#2 将List列表内容保存为csv文件
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


#2 加载Multiple-Phases的文件清单
def load_Multiple_Phases_List(csvPath):
    with open(csvPath, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)
        #print(result[1])
        return result

multPhasesList = load_Multiple_Phases_List(csvPath)
print(len(multPhasesList))


#根据multPhasesList，遍历各患者文件夹并修改名称
def reNameFileName(multPhasesList, basePath):
    for f in multPhasesList:
        srcFile = os.path.join(basePath, f[0].strip(), f[1].strip(), f[3].strip())   #加.strip()是将前后空格去掉
        print("原始文件名:", srcFile)
        dstFile = os.path.join(basePath, f[0].strip(), f[1].strip(), f[4].strip())
        print("新文件名:", dstFile)
        try:
            os.rename(srcFile,dstFile)
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')

#删除多余的文件
def removeUnuseFiles(basePath):
    # 判断路径是否存在
    if (os.path.exists(basePath)):
        dirs_type = os.listdir(basePath)
        # 遍历每一个类别
        for dir_type in dirs_type:
            typePath = os.path.join(basePath, dir_type)
            dirs_patient = os.listdir(typePath)
            # 遍历每一个患者
            for dir_patient in dirs_patient:
                patientPath = os.path.join(typePath, dir_patient)
                files = os.listdir(patientPath)
                lista = ['P1.nrrd', 'P2.nrrd', 'P3.nrrd', 'P4.nrrd']
                for file in files:
                    if file not in lista:
                        os.remove(os.path.join(patientPath, file))

csvPath2 = r"G:\SMART\PySMART\data3\NrrdFileList_v2.csv"

multPhasesList = load_Multiple_Phases_List(csvPath2)
reNameFileName(multPhasesList, basePath)
#removeUnuseFiles(basePath)
