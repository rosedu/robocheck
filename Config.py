"""Config.py
    
    General description:
     This is the module that handles the configurations for Robocheck. It 
    parses and helps the user generate the ConfigFile.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 13.08.2013
"""
    
import json
import sys
import os

language = []
errorsToLookFor = []

def createConfigFile():
    os.system('clear')
    returnPath = os.getcwd()
    languages = os.listdir('languages')
    os.chdir('languages')

    toLookFor = []
    
    for i in range(0, len(languages)):
        print i, languages[i]
    
    option = sys.stdin.readline().splitlines()[0]
    if option.isdigit():
        option = int(option)
        language = languages[option]
    else:
        print "You must enter a number!"
        return False
    
    os.chdir(language)
    try:
        errorListFile = open("ErrorList", "r")
    except IOError as e:
        print "ERROR: Missing ErrorList file for this language!"
        return

    errors = errorListFile.readlines()
    if len(errors) == 0:
        print "ERROR: There are no tools implemented for this language yet!"
        return
    errorListFile.close()

    os.chdir(returnPath)
    for i in range(0, len(errors)):
        errors[i] = errors[i].splitlines()[0]
    

    print "Errors to look for:"
    for error in errors:
        print error,
        dim = (40 - len(error))/2
        for i in range(1,dim):
            print ' ',
        print "[y/N]: ",
        option = sys.stdin.readline().splitlines()[0]
        if option is "Y" or option is "y":
            toLookFor.append(error)
    os.system('clear')
    print "Your configuration: "
    print "Language: ", language
    print
    for error in errors:
        if error in toLookFor:
            print "[x]",
        else:
            print "[ ]",
        print error

    print "\nIs this configuration correct? [Y/n]:"
    option = sys.stdin.readline().splitlines()[0]
    if option is "N" or option is "n":
        createConfigFile()
    else:
        config = open('ConfigFile', 'w')
        jsonList = []
        jsonList.append( { 'Language': language, 'Errors': toLookFor} )
        config.write(json.dumps(jsonList, indent=2))
        config.close()      
        return True

def readConfigFile():
    global language
    global errorsToLookFor

    try:
        configFile = open('ConfigFile', 'r')
    except IOError as e:
        print "ERROR: Robocheck is not configured!"
        print "Please run robocheck-core.py --config to configure it!"
        return False 

    config =json.load(configFile)
    language = config[0]['Language']
    errorsToLookFor = config[0]['Errors']
    return True 

def getLanguage():
    global language
    return language

def getErrorsToLookFor():
    global errorsToLookFor
    return errorsToLookFor
