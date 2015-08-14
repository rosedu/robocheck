"""
    General description:
     This module contains the Windows class, which implements Windows
    platform specific functions.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 07.09.2013
"""
import os
import zipfile
import platform
import subprocess

class Windows:
    def toolIsInstalled(self, tool):
        for path in os.environ["PATH"].split(os.pathsep):
            try:
                filesInPath = os.listdir(path)
            except WindowsError:
                continue
            for fileName in filesInPath:
                """not sure yet
                if tool in fileName and ".exe" in fileName
                    or tool in fileName and ".EXE in fileName:
                """
                if tool + ".exe" == fileName \
                    or tool + ".EXE" == fileName:
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
        proc = subprocess.Popen(['echo', '%TEMP%'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        proc.wait()
        temp = proc.communicate()[0].splitlines()[0].split(";")[0] + os.sep
        return temp

    def zipExtractAll(self, archivePath):
        temp = self.getTempPath()
        zipArchive = zipfile.ZipFile(archivePath)
        zipArchive.extractall(temp + "current-robocheck-test")


    def cdToTemp(self):
        temp = self.getTempPath()
        os.chdir(temp)

    def getArchitecture(self):
        return platform.architecture()
