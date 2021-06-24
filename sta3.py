import os
import glob
import pandas as pd
import shutil

metaDataPath = r"G:\SMART\Datasets\6 CT Scans (batch 2)\MetaData 47"

#重命名P1P4
def reNameP1P4(metaDataPath):
    # 判断路径是否存在
    if (os.path.exists(metaDataPath)):
       fileList = glob.glob(metaDataPath + "/*.csv")
       for file in fileList:
           #通过文件名获取PatientID和序列名称
           #print(file)  #G:\SMART\Datasets\6 CT Scans (batch 2)\MetaData 47\0460dc48_POST CONTRAST ABD ASIR 2.5MM.csv
           filename = os.path.split(file)[-1]
           patientID = filename.split('_')[0]
           seriesName = filename.split('_')[1].replace(".csv","")
           #print("patientName:", patientID, "  seriesName:", seriesName)

           #打开文件,获取路径
           df = pd.read_csv(file, header=0, sep=",")
           #columns = df.columns.values.tolist()
           #print(columns)
           path = df.iloc[0, 0]  #获取第0行第0列(路径)
           times = df['0008|0033']
           times2 = list(set(times)) #去重
           print("path:",path, " times:", times2)

           #如果只有一种时间，则直接将文件夹名称重命名
           if(len(times2) == 1):
               sourePath = os.path.abspath(os.path.join(path, '..'))
               basePath = os.path.abspath(os.path.join(sourePath, '..'))
               if(seriesName[0:3] =="PRE"):
                   targetPath = os.path.join(basePath, 'P1')
               elif (seriesName[0:3] == "ART"):
                   targetPath = os.path.join(basePath, 'P2')
               elif (seriesName[0:3] == "DEL"):
                   targetPath = os.path.join(basePath, 'P4')

               print("sourePath:", sourePath)
               print("targetPath:", targetPath)
               os.rename(sourePath, targetPath)

           #如果有两种时间,则分别将每种时间的文件复制到单独一个文件夹，并重命名
           if(len(times2) ==2):
               times2.sort()#先排序
               #每一种时间
               sourePath = os.path.abspath(os.path.join(path, '..'))
               basePath = os.path.abspath(os.path.join(sourePath, '..'))

               newPath1 = os.path.join(basePath, 'P2')
               newPath2 = os.path.join(basePath, 'P3')
               #创建新文件夹
               if not os.path.exists(newPath1):
                 os.mkdir(newPath1)
               if not os.path.exists(newPath2):
                 os.mkdir(newPath2)

               #移动文件
               #C:\ct2_P2P3\HCC Surveillance\4fbec240\GA1JXMTI\JOGT2EB4/I1000000,165047,165309,165427,165436
               for index, row in df.iterrows():
                    path = df.iloc[index, 0]  # 获取第0行第0列(路径)
                    t= df.iloc[index,'0008|0033']
                    if(t == times2[0]):   #如果是第一个时间
                        shutil.move(path, newPath1)
                        #print(newPath1)
                    elif(t==times2[1]):  #如果是第二个时间
                        shutil.move(path, newPath2)
                        #print(newPath2)
               #删除空文件夹
               files = os.listdir(sourePath)
               if len(files)==0:
                   os.remove(sourePath)
reNameP1P4(metaDataPath)
