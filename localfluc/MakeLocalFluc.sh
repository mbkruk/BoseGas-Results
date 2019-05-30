#!/bin/sh

for FILE in `ls n*e*.txt`
do
	./LocalFluctuations.py $FILE
done
