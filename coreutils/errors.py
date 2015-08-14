""" Errors.py

    General description:
     This is the class used for standardize the erros found by the modules.
    Each module returns a list containing instances of Error class.

    (C) 2013, Andrei Tuicu <andrei.tuicu@gmail.com>
                last review 05.08.2013
"""

class Error:
    code = -1
    sourceFile = -1
    function = -1
    line = -1
    def __init__(self, code, sourceFile, function, line):
        self.code = code
        self.sourceFile = sourceFile
        self.function = function
        self.line = line

    def __eq__(self, other):
        if isinstance(other, Error):
            result = False
            if self.code == other.code \
                and self.sourceFile == other.sourceFile \
                and self.function == other.function \
                and self.line == other.line:

                result = True
            return result
        return NotImplemented

    def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result

    @staticmethod
    def identicalLists(list1, list2):
        # O(N*log N); N=len(list1)
        if len(list1) != len(list2):
            return False
        list1 = sorted(list1, key=lambda x: (x.code, x.sourceFile, x.function, x.line))
        list2 = sorted(list2, key=lambda x: (x.code, x.sourceFile, x.function, x.line))
        sameErrors = True
        for index in range(0, len(list1)):
            if list1[index] != list2[index]:

                sameErrors = False
                break
        return sameErrors
