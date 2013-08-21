""" CValgrind.py

    General description:
     This is a module that check for errors using  Valgrind tool for programs 
    that are written in C. Compatible errors: Memory leak, Invalid access, 
    Invalid free, Unitialized variable usage, Open, but not closed 
    file descriptor. The function runToolGetErrors returns a list of
    instances of Error class, defined in Errors.py

    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 05.08.2013
"""

import subprocess
from Errors import *
compatibleErrors = [ "MEMORY LEAK",
    "INVALID ACCESS",
    "UNITIALIZED VARIABLE USAGE",
    "INVALID FREE",
    "OPENED, BUT NOT CLOSED FILE DESCRIPTOR"]

sources = []

def canHandleErrors( errorList ):
    global compatibleErrors
    for error in errorList:
        if error in compatibleErrors:
            return True
    return False


def getFileFunctionLine( outputLine ):
    details = []
    if ": " not in outputLine:
        return None
    if "at " not in outputLine and "by " not in outputLine:
        return None
    if "exit" in outputLine:
        return None

    fflNotSplited = outputLine.split(": ")[1]

    sourceFile = fflNotSplited.split(" (")[1].split(":")[0]
    if sourceFile not in sources:
        return None

    function = fflNotSplited.split(" (")[0]
    line = fflNotSplited.split(":")[1].split(")")[0]

    details.append(sourceFile)
    details.append(function)
    details.append(line)
    return details

def getCompatibleErrorsToLookFor( errorList ) :
    global compatibleErrors
    errorsToLookFor = []
    for error in errorList:
        if error in compatibleErrors:
            errorsToLookFor.append( error )
    return errorsToLookFor


def getErrors(toolOutput, errorsToLookFor):
    errorList = []
    nrLinesOutput = len(toolOutput)

    errorsToLookFor = getCompatibleErrorsToLookFor( errorsToLookFor )
    print errorsToLookFor
    for i in range( nrLinesOutput ):
        error = None
        if "bytes in" and "are definitely lost in loss record" in toolOutput[i] and \
            "MEMORY LEAK" in errorsToLookFor :

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j]) 
                if ffl is not None:
                    error = Error("MEMORY LEAK", ffl[0], ffl[1], ffl[2])
                    break


        if "Invalid write" in toolOutput[i] and \
            "INVALID ACCESS" in errorsToLookFor \
            or "Invalid read" in toolOutput[i] and \
            "INVALID ACCESS" in errorsToLookFor :

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("INVALID ACCESS", ffl[0], ffl[1], ffl[2])
                    break


        if "Uninitialised value was created" in toolOutput[i] and \
            "UNITIALIZED VARIABLE USAGE" in errorsToLookFor:

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("UNITIALIZED VARIABLE USAGE", ffl[0], ffl[1], ffl[2])
                    break


        if "Invalid free" in toolOutput[i] and \
            "INVALID FREE" in errorsToLookFor :

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("INVALID FREE", ffl[0], ffl[1], ffl[2])
                    break


        if "Open file descriptor" in toolOutput[i] \
            and "<inherited from parent>" not in toolOutput[i+1] and \
            "OPENED, BUT NOT CLOSED FILE DESCRIPTOR" in errorsToLookFor :

            for j in range(i+1, nrLinesOutput):
                ffl = getFileFunctionLine(toolOutput[j])
                if ffl is not None:
                    error = Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR", ffl[0], ffl[1], ffl[2])
                    break

        if error is not None and error not in errorList:
            errorList.append(error)

    return errorList


def runToolGetErrors(exes, sourceFiles, errorList):
    global sources
    global compatibleErrors

    sources = sourceFiles
    process = []
    process.append('valgrind')
    process.append('--leak-check=full')
    process.append('--track-origins=yes')
    process.append('--track-fds=yes')

    errorJsonList = []
    for exe in exes:
        exe = "./" + exe
        process.append(exe)
        print process
        x = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()
        process.remove(exe)
        if x.returncode != 0:
            continue
        toolOutput = x.communicate()[1].splitlines()
        errors = getErrors(toolOutput, errorList)
    return errors

