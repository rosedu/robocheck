"""toolValgrindTest.py

    General description:
     This is a unit test suite for the Valgrind module.
    (C) 2015, Theodor Stoican <theo.stoican@gmail.com>
                 last review 22.08.2015
"""


import os
import sys
import unittest
import subprocess
from coreutils.errors import *
from coreutils import platformhandler

possibleErrors = ["MEMORY LEAK",
            "INVALID ACCESS",
            "UNITIALIZED VARIABLE USAGE",
            "INVALID FREE",
            "OPENED, BUT NOT CLOSED FILE DESCRIPTOR"]

class TestValgrind (unittest.TestCase):

    @classmethod
    def setUpClass (cls):
        cls.platform = platformhandler.getInstance()
        cls.exe = ['test01']
        cls.srcsPath = os.path.abspath('./unit-tests/sources')
        cls.test = 'ValgrindTest01'
        cls.tool = cls.importTool()
        cls.sources = 'testValgrind01.c'
        cls.exesPath = os.path.join (cls.srcsPath, cls.test,'exes')
    def setUp (self):
        self.exitCode =self.compileTest()
    def tearDown (self):
        process = ['make', 'clean']
        subprocess.Popen(process, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    @classmethod
    def importTool(cls):
	workingPath = os.getcwd()
        os.chdir('./languages/C/modules')
        tool = __import__ ('valgrind')
        toolInstance = getattr (tool, 'valgrind')
        os.chdir (workingPath)
        return toolInstance()
    def compileTest(self):
        process = []
        fullPath = os.path.join(self.srcsPath, self.test)
        os.chdir (fullPath)
        process.append('make')
        process.append('build')
        x = subprocess.Popen(process, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        return x.wait()

    def test_all_errors_1 (self):
	global possibleErrors
        expectedOutput = []
        expectedOutput.append(Error("INVALID ACCESS", "testValgrind01.c", "main", "19"))
        expectedOutput.append(Error("INVALID ACCESS","testValgrind01.c","main","21"))
	expectedOutput.append(Error("UNITIALIZED VARIABLE USAGE", "testValgrind01.c", "main","13"))
        expectedOutput.append(Error("INVALID FREE", "testValgrind01.c", "main", "23"))
	expectedOutput.append(Error("INVALID FREE", "testValgrind01.c", "main", "27"))
	expectedOutput.append(Error("OPENED, BUT NOT CLOSED FILE DESCRIPTOR","testValgrind01.c", \
		"main", "25"))
	expectedOutput.append(Error("MEMORY LEAK","testValgrind01.c", "allocateString", "8"))
        self.assertTrue (self.tool.toolIsInstalled(self.platform))
        self.assertEqual (self.exitCode, 0)
        ValgrindOutput = self.tool.runToolGetErrors(self.platform, self.exe, self.sources, \
		self.exesPath, self.srcsPath, possibleErrors)
	self.assertTrue (Error.identicalLists (ValgrindOutput, expectedOutput))        
if __name__ == '__main__':
    unittest.main()
