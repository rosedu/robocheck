""" drmemory.py

    General description:
     This is a module that checks for errors using  Dr Memory tool for programs 
    that are written in C. Compatible errors: Memory leak, Invalid access, 
    Invalid free, Unitialized variable usage, Open, but not closed 
    file descriptor. The function runToolGetErrors returns a list of
    instances of Error class, defined in Errors.py

    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 07.09.2013
"""

import os
import stat
import subprocess
from errors import *

compatibleErrors = ["MEMORY LEAK",
    "INVALID ACCESS",
    "UNITIALIZED VARIABLE USAGE",
    "INVALID FREE",
    "OPENED, BUT NOT CLOSED FILE DESCRIPTOR"]

sources = []

class drmemory:
    @staticmethod
    def toolIsInstalled(platform):
        return platform.toolIsInstalled("drmemory")

    @staticmethod
    def canHandleErrors(errorList):
        global compatibleErrors
        for error in errorList:
            if error in compatibleErrors:
                return True
        return False

    def getCompatibleErrorsToLookFor(self, errorList) :
        global compatibleErrors
        errorsToLookFor = []
        for error in errorList:
            if error in compatibleErrors:
                errorsToLookFor.append(error)

        return errorsToLookFor

    def getFileFunctionLine(self, outputLine):
        details = []
        if '~~Dr.M~~' not in outputLine:
            return None

        if '#' not in outputLine:
            return None
        try:
            fflNotSplited = outputLine.split("# ")[1]
            sourceFile = fflNotSplited.split('[')[1].split(':')[0].split(os.sep)
            sourceFile = sourceFile[len(sourceFile) - 1]
            if sourceFile not in sources:
                return None

            function = fflNotSplited.split(' ')[1]
            line = fflNotSplited.split(':')[1].split(']')[0]
        except IndexError:
            return None

        details.append(sourceFile)
        details.append(function)
        details.append(line)
        return details

    def getErrors(self, toolOutput, errorsToLookFor):
        global sources
        errorList = []
        nrLinesOutput = len(toolOutput)

        errorsToLookFor = self.getCompatibleErrorsToLookFor( errorsToLookFor )

        for i in range ( nrLinesOutput ):
            if '~~Dr.M~~' not in toolOutput[i]:
                continue
            error= None

            if 'LEAK' in toolOutput[i] and \
                '#' in toolOutput[i]:
                for j in range(i+1, nrLinesOutput):
                    if toolOutput[j] == '~~Dr.M~~ ':
                        break
                    ffl = self.getFileFunctionLine(toolOutput[j])
                    if ffl is not None:
                        error = Error("MEMORY LEAK", ffl[0], ffl[1], ffl[2])
                        break


            if 'UNADDRESSABLE ACCESS' in toolOutput[i]:
                for j in range(i+1, nrLinesOutput):
                    if toolOutput[j] == '~~Dr.M~~ ':
                        break

                    ffl = self.getFileFunctionLine(toolOutput[j])
                    if ffl is not None:
                        error = Error("INVALID ACCESS", ffl[0], ffl[1], ffl[2])
                        break

            if 'REACHABLE LEAK' in toolOutput[i]:
                for j in range(i+1, nrLinesOutput):
                    if toolOutput[j] == '~~Dr.M~~ ':
                        break
                    ffl = self.getFileFunctionLine(toolOutput[j])
                    if ffl is not None:
                        error = Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR", ffl[0], ffl[1], ffl[2])
                        break

            if 'UNINITIALIZED' in toolOutput[i]:
                for j in range(i+1, nrLinesOutput):
                    if toolOutput[j] == '~~Dr.M~~ ':
                        break
                    ffl = self.getFileFunctionLine(toolOutput[j])
                    if ffl is not None:
                        error = Error("UNITIALIZED VARIABLE USAGE", ffl[0], ffl[1], ffl[2])
                        break
            if 'INVALID HEAP ARGUMENT to free()' in toolOutput[i]:
                for j in range(i+1, nrLinesOutput):
                    if toolOutput[j] == '~~Dr.M~~ ':
                        break
                    ffl = self.getFileFunctionLine(toolOutput[j])
                    if ffl is not None:
                        error = Error("INVALID FREE", ffl[0], ffl[1], ffl[2])
                        break

            if error is not None and error not in  errorList:
                errorList.append(error)

        return errorList

    def runToolGetErrors(self, platform, exes, sourceFiles, errorList):
        global sources
        sources = sourceFiles

        process = []
        fullCommand = platform.getFullCommand("drmemory")
        process.append(fullCommand)
        process.append("-show_reachable")
        process.append("--")

        for exe in exes:
            exe = "."+ os.sep + exe
            if platform.isExecutable(exe) is False:
                continue

            process.append(exe)
            print process
            x = subprocess.Popen(process, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
            x.wait()

            toolOutput = x.communicate()[1].splitlines()
            errors = self.getErrors(toolOutput, errorList)
            process.remove(exe)

        return errors

