#设置NRRD文件的对比度


from glob import glob
import os
import numpy as np
import SimpleITK as sitk

#1 批量调整NRRD文件的Window width和Window Center
def setContrastofNrrd(nrrdpath):
  # 判断路径是否存在
  if (os.path.exists(nrrdpath)):
    dir_patientlist = os.listdir(nrrdpath)
    # 遍历每一个患者
    for dir_patient in dir_patientlist:
      patientPath = os.path.join(nrrdpath, dir_patient)
      #定位到子文件夹
      patientPath = os.path.join(patientPath,"3 Clean_data (4 phases)-contrasted")
      if(os.path.exists(patientPath)):
          #遍历每个文件
          files = glob(patientPath + '/*.nrrd')
          for file in files:
             print(file)
             #调整单个NRRD文件的Window width和Window Center
             setContrastSingleNrrd(file)


#调整单个NRRD文件的Window width和Window Center
def setContrastSingleNrrd(file):
    img = sitk.ReadImage(file)
    img = sitk.GetArrayFromImage(img)

    # (1) 获取NRRD元数据的窗宽和窗高
    center, width = getCenterWidth(file)
    # (2) 根据窗宽和窗高重新计算对比度
    min, max, dFactor = calContrast(center, width)

    print("min:", min)
    print("max:", max)
    print("dFactor:", dFactor)

    try:
        #开始转换为图像
        (x, y, z) = img.shape
        #print(img.shape)
        newimage=np.zeros(img.shape)
        for i in range(z):  # z是图像的序列
          silce = img[:, :, i]  # 选择哪个方向的切片都可以
          silce = silce - min
          silce = np.trunc(silce * dFactor)
          silce[silce < 0.0] = 0
          silce[silce > 255.0] = 255  # 转换为窗位窗位之后的数据
          newimage[:,:,i] = silce

        #newimage = newimage.reverse()
        # newimage =newimage[::-1]
        out = sitk.GetImageFromArray(newimage)

        #设置元数据
        reader = sitk.ImageFileReader()
        reader.SetFileName(file)
        reader.LoadPrivateTagsOn()
        reader.ReadImageInformation()

        for k in reader.GetMetaDataKeys():
            v = reader.GetMetaData(k)
            out.SetMetaData(k, v)

        #设置切片间距
        img2 = reader.Execute()
        origin = img2.GetOrigin()
        spacing = img2.GetSpacing()
        print("origin:", origin, " spacing:", spacing)

        out.SetOrigin(origin)
        s2 = spacing[2] * 1.5
        spacing2 = (spacing[0], spacing[1], s2)
        print(s2)
        out.SetSpacing(spacing2)
        print(out.GetSpacing())

        os.remove(file)
        sitk.WriteImage(out, os.path.join(file[:-5] + '.nrrd'))

        print("保存成功:" + file)
    except Exception as e:
        print("转换失败:", file)
        print("出错原因：", e)

#3 获取NRRD元数据的窗宽和窗高
def getCenterWidth(scanPath):
    reader = sitk.ImageFileReader()
    reader.SetFileName(scanPath)
    reader.LoadPrivateTagsOn()
    reader.ReadImageInformation()

    center="50"
    width="350"
    if (reader.HasMetaDataKey("0028|1050")): #WindowCenter
       center = reader.GetMetaData("0028|1050")
    if (reader.HasMetaDataKey("0028|1051")):  # WindowWidth
       width = reader.GetMetaData("0028|1051")

    center1=50
    width1=350
    if ('\\' in center and center.index('\\') > -1):
        center1 = int(center[0:center.index('\\')])
    elif ('.' in center and center.index('.') > -1):
        center1 = int(center[0:center.index('.')])
    else:
        center1 = int(center)

    if ('\\' in width and width.index('\\') > -1):
        width1 = int(width[0:width.index('\\')])
    elif ('.' in width and width.index('.') > -1):
        width1 = int(width[0:width.index('.')])
    else:
        width1 = int(width)
    print("center:", center)
    print("width:", width)
    return center1, width1

#4 根据窗宽和窗高重新计算对比度
def calContrast(center, width):
    #转换成窗宽窗位
    min = (2 * center - width) / 2.0 + 0.5
    max = (2 * center + width) / 2.0 + 0.5
    dFactor = 255.0 / (max - min)
    print("min:", min)
    print("max:", max)
    print("dFactor:", dFactor)
    return min, max, dFactor


#nrrdpath = r'G:\SMART\Datasets\NRRDFiles_Contrast'
nrrdpath = os.path.normpath(r'G:\SMART\Datasets\1 CT Scans')

setContrastofNrrd(nrrdpath)
