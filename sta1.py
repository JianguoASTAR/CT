#统计每个患者的每次Scan的图像数量
#遍历每个患者文件夹下的DICOM文件夹名称以及底层文件夹中的图像数量
import os

#1 删除无用文件
# 遍历所有目录,找到指定文件(.DS_Store, ._.DS_Store), 并删除
# 放在一开始执行,然后重新执行所有程序
def delDS_Store(basepath):
    for root, dirs, files in os.walk(basepath):
        for filename in files:
            if filename ==".DS_Store" or filename == "._.DS_Store" or filename =="Autorun.inf" or filename == "desktop.ini" or filename =="._Autorun.inf" or filename =="VERSION":
                os.remove(os.path.join(root, filename))


#2 获取CT扫描文件路径和文件数量
# 遍历文件夹,获取文件数量, 直到文件夹中全是文件,没有子文件夹
def getFolders(parentPath, childPathList):
    if len(childPathList)==0:
        childPathList = list()   #新整合的文件夹路径
    #判断路径是否存在
    if (os.path.exists(parentPath)):
        #获取子文件夹
        dirs_child =  os.listdir(parentPath)
        for childPath in dirs_child:
            childPath= os.path.join(parentPath,childPath)
            #如果当前路径是文件夹,则进一步前进遍历
            if (os.path.isdir(childPath)):
                #print("dirpath:", childPath)
                childPathList = getFolders(childPath, childPathList)
            else:  #如果当前路径不是文件夹,而是文件,则只记录当前路径(文件)所在的父级路径
                childPathList.append(parentPath)
    # 过滤掉重复的数据
    childPathList = list(set(childPathList))
    #  List排序 (默认按字母升序排列)
    childPathList.sort()
    print("路径数量:", len(childPathList))
    #print(childPathList)
    return childPathList

#3 保存CT扫描文件路径
# 将List列表内容保存为csv文件
def writeData2CSV(data, filename):
    f = open(filename,'w')
    for d in data:
        f.write(str(d).replace('[','').replace(']','').replace(' ','').replace('\'',''))
        f.write("\n")
    f.close()

#4 获取患者信息并统计CT图像数量
#childPathList: G:\SMART\PySMART\data3\OriginalData\A001\000\000\000\068\77\352
def getPatientScanIDs(basepath, childPathList):
    patientScanList = list() #保存Patient ID, Scan ID
    patientScanList.append(["PatientID", "ScanID", "Imagecount", "Path"])  #增加一个标题行
    for path in childPathList:
        item2 = path.replace(basepath, "")   #先将根目录去掉
        subitems = item2.split('\\')  #根据'\'字符切分
        patientID = subitems[1]   #找出第二个列表项,作为patient ID
        scanID = subitems[-1]     #找出最后一个列表项,作为scan ID
        if (len(patientID)>0) and len(scanID)>0:
            imagecount =len(os.listdir(path))
            if (imagecount>10):
                patientScanList.append([patientID, scanID, imagecount, path])
        else:  #如果有错,打印出来看一下
            print ("path:", item2)
            print("patientID:", patientID)
            print("scanID:", scanID)
    return patientScanList

basepath = r"G:\SMART\PySMART\data3\OriginalData"

#1 删除无用文件
delDS_Store(basepath)

#2 获取CT扫描文件路径和文件数量
childPathList=list()
childPathList = getFolders(basepath, childPathList)

#3 保存CT扫描文件路径
writeData2CSV(childPathList, "../data3/CTPathList_batch2.csv")

#4 获取患者信息并统计CT图像数量
patientScanList = getPatientScanIDs(basepath, childPathList)

#5 保存CT图像信息
writeData2CSV(patientScanList, "../data3/patientScanImageCount10.csv")
