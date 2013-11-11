""" Linux.py

    General description:
     This module contains the Linux class, which implements Linux
    platform specific functions.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                   last review 07.09.2013
"""

import subprocess
import getpass
import os

class Linux:
    def toolIsInstalled( self, cmd ):
        returnCode = subprocess.call("type " + cmd, shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
        if returnCode is True:
            return True

        bashrc = os.path.expanduser("~") + "/.bashrc"
        alias = "alias " + cmd

        grep = subprocess.Popen(["grep", alias, bashrc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep.wait()
        if grep.returncode != 0:
            return False

        fullCommand = grep.communicate()[0].splitlines()[0].split("=")[1]
        return self.toolIsInstalled(fullCommand)

    def getFullCommand(self, cmd ):
        if subprocess.call("type " + cmd, shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0 :
            return cmd

        bashrc = os.path.expanduser("~") + "/.bashrc"
        alias = "alias " + cmd

        grep = subprocess.Popen(["grep", alias, bashrc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep.wait()

        fullCommand = grep.communicate()[0].splitlines()[0].split("=")[1]
        fullCommand = fullCommand.split('"')[1]

        return fullCommand

    def isExecutable(self, fileName):
        return os.access(fileName, os.X_OK)

    def zipExtractAll(self, archivePath ):
        extractCmd = []
        extractCmd.append('unzip')
        extractCmd.append('-q')
        extractCmd.append('-d')
        extractCmd.append('/tmp/current-robocheck-test')
        extractCmd.append(archivePath)
        x = subprocess.Popen(extractCmd)
        x.wait()

    def getTempPath(self):
        return "/tmp/"

    def cdToTemp(self):
        os.chdir("/tmp")
