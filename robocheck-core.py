"""robocheck-core.py
   
   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 25.08.2013
"""
import os
import sys
import json
import subprocess
import time
from errors import *
import valgrind
import configuration
import platformhandler

def main():
    sys.path.insert(0, "platforms")
    platformInstance = platformhandler.getInstance()
    if platformInstance is None:
        print "ERROR: Your OS is not supported by Robocheck"

    if "--config" in sys.argv:
        configuration.createConfigFile()
        return
    couldRead = configuration.readConfigFile()
    if couldRead is False:
        return

    language = configuration.getLanguage()
    errorsToLookFor = configuration.getErrorsToLookFor()

    extractCmd = []
    extractCmd.append('unzip')
    extractCmd.append('-q')
    extractCmd.append('-d')
    extractCmd.append('current-test')
    extractCmd.append(sys.argv[1])
    x = subprocess.Popen(extractCmd)
    x.wait()

    errorJsonList = []
    returnPath = os.getcwd()
    os.chdir("current-test")
    sources = os.listdir('src')
    exes = os.listdir('bins')
    exesPath = "bins"
    os.chdir(exesPath)
    errors = valgrind.runToolGetErrors(exes, sources, errorsToLookFor)
    for err in errors:
        errorJsonList.append( {
            'code': err.code,
            'sourceFile': err.sourceFile,
            'function': err.function,
            'line': err.line,
            })
    print json.dumps(errorJsonList, indent=2)
    os.chdir(returnPath)

    jsonOutput = open('output.json', 'w')
    jsonOutput.write(json.dumps(errorJsonList, indent=2))
    jsonOutput.close()


if __name__ == '__main__':
   main()
