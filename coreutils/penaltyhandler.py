"""penaltyhandler.py

    General description:
     This is the module that manages everything regarding penalties;
    starting from configuration, up to adding the informations about
    penalties to the output.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
    (C) 2015, Constantin Mihalache <mihalache.c94@gmail.com>
            last rewiew: 29.07.2015
"""

import os
import sys

def confirmPenaltyConfigurations(penaltyDictionary):
    os.system('clear')

    padding = 2
    max_error_len = max(len(error) for error in penaltyDictionary) + padding
    spacing = ' '*(max_error_len-len('Error Type'))

    print 'Error Type',
    print spacing,
    print 'Mode[S/M]  ',
    print 'Occurences  ',
    print 'Penalty'
    print ''

    for error in penaltyDictionary:
        error_spacing = ' '*(max_error_len-len(error))
        print error,
        print error_spacing,
        penaltyConfig = penaltyDictionary[error]
        mode = penaltyConfig["Mode"]
        penalty = penaltyConfig["Penalty"]
        mode_spacing = ' '*(len('Mode[S/M]') - len(mode) + padding - 1)
        if mode == 'S':
            print 'S',
            print mode_spacing,
            occurance_spacing = ' '*(len('Occurences') + padding)
            print occurance_spacing,
        else:
            print 'M',
            print mode_spacing,
            occurence = penaltyConfig["Occurences"]
            occurance_spacing = ' '*(len('Occurences') - len(str(occurence)) + padding - 1)
            print occurence,
            print occurance_spacing,
        print penalty

    option = raw_input('\nIs this configuration correct? [Y/n] ')
    if len(option) is not 0 and option[0] != 'Y' and option[0] != 'y':
        return False
    else:
        return True

def penaltyConfig( errorsToLookFor ):
    penaltyDictionary = dict()
    os.system('clear')
    for error in errorsToLookFor:
        print error
        while True:
            mode = raw_input("\tMode[S/M]: ")
            if len(mode) is not 0:
                mode = mode[0].upper()
            if mode != "S" and mode != "M":
                print "Invalid option!"
            else:
                break

        if mode == "M":
            while True:
                occurence = raw_input("\tOccurences: ")
                if len(occurence) is not 0 and occurence.isdigit():
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
            penalty = raw_input("\tPenalty: ")
            try:
                penalty = float(penalty)
                if penalty < 0:
                    print "Invalid option! Need a float >= 0."
                else :
                    break
            except ValueError:
                print "Invalid option! Need a float number."
        if mode == 'S':
            penaltyDictionary[error] = dict([("Mode", mode), \
                                        ("Penalty", penalty)])
        else:
            penaltyDictionary[error] = dict([("Mode", mode), \
                                        ("Occurences", occurence), \
                                        ("Penalty", penalty)])
        print ''

    if confirmPenaltyConfigurations( penaltyDictionary) is True:
        return penaltyDictionary
    else:
        return penaltyConfig( errorsToLookFor )


def getErrorsToLookFor(penaltyDictionary):
    errorsToLookFor = []
    for error in penaltyDictionary:
        errorsToLookFor.append(error)

    return errorsToLookFor

def applyPenaltiesGetJson(errorsFound, penaltyDictionary):
    multiplePenalties = dict()
    errorJsonList = []
    for error in errorsFound:
        if penaltyDictionary[error.code]["Mode"] == "S":
            errorJsonList.append( {
                'code': error.code,
                'sourceFile': error.sourceFile,
                'function': error.function,
                'line': error.line,
                'penalty': penaltyDictionary[error.code]["Penalty"]
                })
        else :
            errorJsonList.append( {
                'code': error.code,
                'sourceFile': error.sourceFile,
                'function': error.function,
                'line': error.line,
                'penalty': 0.0
                })
            if error.code not in multiplePenalties:
                multiplePenalties[error.code] = 1
            else :
                multiplePenalties[error.code] += 1

    otherPenaltiesList = []
    for error in multiplePenalties:
        penalty = 0.0
        if multiplePenalties[error] > penaltyDictionary[error]["Occurences"]:
            penalty = penaltyDictionary[error]["Penalty"]
        otherPenaltiesList.append( {
                'code': error,
                'accepted': penaltyDictionary[error]["Occurences"],
                'found': multiplePenalties[error],
                'penalty': penalty
                })

    finalOutputJson = dict([("ErrorsFound", errorJsonList), ("OtherPenalties", otherPenaltiesList)])
    return finalOutputJson
