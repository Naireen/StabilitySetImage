#!/bin/bash

#create all the csvs file

for i in {15..100}
do
    echo $i
    command="python collect_times.py $i"
    eval $command
done

