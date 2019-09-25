#!/bin/bash

echo "Generating random distribution data files"
cd csvs/random
python collect_all_times.py
cd random_features
ls > Order.txt

echo "Generating resonant distribution data files"
cd ../../resonant
python collect_all_times.py
cd resonant_features
ls > Order.txt

echo "Generating other distribution data files"
cd ../other
python collect_times.py 
