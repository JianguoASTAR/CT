#3 生成NRRD文件
def saveNRRDBySimpleITK(patientList,scanList, pathList):
    for i in range(len(pathList)):
        dicompath= pathList[i].strip() #要去掉两边的空格
        print(dicompath)
        series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(dicompath)
        #print("series ids:", series_ids)

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
            size = image3D.GetSize()
            print("Image size:", size[0], size[1], size[2])

            image_array = sitk.GetArrayFromImage(image3D)

            # SimpleITK读取的图像数据的坐标顺序为zyx，即从多少张切片到单张切片的宽和高；
            # 而据SimpleITK Image获取的origin和spacing的坐标顺序则是xyz

            origin = image3D.GetOrigin()
            spacing = image3D.GetSpacing()
            print("origin:", origin, " spacing:", spacing)
            img2 = sitk.GetImageFromArray(image_array)
            img2.SetOrigin(origin)
            s2 = spacing[2] * 1.5
            spacing2 = (spacing[0], spacing[1], s2)
            print(s2)
            img2.SetSpacing(spacing2)
            print(img2.GetSpacing())

            for k in reader.GetMetaDataKeys():
                v = reader.GetMetaData(k)
                img2.SetMetaData(k, v)

            seriedescription = reader.GetMetaData('0008|103e')  # 读取对应的Tag，0002开头的不能读写
            seriedescription = seriedescription.replace("/","")   #有些描述有"/"符号
            print(seriedescription)
            #ImageType = reader.GetMetaData('0008|0008')  # 读取对应的Tag，0002开头的不能读写
            ##img2.EraseMetaData('0008|0008')  # 删除Tag，更改的话可以不写
            #img2.SetMetaData('0008|0008', ImageType)  # 更改新dcm的Tag值
            #SOPClassUID = reader.GetMetaData('0008|0016')
            #img2.SetMetaData('0008|0016', SOPClassUID)

            #img2.SetMetaData('0008|0018', reader.GetMetaData('0008|0018'))

            #SeriesInstanceUID = reader.GetMetaData('0020|000e')  # 这个Tag改不了，保存时貌似会随机赋值
            #img2.SetMetaData('0020|000e', SeriesInstanceUID)
            if (not os.path.samestat('../data3/NRRD/'+patientList[i])):
                os.mkdir('../data3/NRRD/'+patientList[i])

            sitk.WriteImage(img2, '../data3/NRRD/'+patientList[i] +"/" +seriedescription+".nrrd")


saveNRRDBySimpleITK(patientList,scanList, pathList)
