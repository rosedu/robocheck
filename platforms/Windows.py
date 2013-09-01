"""
    General description:
     This module contains the Windows class, which implements Windows
    platform specific functions.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 01.09.2013
"""
import os
import zipfile

class Windows:
    def toolIsInstalled(self, tool):
        for path in os.environ["PATH"].split(os.pathsep):
            filesInPath = os.listdir(path)
            for fileName in filesInPath:
                """not sure yet
                if tool in fileName and ".exe" in fileName
                    or tool in fileName and ".EXE in fileName:
                """
                if tool + ".exe" == fileName \
                    or tool + ".EXE" == fileName:
                    print path
                    print fileName
                    return True

        return False

    def zipExtractAll(self, archivePath):
        zipArchive = zipfile.ZipFile(archivePath)
        zipArchive.extractall("current-test")
