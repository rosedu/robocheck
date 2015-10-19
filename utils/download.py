import urllib2
import os
import sys

"""
   Downloads the file from the url into the specified folder,
renaming it 'fileNae
"""
def downloadFile(folderPath, fileName, url):
    try:
        u = urllib2.urlopen(url)
        f = open(os.path.join(folderPath, fileName), 'wb')
        meta = u.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (fileName, fileSize)

        fileSizeDl = 0
        blockSz = 8192
        while True:
            buffer = u.read(blockSz)
            if not buffer:
                break

            fileSizeDl += len(buffer)
            f.write(buffer)
            status = "%3.2f%%" % (fileSizeDl * 100. / fileSize)
            status += chr(8)*(len(status)+1)
            print status,

        f.close()
    except Exception:
        print "\nCould not download the file to the specified location!"
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "\nUsage: python download.py [folderPath] [fileName] [url]"
        sys.exit(1)

    folderPath = os.path.abspath(sys.argv[1])
    fileName = sys.argv[2]
    url = sys.argv[3]

    downloadFile(folderPath, fileName, url)
