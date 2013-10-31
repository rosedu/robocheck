"""modulehandler.py

    General description:
     This is the module that dynamically loads the classes for the tools
    used to get the errors. The "getCompatibleModules" function loads
    all the classes for the language specified and instanciates only
    those which tool can search for the errors specified and which have
    the tool installed.

    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                     last review 26.08.2013
"""
import os
import sys

def getCompatibleModules(language, errorsToLookFor, platform):
    returnPath = os.getcwd()
    os.chdir("languages")
    os.chdir(language)
    allModules = os.listdir("modules")
    os.chdir("modules")
    sys.path.insert(0, ".")

    compatibleModules = []

    for module in allModules:
        if ".pyc" in module:
            allModules.remove(module)

    for i in range(0, len(allModules)):
        allModules[i] = allModules[i].split(".py")[0]

    for module in allModules:
        if module == "__init":
            continue
        tool = __import__(module)
        toolClass = getattr(tool, module)
        if toolClass.canHandleErrors(errorsToLookFor) and \
            toolClass.toolIsInstalled(platform):

            compatibleModules.append( toolClass() )

    os.chdir(returnPath)
    if len(compatibleModules) == 0:
        return None

    return compatibleModules
