import zipfile
import os

def writeAllFileToZip(absDir, zipFile):
    for f in os.listdir(absDir):
        absFile = os.path.join(absDir, f)
        if os.path.isdir(absFile):
            relFile = absFile[len(os.getcwd())+1:]
            zipFile.write(relFile)
            writeAllFileToZip(absFile, zipFile)
        else:
            relFile = absFile[len(os.getcwd())+1:]
            zipFile.write(relFile)
    return
    
# zipFilePath = os.path.join(os.getcwd(),"test.zip") #zip文件路径
zipFilePath = 'demo_folder.zip'

with zipfile.ZipFile(zipFilePath ,'w', zipfile.ZIP_DEFLATED) as zipFile:

    absDir = os.path.abspath('demo_folder') #要压缩的文件夹绝对路径

    writeAllFileToZip(absDir, zipFile) #开始压缩

print("Done compressing!")