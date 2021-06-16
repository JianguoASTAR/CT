import SimpleITK as sitk

#2 加载DICOM切片序列文件的元数据
def readMetaDatafromDICOMSeries(dicompath):
    # 设置序列读取器
    series_reader = sitk.ImageSeriesReader()
    # 获取所有图像文件名
    fileNames = series_reader.GetGDCMSeriesFileNames(dicompath)
    # 将图像文件名列表载入序列读取器中
    series_reader.SetFileNames(fileNames)
    series_reader.MetaDataDictionaryArrayUpdateOn()
    series_reader.LoadPrivateTagsOn()
    images = series_reader.Execute()

    keylist = list()
    metaDataList=list()
    #获取第一个切片，的meta data的key
    mykeys = series_reader.GetMetaDataKeys(0)
    for k in mykeys:
        keylist.append(k)
    print(keylist)
    # 列出第一个切处的元数据(DICOM Tags)
    # keylist = ['0008|0020', '0008|0021', '0008|0022', '0008|0023', '0008|0030', '0008|0031', '0008|0032',
    #                        '0008|0033', '0008|103E', '0010|0010', '0010|0020', '0010|0030', '0010|0040', '0010|1010',
    #                        '0008|0080', '0028|0010', '0028|0011', '0028|1050', '0028|1051','0020|4000']

    metaDataList.append(keylist)
    #遍历每个slice
    for slice_num in range(len(fileNames)):
        metaData = list()
        #slice_num = 0
        #mykeys = series_reader.GetMetaDataKeys(slice_num)
        for tag in keylist:
            print(tag)
            if (series_reader.HasMetaDataKey(slice_num, tag)):
                metaData.append(series_reader.GetMetaData(slice_num, tag))
            else:
                metaData.append('')
        metaDataList.append(metaData)

    return metaDataList

#3 保存CT扫描文件路径
# 将List列表内容保存为csv文件
def writeData2CSV(data, filename):
    f = open(filename,'w')
    for d in data:
        f.write(str(d).replace('[','').replace(']','').replace('\'',''))
        f.write("\n")
    f.close()

dicompath= r"G:\SMART\PySMART\data3\DICOM\A001_353"
metaDataList = readMetaDatafromDICOMSeries(dicompath)
writeData2CSV(metaDataList, "../data3/MeatDataList4_fromDICOM.csv")



