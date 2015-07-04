#! /bin/bash

tests=$(ls -1 ./tests)
mkdir current-test
for current in $tests; do
    echo $current
    current="./tests/$current/*"
    cp $current ./current-test/
    pushd ./current-test &> /dev/null
    make &> /dev/null

    mkdir src
    mv *.c *.h ./src &> /dev/null

    mkdir bins
    mv *.in *.out robocheck-test ./bins &> /dev/null
    zip -r test.zip ./src ./bins &> /dev/null

    rm -r ./bins
    rm -r ./src

    popd &> /dev/null
    python robocheck-core.py ./current-test/test.zip
    rm -r ./current-test/*
done
rm -r current-test
