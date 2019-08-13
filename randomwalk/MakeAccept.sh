#!/bin/bash

bgmc -N 100 -n 1 -e 5 -d 0.0259 -s 1 -f 8 -a -o accept-0.9.txt
bgmc -N 100 -n 1 -e 5 -d 0.367 -s 1 -f 8 -a -o accept-0.1.txt

./MakeXMax.py accept-0.9.txt
./MakeXMax.py accept-0.1.txt
