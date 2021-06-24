import csv
import pandas as pd
import os
import shutil

#将具有P2P3混合的患者的文件夹复制一份
def copyPatientFolder(sourceBasePath, newBasePath, patientListPath):
    df = pd.read_csv(patientListPath, header=0, sep=",")
    for index, row in df.iterrows():
        ty = df.loc[index, "Type"]
        pID = df.loc[index, "PatientID"]
        sourcePath = os.path.join(sourceBasePath, ty, pID)
        targetPath = os.path.join(newBasePath, ty, pID)

        if(os.path.exists(sourcePath)):
            shutil.copy(sourcePath, targetPath)
            print("copy succesful:", targetPath)
        else:
            print("Source Path does not exist:", sourcePath)

#将具有P2P3混合的患者的文件夹复制一份
sourceBasePath = r"G:\SMART\PySMART"
newBasePath = r"G:\SMART\PySMART"
patientListPath = r"G:\SMART\PySMART\data4_batch2\PatientList2_P2P3.csv"
copyPatientFolder(sourceBasePath, newBasePath, patientListPath)



