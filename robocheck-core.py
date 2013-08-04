"""robocheck-core.py
   
   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   file with all the errors. 
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 05.08.2013
"""
import os
import sys
import json
import subprocess
import time
from Errors import *
import CValgrind


def main():
    extractCmd = []
    extractCmd.append('unzip')
    extractCmd.append('-q')
    extractCmd.append('-d')
    extractCmd.append('current-test/')
    extractCmd.append(sys.argv[1])
    x = subprocess.Popen(extractCmd)
    time.sleep(0.5)

    errorJsonList = []    
    sources = os.listdir('./current-test/src')
    exes = os.listdir('./current-test/bins')
    exesPath = "./current-test/bins/"
    returnPath = os.getcwd()
    os.chdir(exesPath)
    errors = CValgrind.runToolGetErrors(exes, sources)
    for err in errors:
        errorJsonList.append( {
            'code': err.code,
            'sourceFile': err.sourceFile,
            'function': err.function,
            'line': err.line,
            })
    print json.dumps(errorJsonList, indent=2)
    
    jsonOutput = open('JsonOutput', 'w')
    jsonOutput.write(json.dumps(errorJsonList, indent=2))
    jsonOutput.close()

    os.chdir(returnPath)

if __name__ == '__main__':
    main()
