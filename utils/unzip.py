import zipfile
import sys
import os


"""
    Extracts the contents of the zip file located at 'zipPath'
into the folder located at 'folderPath'.
"""
def unzipToFolder(zipPath, folderPath):
    #try:
    zf = zipfile.ZipFile(zipPath)
    uncompress_size = sum((file.file_size for file in zf.infolist()))
    extracted_size = 0
    for file in zf.infolist():
        extracted_size += file.file_size
        #print "%s %%\r" % (extracted_size * 100/uncompress_size)
        status = "Unzip %3.2f%%" % (extracted_size * 100/uncompress_size)
        status += chr(8)*(len(status)+1)
        print status,
        zf.extract(file, folderPath)
    #except:
     #   print "\nCould not extract the zip file to the specified location."
      #  sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "\nUsage: python unzip.py [zipLocation] [folderLocation] "
        sys.exit(1)
        
    zipPath = os.path.abspath(sys.argv[1])
    folderPath = os.path.abspath(sys.argv[2])

    unzipToFolder(zipPath, folderPath)
