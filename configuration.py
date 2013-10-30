"""Config.py

    General description:
     This is the module that handles the configurations for Robocheck. It 
    parses and helps the user generate the config.json.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 13.08.2013
"""

import json
import sys
import os

language = []
errorsToLookFor = []

def confirmPenaltyConfigurations( penaltyDictionary ):
    os.system('clear')
    print 'Error Type',
    for i in range(15):
        print ' ',
    print 'Mode[S/M] ',
    print 'Occurences ',
    print 'Penalty'
    print ''

    for error in penaltyDictionary:
        print error,
        for i in range( (45-len(error))/2 ):
            print ' ',
        if penaltyDictionary[error][0] is None:
            print 'S',
            for i in range(4):
                print ' ',
            print ' ',
        else:
            print 'M',
            for i in range(4):
                print ' ',
            print penaltyDictionary[error][0],

        for i in range(4):
            print ' ',
        print penaltyDictionary[error][1]

    print '\nIs this configuration correct? [Y/n]',
    option = sys.stdin.readline().splitlines()[0]
    if option != 'N' and option != 'n':
        return True
    else:
        return False

def penaltyConfig( errorsToLookFor ):
    penaltyDictionary = dict()
    os.system('clear')
    for error in errorsToLookFor:
        print error
        while True:
            print "\tMode[S/M]:  ",
            mode = sys.stdin.readline().splitlines()[0].upper()
            if mode != "S" and mode != "M":
                print "Invalid option!"
            else:
                break

        if mode == "M":
            while True:
                print "\tOccurences: ",
                occurence = sys.stdin.readline().splitlines()[0]
                if occurence.isdigit():
                    occurence = int(occurence)
                    if occurence <= 0:
                        print "Invalid option! Need a number > 0."
                    else:
                        break
                else:
                    print "Invalid option! Need a number."
        else:
            occurence = None


        while True:
            print "\tPenalty:    ",
            penalty = sys.stdin.readline().splitlines()[0]
            try:
                penalty = float(penalty)
                if penalty < 0:
                    print "Invalid option! Need a float >= 0."
                else :
                    break
            except ValueError:
                print "Invalid option! Need a float number."
        penaltyDictionary[error] = [occurence, penalty]
        print ''

    if confirmPenaltyConfigurations( penaltyDictionary) is True:
        return penaltyDictionary
    else:
        return penaltyConfig( errorsToLookFor )


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
        print "[Y/n]: ",
        option = sys.stdin.readline().splitlines()[0]
        if option is "N" or option is "n":
            continue
        else:
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
        print "Do you want to add penalties for errors? [Y/n]"
        option = sys.stdin.readline().splitlines()[0]
        if option is "N" or option is "n":
            penalty = False
        else:
            penalty = True
            toLookFor = penaltyConfig( toLookFor )

        config = open('config.json', 'w')
        jsonList = []
        jsonList.append( { 'Language': language, 'Errors': toLookFor, 'Penalty' : penalty } )
        config.write(json.dumps(jsonList, indent=2))
        config.close()
        return True

def readConfigFile():
    global language
    global errorsToLookFor

    try:
        configFile = open('config.json', 'r')
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
