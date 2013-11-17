"""robocheck-core.py

   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 17.11.2013
"""
import os
import sys
import json
import subprocess
import time
import zipfile
import shutil

from coreutils.errors import *
from coreutils import configuration
from coreutils import platformhandler
from coreutils import modulehandler
from coreutils import penaltyhandler

def init(pathToRobocheck):
    if os.sep in pathToRobocheck:
        path = pathToRobocheck[0]
        pathToRobocheck=pathToRobocheck[1:]
        if(pathToRobocheck[0] == os.sep):
            path += pathToRobocheck[0]
            pathToRobocheck=pathToRobocheck[1:]

        dirList = pathToRobocheck.split(os.sep)
        for i in range(len(dirList) -1):
            path += dirList[i] + os.sep

        os.chdir(path)

def cleanUp(platformInstance):
    if "current-robocheck-test" in os.listdir( platformInstance.getTempPath() ):
        shutil.rmtree(platformInstance.getTempPath() + "current-robocheck-test")

def getRemainingErrors(errorsToLookFor, errorsFound):
    for error in errorsFound:
        if error.code in errorsToLookFor:
            errorsToLookFor.remove(error.code)
    return errorsToLookFor

def helpMessage():
    print "Usage:"
    print "\t robocheck --config             - for configuring Robocheck"
    print "\t robocheck /path/to/ZipArchive  - for running Robocheck"

def main():
    callerPath = os.getcwd()

    init(sys.argv[0])
    sys.path.insert(0, "platforms")
    sys.path.insert(0, os.getcwd())
    returnPath = os.getcwd()
    platformInstance = platformhandler.getInstance()
    if platformInstance is None:
        print "ERROR: Your OS is not supported by Robocheck"
        return

    if len(sys.argv) != 2 or "--help" in sys.argv:
        helpMessage()
        exit()

    if "--config" in sys.argv:
        configuration.createConfigFile()
        return
    cleanUp(platformInstance)
    couldRead = configuration.readConfigFile()
    if couldRead is False:
        return

    language = configuration.getLanguage()
    penaltyFlag = configuration.getPenaltyFlag()

    if penaltyFlag is True:
        penaltyDictionary = configuration.getPenaltyDictionary()
        errorsToLookFor = penaltyhandler.getErrorsToLookFor(penaltyDictionary)
    else:
        errorsToLookFor = configuration.getErrorsToLookFor()



    tools = modulehandler.getCompatibleModules(language, errorsToLookFor, platformInstance)

    os.mkdir(platformInstance.getTempPath() + "current-robocheck-test")
    os.chdir(callerPath)
    platformInstance.zipExtractAll(sys.argv[1])


    platformInstance.cdToTemp()
    errorJsonList = []
    os.chdir("current-robocheck-test")
    sources = os.listdir('src')
    exes = os.listdir('bins')
    exesPath = "bins"
    srcsPath = 'src'

    errorList = []

    for tool in tools:
        errors = tool.runToolGetErrors(platformInstance, exes, sources, exesPath, srcsPath, errorsToLookFor)
        errorsToLookFor = getRemainingErrors(errorsToLookFor, errors)

        for err in errors:
            if err not in errorList:
                errorList.append(err)
    if penaltyFlag is True:
        errorJsonList = penaltyhandler.applyPenaltiesGetJson(errorList, penaltyDictionary)
    else:
        for err in errorList:
            errorJsonList.append( {
                'code': err.code,
                'sourceFile': err.sourceFile,
                'function': err.function,
                'line': err.line,
                })
        errorJsonList = dict([("ErrorsFound",errorJsonList)])

    print json.dumps(errorJsonList, indent=2)


    os.chdir(callerPath)
    jsonOutput = open('robocheck-output.json', 'w')
    jsonOutput.write(json.dumps(errorJsonList, indent=2))
    jsonOutput.close()

    cleanUp(platformInstance)

if __name__ == '__main__':
   main()
