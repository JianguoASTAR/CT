#重命名JPG文件
import pandas as pd
import glob
import os
import shutil


def delFolder(p2p3Path2):
    df = pd.read_csv(p2p3Path2, header=0, sep=",")
    for index, row in df.iterrows():
        dicompath = df.iloc[index, 3]  # 获取第0行第0列(路径)
        dicompath = dicompath + "_jpg"
        shutil.rmtree(dicompath)
        #os.remove(dicompath)

def renameFile(p2p3Path2):
    df = pd.read_csv(p2p3Path2, header=0, sep=",")
    for index, row in df.iterrows():
        dicompath = df.iloc[index, 3]  # 获取第0行第0列(路径)
        dicompath = dicompath + "_jpg"
        #print(dicompath)
        fileList = glob.glob(dicompath + "/*")
        for file in fileList:

            filename = os.path.split(file)[-1]  #共8位，I1000000,I2000000, ..., I9000000, I1000001, I1100000, I1200000, ..., I1900000,I2000001,I2100000,
            filename = filename.split('.')[0]
            #print(filename)

            #先将每逢10的数（尾数为1） I1000001,的命名找出并重新命名
            if filename[-1]!="0" and len(filename)==8 :
                newname =int(filename[1:-1])  #取第1-7位的值并转为整数, 将第一位"I"和最后一位"1"去掉
                lastnumber = int(filename[-1])
                newname = delZero(str(newname))
                if lastnumber==1:
                    newname = int(newname) * 10
                elif lastnumber == 2:
                    newname = int(newname) * 100
                    #newname = "B"+newname
                elif lastnumber == 3:
                    #newname = int(newname) * 1000
                    newname = "C"+newname
                elif lastnumber == 4:
                    newname = "D"+newname
                elif lastnumber == 5:
                    newname = "E"+newname
                newname = str(newname)
                newname = newname.zfill(6)
                newname = newname+".jpg"
                print("oldname1:", filename, " newname:", newname)
                try:
                    os.rename(file, os.path.join(dicompath, newname))
                except:
                    print("false:")
            elif len(filename)==8:
                newname = int(filename[1:])  # 取第1-7位的值并转为整数, 将第一位"I"和最后一位"1"去掉
                newname = delZero(str(newname))
                newname = newname.zfill(6)
                newname = str(newname) + ".jpg"
                print("oldname2:", filename, " newname:", newname)
                try:
                    os.rename(file, os.path.join(dicompath, newname))
                except:
                    print("false:")

def renameFileDICOM(p2p3Path2):
    df = pd.read_csv(p2p3Path2, header=0, sep=",")
    for index, row in df.iterrows():
        dicompath = df.iloc[index, 3]  # 获取第0行第0列(路径)
        #dicompath = dicompath + "_jpg"
        #print(dicompath)
        fileList = glob.glob(dicompath + "/*")
        for file in fileList:

            filename = os.path.split(file)[-1]  #共8位，I1000000,I2000000, ..., I9000000, I1000001, I1100000, I1200000, ..., I1900000,I2000001,I2100000,
            filename = filename.split('.')[0]
            #print(filename)

            #先将每逢10的数（尾数为1） I1000001,的命名找出并重新命名
            if filename[-1]!="0" and len(filename)==8 :
                newname =int(filename[1:-1])  #取第1-7位的值并转为整数, 将第一位"I"和最后一位"1"去掉
                lastnumber = int(filename[-1])
                newname = delZero(str(newname))
                if lastnumber==1:
                    newname = int(newname) * 10
                elif lastnumber == 2:
                    newname = int(newname) * 100
                    #newname = "B"+newname
                elif lastnumber == 3:
                    #newname = int(newname) * 1000
                    newname = "C"+newname
                elif lastnumber == 4:
                    newname = "D"+newname
                elif lastnumber == 5:
                    newname = "E"+newname
                newname = str(newname)
                newname = newname.zfill(6)
                newname = newname+".dcm"
                print("oldname1:", filename, " newname:", newname)
                try:
                    os.rename(file, os.path.join(dicompath, newname))
                except:
                    print("false:")
            elif len(filename)==8:
                newname = int(filename[1:])  # 取第1-7位的值并转为整数, 将第一位"I"和最后一位"1"去掉
                newname = delZero(str(newname))
                newname = newname.zfill(6)
                newname = str(newname) + ".dcm"
                print("oldname2:", filename, " newname:", newname)
                try:
                    os.rename(file, os.path.join(dicompath, newname))
                except:
                    print("false:")


def renameFileDICOM2(p2p3Path2):
    df = pd.read_csv(p2p3Path2, header=0, sep=",")
    for index, row in df.iterrows():
        dicompath = df.iloc[index, 3]  # 获取第0行第0列(路径)
        #dicompath = dicompath + "_jpg"
        #print(dicompath)
        fileList = glob.glob(dicompath + "/*.jpg")
        for file in fileList:
            newname = file[0:-4]+".dcm"
            print("oldname2:", file, " newname:", newname)
            os.rename(file, os.path.join(dicompath, newname))

def delZero(name):
    if name[-1] !="0":
        return name
    else:
        name = name[:-1]
        return delZero(name)


p2p3Path2 = "path2.csv"
#delFolder(p2p3Path2)
#renameFile(p2p3Path2)
renameFileDICOM2(p2p3Path2)
