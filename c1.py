from PIL import Image
import os.path
import glob
def convertjpg(jpgfile,outdir,width=1280,height=1024):
    img=Image.open(jpgfile)
    new_img=img.resize((width,height),Image.BILINEAR)
    new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
for jpgfile in glob.glob("/home/yo/caffe/myproject/zte/test_set/*.jpg"):
    convertjpg(jpgfile,"/home/youname/mycode/cv/set")uname
