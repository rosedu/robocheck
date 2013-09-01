""" Linux.py

    General description:
     This module contains the Linux class, which implements Linux
    platform specific functions.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                   last review 25.08.2013
"""

import subprocess

class Linux:
    def toolIsInstalled( self, cmd ):
       return subprocess.call("type " + cmd, shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def zipExtractAll(self, archivePath ):
        extractCmd = []
        extractCmd.append('unzip')
        extractCmd.append('-q')
        extractCmd.append('-d')
        extractCmd.append('current-test')
        extractCmd.append(archivePath)
        x = subprocess.Popen(extractCmd)
        x.wait()
