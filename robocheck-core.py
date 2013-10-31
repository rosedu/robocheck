"""robocheck-core.py

   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 30.10.2013
"""
import os
import sys
import json
import subprocess
import time
import zipfile

from coreutils.errors import *
from coreutils import configuration
from coreutils import platformhandler
from coreutils import modulehandler
from coreutils import penaltyhandler

def main():
    sys.path.insert(0, "platforms")
    sys.path.insert(0, os.getcwd())
    platformInstance = platformhandler.getInstance()
    if platformInstance is None:
        print "ERROR: Your OS is not supported by Robocheck"
        return

    if "--config" in sys.argv:
        configuration.createConfigFile()
        return
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

    platformInstance.zipExtractAll(sys.argv[1])

    errorJsonList = []
    returnPath = os.getcwd()
    os.chdir("current-test")
    sources = os.listdir('src')
    exes = os.listdir('bins')
    exesPath = "bins"

    errorList = []

    os.chdir(exesPath)
    for tool in tools:
        errors = tool.runToolGetErrors(platformInstance, exes, sources, errorsToLookFor)
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
    os.chdir(returnPath)

    jsonOutput = open('output.json', 'w')
    jsonOutput.write(json.dumps(errorJsonList, indent=2))
    jsonOutput.close()


if __name__ == '__main__':
   main()
