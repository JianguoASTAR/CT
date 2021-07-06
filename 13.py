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
        f.write(str(d).replace('[','').replace(']','').replace('\'',''))
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
        srcFile1 = os.path.join(basePath, f[0].strip(), f[1].strip(), f[2].strip()+".nrrd")   #加.strip()是将前后空格去掉
        srcFile2 = os.path.join(basePath, f[0].strip(), f[1].strip(), f[2].strip()+" .nrrd")  #有些文件名后面有空格
        print("原始文件名:", srcFile1)
        dstFile = os.path.join(basePath, f[0].strip(), f[1].strip(), f[3].strip()+"_"+f[1].strip()+".nrrd")
        print("新文件名:", dstFile)
        try:
            if (os.path.exists(srcFile1)):
                os.rename(srcFile1,dstFile)
                print('rename file success\r\n')
            elif (os.path.exists(srcFile2)):
                os.rename(srcFile2, dstFile)
                print('rename file success\r\n')
            else:
                print("file does not exist")
        except Exception as e:
            print(e)
            print('rename file fail\r\n')


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
                lista = ['P1', 'P2', 'P3', 'P4']
                for file in files:
                    fname = file[0:2]  #只获取前两个字符
                    print(fname)
                    if fname not in lista:
                        print("removing ", file)
                        os.remove(os.path.join(patientPath, file))

#删除当前目录下的空的子文件夹
def removeEmptyFolder(basePath):
    folders = list(os.walk(basePath))[1:]

    for folder in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        if not folder[2]:
            os.rmdir(folder[0])

csvPath2 = r"G:\SMART\PySMART\data3\NrrdFileList_v2.csv"

multPhasesList = load_Multiple_Phases_List(csvPath2)
reNameFileName(multPhasesList, basePath)
#removeUnuseFiles(basePath)

#basePath = r"c:\ct3_Cleandata\HCC"
#basePath = r"c:\ct3_Cleandata\HCC Surveillance"
#basePath = r"c:\ct3_Cleandata\non-HCC"
removeEmptyFolder(basePath)
