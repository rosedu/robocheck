"""robocheck-core.py
   
   General description:
    This is the core of the program. It loads the modules, runs them, 
   receives a list of errors from each module and creates a json
   file with all the errors. 
   (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 26.07.2013
"""
import sys
import json
import subprocess

class Error:
    def __init__(self, code, sourceFile, function, line):
        self.code = code
        self.sourceFile = sourceFile
        self.function = function
        self.line = line


SOURCES = ["test1.c"]

def getFileFunctionLine( outputLine ):
    details = []
    
    fflNotSplited = outputLine.split(": ")[1]

    sourceFile = fflNotSplited.split(" (")[1].split(":")[0]
    if sourceFile not in SOURCES:
        return None

    function = fflNotSplited.split(" (")[0]
    line = fflNotSplited.split(":")[1].split(")")[0]
    
    details.append(sourceFile)
    details.append(function)
    details.append(line)
    return details
      

def getErrors(toolOutput):
    errorList = []
    nrLinesOutput = len(toolOutput)
    for i in range( nrLinesOutput ):
        if "bytes in" and "are definitely lost in loss record" in toolOutput[i]:
            for j in range(i+1, nrLinesOutput):
                if "by" not in toolOutput[j]  and "at" not in toolOutput[j]:
                    print toolOutput[j]
                    break
                ffl = getFileFunctionLine(toolOutput[j]) 
                if ffl is not None:
                    error = Error("MEMORY LEAK", ffl[0], ffl[1], ffl[2])
                    errorList.append(error)
                    break    
        if "Invalid write" in toolOutput[i]:
             ffl = getFileFunctionLine(toolOutput[i+1])
             error = Error("INVALID ACCESS", ffl[0], ffl[1], ffl[2])       
             errorList.append(error)
    return errorList   

def main():
   process = []
   process.append('valgrind')
   process.append('--leak-check=full')
   process.append('./tests/a.out')

   x = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   toolOutput = x.communicate()[1].splitlines()
   errors = getErrors(toolOutput)
   for err in errors:
       print err.code
       print err.sourceFile
       print err.function
       print err.line
       print    

if __name__ == '__main__':
    main()
