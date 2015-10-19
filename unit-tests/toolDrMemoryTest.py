"""toolDrMemoryTest.py

    General description:
     This is a unit test suite for the DrMemory module.
    (C) 2015, Constantin Mihalache <mihalache.c94@gmail.com>
                 last review 06.08.2015
"""

import os
import sys
import unittest
import subprocess
from coreutils import platformhandler
from coreutils.errors import *

class TestDrMemory(unittest.TestCase):
    @classmethod
    def importTool(cls, toolName):
        os.chdir('./languages/C/modules')
        tool = __import__(toolName)
        toolInstance = getattr(tool, toolName)
        os.chdir(cls.returnPath)
        return toolInstance()

    @classmethod
    def setUpClass(cls):
        global platformName
        cls.returnPath = os.getcwd()
        cls.toolInstance = cls.importTool('drmemory')
        cls.platformInstance = platformhandler.getInstance()
        cls.platformName = cls.platformInstance.__class__.__name__
        cls.sourceFolder = os.path.abspath('./unit-tests/sources')
        if cls.toolInstance.toolIsInstalled(cls.platformInstance) is False:
            print "Nothing to test! (tool not installed)"
            sys.exit(0)

    def compileCurrentTest(self, testFolderPath):
        os.chdir(testFolderPath)
        make_build = 1
        if self.platformName is 'Windows':
            make_build = subprocess.Popen(['nmake','/nologo','/f','Makefile','build'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if self.platformName is 'Linux':
            make_build = subprocess.Popen(['make','-f','GNUmakefile','build'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return make_build.wait() # returns exit code

    def cleanCurrentTempFiles(self):
        make_clean = 1
        if self.platformName is 'Windows':
            make_clean = subprocess.Popen(['nmake','/nologo','/f','Makefile','clean'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if self.platformName is 'Linux':
            make_clean = subprocess.Popen(['make','-f','GNUmakefile','clean'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        os.chdir(self.returnPath)
        return make_clean.wait() # returns exit code

    def tearDown(self):
        self.exitCode = self.cleanCurrentTempFiles()

    def test_all_errors_Linux_1(self):
        if self.platformName is not 'Linux':
            return self.skipTest('Linux test')

        errorList = ["MEMORY LEAK",
            "INVALID ACCESS",
            "UNITIALIZED VARIABLE USAGE",
            "INVALID FREE",
            "OPENED, BUT NOT CLOSED FILE DESCRIPTOR"]

        expectedOutput = [Error("INVALID ACCESS", "main.c", "main", "31"),
            Error("INVALID FREE", "main.c", "main", "33"),
            Error("UNITIALIZED VARIABLE USAGE", "main.c", "main", "33"),
            Error("INVALID ACCESS", "main.c", "invalid_acces_function", "10"),
            Error("UNITIALIZED VARIABLE USAGE", "main.c", "uninitialized_variable_usage_function", "17"),
            Error("INVALID FREE", "main.c", "main", "40"),
            Error("UNITIALIZED VARIABLE USAGE", "main.c", "main", "40"),
            Error("MEMORY LEAK", "main.c", "main", "29"),
            Error("MEMORY LEAK", "main.c", "invalid_acces_function", "8"),
            Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR", "main.c", "main", "24")]

        testFolderName = 'drmemoryTest01'
        testFolderPath = os.path.join(self.sourceFolder, testFolderName)
        exitCode = self.compileCurrentTest(testFolderPath)
        self.assertEqual(exitCode, 0, msg="Failed while trying to compile the test!")

        exes = ['robocheck-test']
        sources = ['main.c']
        exesPath = os.path.join(testFolderPath, 'exes')
        sourcesPath = testFolderPath

        toolOutput = self.toolInstance.runToolGetErrors(self.platformInstance, exes, sources,
            exesPath, sourcesPath, errorList)
        self.assertTrue(Error.identicalLists(expectedOutput, toolOutput), msg="The output is not as expected!")

    def test_all_errors_Windows_1(self):
        if self.platformName is not 'Windows':
            return self.skipTest('Windows test')

        errorList = ["MEMORY LEAK",
            "INVALID ACCESS",
            "UNITIALIZED VARIABLE USAGE",
            "INVALID FREE",
            "OPENED, BUT NOT CLOSED FILE DESCRIPTOR"]

        expectedOutput = [Error("INVALID ACCESS", "main.c", "main", "31"),
            Error("INVALID ACCESS", "main.c", "invalid_acces_function", "10"),
            Error("UNITIALIZED VARIABLE USAGE", "main.c", "uninitialized_variable_usage_function", "17"),
            Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR", "main.c", "main", "24"),
            Error("MEMORY LEAK", "main.c", "main", "29"),
            Error("MEMORY LEAK", "main.c", "invalid_acces_function", "8")]

        testFolderName = 'drmemoryTest01'
        testFolderPath = os.path.join(self.sourceFolder, testFolderName)
        exitCode = self.compileCurrentTest(testFolderPath)
        self.assertEqual(exitCode, 0, msg="Failed while trying to compile the test!")

        exes = ['robocheck-test.exe']
        sources = ['main.c']
        exesPath = os.path.join(testFolderPath, 'exes')
        sourcesPath = testFolderPath

        toolOutput = self.toolInstance.runToolGetErrors(self.platformInstance, exes, sources,
            exesPath, sourcesPath, errorList)
        self.assertTrue(Error.identicalLists(expectedOutput, toolOutput), msg="The output is not as expected!")

if __name__ == '__main__':
    unittest.main()
