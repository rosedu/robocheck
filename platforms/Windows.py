"""
    General description:
     This module contains the Windows class, which implements Windows
    platform specific functions.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 07.09.2013
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

    def getFullCommand(self, cmd):
        return cmd

    def isExecutable(self, cmd):
        if len(cmd) < 5:
            return False

        if cmd[len(cmd)- 3 - 1 :] == '.exe':
            return True

        return False

    def getTempPath(self):
        temp = os.system("echo %TEMP%").split(";")[0] + os.sep
        return temp

    def zipExtractAll(self, archivePath):
        temp = getTempPath()
        zipArchive = zipfile.ZipFile(archivePath)
        zipArchive.extractall(temp + "current-robocheck-test")


    def cdToTemp(self):
        temp = getTempPath()
        os.chdir(temp)
