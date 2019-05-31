#!/bin/sh

for FILE in `ls n*e*.txt`
do
	./MakeXMax.py $FILE
done
