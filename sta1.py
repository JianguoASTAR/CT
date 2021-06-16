import os
import SimpleITK as sitk
#读取由ITK-SNAP软件手动保存的所有nrrd文件的元数据,并保存为CSV文件

basePath=r"G:\SMART\PySMART\data3\NRRD"
nrrdFilePath = r"G:\SMART\PySMART\data3\NRRD\HCC\A001\P1.nrrd"

#获取一个NRRD文件的元数据
def readAllMetaKey(nrrdFilePath):
    keylist =list()
    reader = sitk.ImageFileReader()
    reader.SetFileName(nrrdFilePath)
    reader.LoadPrivateTagsOn()
    reader.ReadImageInformation()

    #遍历所有keys
    for k in reader.GetMetaDataKeys():
        keylist.append(k)
    return keylist


# 2.2 从路径字符串中直接获取Site ID、Patient ID, Scan ID。
def readAllNrrdMetaData(nrrdpath, keylist):
    metaDataList = list()
    # 判断路径是否存在
    if (os.path.exists(nrrdpath)):
        dirs_site = os.listdir(nrrdpath)
        # 遍历每一个站点(类别)
        for dir_site in dirs_site:
            sitePath = os.path.join(nrrdpath, dir_site)
            dirs_patient = os.listdir(sitePath)
            # 遍历每一个患者
            for dir_patient in dirs_patient:
                patientPath = os.path.join(sitePath, dir_patient)
                dirs_scan = os.listdir(patientPath)
                # 遍历每一个Scan文件(nrrd)
                for dir_scan in dirs_scan:
                    scanPath = os.path.join(patientPath, dir_scan)
                    # 调用函数,读取每个Scan文件(nrrd格式)的元数据
                    metaData = readMetaDatafromNrrd(scanPath, keylist)
                    # 将Site ID, Patient ID, Scan ID和读取到的元数据合成一个list
                    metaDataItem = [dir_site, dir_patient, dir_scan]
                    # 将两个list合并成一个
                    metaDataItem.extend(metaData)
                    metaDataList.append(metaDataItem)
    #定义元数据的key code和key name,并插入到列表的头部
    metaDataHeadCode = ['SiteID','PatientID','ScanID']
    metaDataHeadCode = metaDataHeadCode+keylist
    metaDataList.insert(0, metaDataHeadCode)
    return metaDataList


#使用SimpleITK读取nrrd和nii.gz元数据
def readMetaDatafromNrrd(scanPath, keylist):
    metaData = list()
    reader = sitk.ImageFileReader()

    reader.SetFileName(scanPath)
    reader.LoadPrivateTagsOn()

    reader.ReadImageInformation()

    #遍历所有keys
    #for k in reader.GetMetaDataKeys():
    #    v = reader.GetMetaData(k)
    #    print(f"({k}) = = \"{v}\"")

    #print(f"Image Size: {reader.GetSize()}")
    #print(f"Image PixelType: {sitk.GetPixelIDValueAsString(reader.GetPixelID())}")

    #获取指定要读取的项的名称
    for tag in keylist:
        if(reader.HasMetaDataKey(tag)):
            metaData.append(reader.GetMetaData(tag))
        else:
            metaData.append('')
    return metaData

#3 保存CT扫描文件路径
# 将List列表内容保存为csv文件
def writeData2CSV(data, filename):
    f = open(filename,'w')
    for d in data:
        f.write(str(d).replace('[','').replace(']','').replace('\'',''))
        f.write("\n")
    f.close()

#获取一个NRRD文件的元数据
keylist = readAllMetaKey(nrrdFilePath)

metaDataList = readAllNrrdMetaData(basePath, keylist)
writeData2CSV(metaDataList, "../data3/MeatDataList3_fromNrrd.csv")
