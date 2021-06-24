import zipfile
import zlib

def zipit(path, zipname):
    zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:

            p = os.path.join(root, file)
            print(p)
            zipf.write(p)
saveBasePath=r"C:\Users\i2r_account\PycharmProjects\SMARTProject2\mc"
#3 批量执行元数据读取
zipit(saveBasePath, "cc.zip")
