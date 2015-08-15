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
        os.chdir('./languages/C/modules');
        tool = __import__(toolName)
        toolInstance = getattr(tool, toolName)
        os.chdir(cls.returnPath)
        return toolInstance()

    @classmethod
    def setUpClass(cls):
        cls.returnPath = os.getcwd()
        cls.toolInstance = cls.importTool('drmemory')
        cls.platformInstance = platformhandler.getInstance()
        cls.platformInstance.getArchitecture()
        cls.sourceFolder = os.path.abspath('./unit-tests/sources')
        cls.tests = ['drmemoryTest01'] # add test folders here
        cls.currentPath = None
        cls.currentTest = 0
        cls.exitCode = 0
        if cls.toolInstance.toolIsInstalled(cls.platformInstance) is False:
            print "Nothing to test! (tool not installed)"
            sys.exit(0);

    def compileCurrentTest(self):
        testFolderName = self.tests[self.currentTest]
        self.currentPath = os.path.join(self.sourceFolder,testFolderName)
        os.chdir(self.currentPath)
        make_build = subprocess.Popen(['make','build'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return make_build.wait() # returns exit code

    def cleanCurrentTempFiles(self):
        make_clean = subprocess.Popen(['make', 'clean'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        os.chdir(self.returnPath)
        self.currentPath = None
        return make_clean.wait() # returns exit code

    def setUp(self):
        self.exitCode = self.compileCurrentTest()

    def tearDown(self):
        self.exitCode = self.cleanCurrentTempFiles()
        self.currentTest = self.currentTest+1

    def test_all_errors_1(self):
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

        exes = ['robocheck-test']
        sources = ['main.c']
        exesPath = os.path.join(self.currentPath, 'exes')
        sourcesPath = self.currentPath

        self.assertEqual(self.exitCode, 0)
        toolOutput = self.toolInstance.runToolGetErrors(self.platformInstance, exes, sources,
            exesPath, sourcesPath, errorList)
        self.assertTrue(Error.identicalLists(expectedOutput, toolOutput))

if __name__ == '__main__':
    unittest.main()
