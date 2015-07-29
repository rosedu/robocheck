"""configurationTest.py

    General description:
     This is a unit test suite for the configuration module.
    (C) 2015, Constantin Mihalache <mihalache.c94@gmail.com>
                 last review 29.07.2015
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
    # suppress outputing to stdout and system('clear') method
    with open(os.devnull, "w") as devnull, mock.patch('os.system'):
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

@contextmanager
def mock_stdin(mockInput):
    # mock stdin with the mockList
    with mock.patch('__builtin__.raw_input') as m_stdin:
        m_stdin.side_effect = mockInput
        yield

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
        self.assertEqual(configuration.getLanguage(), "C")
        self.assertFalse(configuration.getPenaltyFlag())
        self.assertEqual(configuration.getErrorsToLookFor(),
            ['MEMORY LEAK', 'INVALID ACCESS', 'INVALID FREE'])

    def test_reading_2(self):
        # testing penalty configurations
        self.assertTrue(configuration.readConfigFile(os.path.join(self.testsDirectory,
            "configurationTestReading2.json")))
        self.assertEqual(configuration.getLanguage(), "C")
        self.assertTrue(configuration.getPenaltyFlag())
        self.assertEqual(configuration.getErrorsToLookFor(),
            ['UNITIALIZED VARIABLE USAGE', 'INVALID ACCESS', 'MEMORY LEAK',
            'INVALID FREE'])
        self.assertEqual(configuration.getPenaltyDictionary(),
        {'UNITIALIZED VARIABLE USAGE': {'Penalty': 7.0, 'Mode': 'S'},\
        'INVALID ACCESS': {'Penalty': 6.0, 'Mode': 'S'},\
        'MEMORY LEAK': {'Penalty': 5.0, u'Mode': 'S'},\
        'INVALID FREE': {'Penalty': 8.0, 'Mode': 'S'}})

    def test_writing_1(self):
        mockInput = ["1", "Y", "Y", "N", "Y", "Y", "Y", "N"]
        with mock_stdin(mockInput), suppress_stdout():
            configuration.createConfigFile(self.tempConfigFile)
        # check the generated file
        self.assertTrue(filecmp.cmp(self.tempConfigFile,
            os.path.join(self.testsDirectory, 'configurationTestWriting1.json'), shallow=False))

    def test_writing_2(self):
        mockInput = ['1', 'Y', 'Y', 'Y', 'N', 'Y', 'Y', 'Y',
            'S', '5.01', 'S', '4.3', 'S', '3', 'M', '2', '3.99', 'Y']
        with mock_stdin(mockInput), suppress_stdout():
            configuration.createConfigFile(self.tempConfigFile)
        self.assertTrue(filecmp.cmp(self.tempConfigFile,
            os.path.join(self.testsDirectory, 'configurationTestWriting2.json'), shallow=False))

if __name__ == '__main__':
    unittest.main()
