#!/bin/sh

# MakeLocalFluc.sh <base cutoff (temperature)> <extra mode pairs (attractive interaction strength)>

INT_TYPE=contact
OUTPUT=localfluc/n$1-e$2-dipol-0.060.txt

#bgmc -N 100 -n $1 -e $2 -g `tail -n1 findmin/$INT_TYPE/python/e-$2.out` -mo -o $OUTPUT
bgmc -N 100 -n $1 -e $2 -I intcoeff/dipol-0.060.in -g `tail -n1 findmin/dipol-0.060/e-$2.out` -mo -o $OUTPUT
