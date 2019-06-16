#!/bin/sh

for FILE in `ls data/n*e*.txt`
do
	./LocalFluctuations.py $FILE
done
