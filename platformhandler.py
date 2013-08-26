""" platformhandler.py

    General description:
     This is module that dynamically loads the classes for specific platforms.
    The OS name (contained in the string returned by platform.platform() 
    function), class and file where the class is written MUST have the same
    name. This classes contain implementations of functions that depend on
    the platform on which robocheck is running. The "getInstance" function
    creates an instance of a platform class. This instance can be used
    later in Visitor and Strategy like patterns.
    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                 last review 25.08.2013
"""

import os
import platform
import sys

def getInstance():
    platformInstance = None
    allSupportedPlatforms = os.listdir("platforms")
    returnPath = os.getcwd()
    os.chdir("platforms")
    sys.path.insert(0, ".")
    for i in range(1, len(allSupportedPlatforms)):
        allSupportedPlatforms[i] = allSupportedPlatforms[i].split(".py")[0]

    for platformName in allSupportedPlatforms:
        if platformName in platform.platform():
            myPlatformModule = __import__(platformName)
            myPlatformClass = getattr(myPlatformModule, platformName)
            platformInstance = myPlatformClass()
    os.chdir(returnPath)
    return platformInstance

