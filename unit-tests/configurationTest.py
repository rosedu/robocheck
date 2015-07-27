"""configurationTest.py

    General description:
     This is a unit test suite for the configuration module.
    (C) 2015, Constantin Mihalache <mihalache.c94@gmail.com>
                 last review 27.07.2015
"""

import os
import mock
import sys
import io
import filecmp
import unittest
from contextlib import contextmanager
from coreutils import configuration

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.configFile = os.path.abspath("config.json")
        self.testsDirectory = os.path.abspath("./unit-tests")
        self.tempConfigFile = os.path.abspath("./tempConfigFile.json")

    def tearDown(self):
        if os.path.exists(self.tempConfigFile):
            os.remove(self.tempConfigFile)

    def test_reading_1(self):
        self.assertTrue(configuration.readConfigFile(os.path.join(self.testsDirectory,
            "configurationTestReading1.json")))
        self.assertEqual(configuration.getLanguage(), "C");
        self.assertFalse(configuration.getPenaltyFlag())
        self.assertEqual(configuration.getErrorsToLookFor(),
            ['MEMORY LEAK', 'INVALID ACCESS', 'INVALID FREE'])

    def test_writing_1(self):
        # mock stdin with the side_effect list
        with mock.patch('sys.stdin') as m_stdin:
            m_stdin.readline.side_effect = ["1", "Y", "Y", "N", "Y", "Y", "Y", "N"]
            # suppress outputing to stdout and system('clear') method
            with suppress_stdout(), mock.patch('os.system') as m_system:
                configuration.createConfigFile(self.tempConfigFile)
        # check the generated file
        self.assertTrue(filecmp.cmp(self.tempConfigFile,
            os.path.join(self.testsDirectory, 'configurationTestWriting1.json'), shallow=False))

if __name__ == '__main__':
    unittest.main()
