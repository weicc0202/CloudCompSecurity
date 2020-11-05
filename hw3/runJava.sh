#!/bin/bash

hadoop fs -rm -r output
hadoop com.sun.tools.javac.Main freqCount.java
jar cf fc.jar freqCount*.class
hadoop jar fc.jar freqCount hw3 output
hadoop fs -getmerge output/ output/file.txt

