#!/bin/bash

#output colors
green='\033[0;32m'
default='\033[0m'

#run all the unit-tests
testIndex=1
tests=$(ls ./unit-tests/ | grep '.py$' | grep -v '^__init__.py')
currentTest=$(echo $tests | cut -d ' ' -f $testIndex | cut -d '.' -f 1)
while [[ "$currentTest" != "" ]]; do
    printf "Test "$testIndex": "${green}$currentTest${default}"\n"
    echo "----------------------------------------------------------------------"
    python -m unit-tests.$currentTest -v
    let "testIndex++"
    currentTest=$(echo $tests | cut -d ' ' -f $testIndex | cut -d '.' -f 1)
done
