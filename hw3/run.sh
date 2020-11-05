#!/bin/bash

hadoop fs -rm -r output 

hadoop jar /usr/local/hadoop-2.7.0/share/hadoop/tools/lib/hadoop-streaming-2.7.0.jar \
-file mapper.py    -mapper mapper.py \
-file reducer.py   -reducer reducer.py \
-input hw3 -output output

hadoop fs -getmerge output/ output/file.txt
