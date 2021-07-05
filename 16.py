
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

csvPath2 = r"G:\SMART\PySMART\data3\NrrdFileList_v2.csv"

multPhasesList = load_Multiple_Phases_List(csvPath2)
reNameFileName(multPhasesList, basePath)
#removeUnuseFiles(basePath)
