"""configuration.py

    General description:
     This is the module that handles the configurations for Robocheck. It
    parses and helps the user generate the config.json.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
    (C) 2015, Constantin Mihalache <mihalache.c94@gmail.com>
                 last review 29.07.2015
"""

import json
import sys
import os
from coreutils import penaltyhandler, platformhandler

language = []
errorsToLookFor = []
penaltyFlag = []
penaltyDictionary = {}

def selectLanguage(languages):
    print 'Available languages:'
    for i in range(0, len(languages)):
        print i, languages[i]
    option = raw_input("Choice: ")
    print
    if len(option) is not 0 and option[0].isdigit():
        option = int(option[0])
        language = languages[option]
        return language
    else:
        print "You must enter a number!"
        return None

def selectErrorsToLookFor():
    try:
        errorListFile = open("ErrorList", "r")
    except IOError as e:
        print "ERROR: Missing ErrorList file for this language!"
        return None, None

    errors = errorListFile.readlines()
    errorListFile.close()
    if len(errors) is 0:
        print "ERROR: There are no tools implemented for this language yet!"
        return None ,None

    for i in range(0,len(errors)):
        errors[i] = errors[i].splitlines()[0]

    toLookFor = []
    print "Errors to look for:"
    padding = 2
    max_len = max(len(error) for error in errors) + padding
    for error in errors:
        spacing = ' '*(max_len-len(error))
        option = raw_input(error + spacing + "[Y/n]: ")
        if len(option) is not 0 and option[0] is 'N' or option is 'n':
            continue
        else:
            toLookFor.append(error)
    return errors, toLookFor

def checkConfiguration(language, errors, toLookFor):
    print "Your configuration: "
    print "Language: ", language
    print
    for error in errors:
        if error in toLookFor:
            print "[x]",
        else:
            print "[ ]",
        print error
    option = raw_input("\nIs this configuration correct? [Y/n]: ")
    if len(option) is not 0 and option is "N" or option is "n":
        return False
    return True

def writeConfigurationFile(filepath, language, toLookFor, penalty):
    config = open(filepath, 'w')
    jsonList = []
    jsonList.append( { 'Language': language, 'Errors': toLookFor, 'Penalty' : penalty } )
    config.write(json.dumps(jsonList, indent=2))
    config.close()

def createConfigFile(filepath):
    platformInstance = platformhandler.getInstance()
    platformInstance.clearScreen()
    returnPath = os.getcwd()
    languages = sorted(os.listdir('languages'), reverse=True)
    os.chdir('languages')

    language = selectLanguage(languages)
    if language is None:
        return False

    os.chdir(language)
    errors, toLookFor = selectErrorsToLookFor()
    os.chdir(returnPath)
    if toLookFor is None:
        return False

    platformInstance.clearScreen()
    if not checkConfiguration(language, errors, toLookFor):
        createConfigFile(filepath)
    else:
        option = raw_input("Do you want to add penalties for errors? [Y/n] ")
        if len(option) is not 0 and option is "N" or option is "n":
            penalty = False
        else:
            penalty = True
            toLookFor = penaltyhandler.penaltyConfig(toLookFor)
        writeConfigurationFile(filepath, language, toLookFor, penalty)

        print "\nRobocheck was succefully configured!"
        return True

def readConfigFile(filepath):
    global language
    global errorsToLookFor
    global penaltyFlag
    global penaltyDictionary

    try:
        configFile = open(filepath, 'r')
    except IOError as e:
        print "ERROR: Robocheck is not configured!"
        print "Please run robocheck-core.py --config to configure it!"
        return False

    config =json.load(configFile)
    language = config[0]['Language']
    penaltyFlag = config[0]['Penalty']
    if penaltyFlag is True:
        penaltyDictionary = config[0]['Errors']
        errorsToLookFor = penaltyhandler.getErrorsToLookFor(penaltyDictionary)
    else:
        errorsToLookFor = config[0]['Errors']
        penaltyDictionary = None
    return True

def getJson(errorList):
    global penaltyDictionary
    global penaltyFlag

    if penaltyFlag is True:
        return penaltyhandler.applyPenaltiesGetJson(errorList, penaltyDictionary)

    errorJsonList = []
    for err in errorList:
        errorJsonList.append( {
            'code': err.code,
            'sourceFile': err.sourceFile,
            'function': err.function,
            'line': err.line,
            })
    return errorJsonList

def getLanguage():
    global language
    return language

def getErrorsToLookFor():
    global errorsToLookFor
    return errorsToLookFor

def getPenaltyFlag():
    global penaltyFlag
    return penaltyFlag

def getPenaltyDictionary():
    global penaltyDictionary
    return penaltyDictionary
