#! /bin/bash

starting_path=$(pwd)

tests=$(ls -1 ./tests)
mkdir current-test
for current in $tests; do
    echo $current
    current="./tests/$current/*"
    cp $current ./current-test/
    cd ./current-test
    make

    mkdir src
    mv *.c *.h ./src &> /dev/null

    mkdir bins
    mv *.in *.out robocheck-test ./bins &> /dev/null
    zip -r test.zip ./src ./bins &> /dev/null

    rm -r ./bins
    rm -r ./src

    cd $starting_path
    python robocheck-core.py ./current-test/test.zip
    rm -r ./current-test/*
done
rm -r current-test
