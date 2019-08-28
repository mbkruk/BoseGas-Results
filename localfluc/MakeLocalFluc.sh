#!/bin/bash

HELP="MakeLocalFluc.sh <0/1/2/3> <output dir>"

if [ "$#" -ne 2 ]
then
	echo $HELP
	exit 1
fi

DATA=$2
case "$1" in
	"0")
	NAME="n1-e7-contact"
	CMD="bgmc -N 100 -n 1 -e 7 -a"
	;;
	"1")
	NAME="n3-e7-contact"
	CMD="bgmc -N 100 -n 3 -e 7 -a"
	;;
	"2")
	NAME="n1-e7-dipole-0.060"
	CMD="bgmc -N 100 -n 1 -e 7 -g -0.032035302086685036 -I ../intcoeff/dipol-0.060.in -a"
	;;
	"3")
	NAME="n3-e7-dipole-0.060"
	CMD="bgmc -N 100 -n 3 -e 7 -g -0.032035302086685036 -I ../intcoeff/dipol-0.060.in -a"
	;;
	*)
	echo $HELP
	exit 1
esac

for N in {1..32}
do
	$CMD -o $DATA$NAME-$N.txt
done

./combine $DATA$NAME-*.txt > $DATA$NAME.in.txt

./localfluc mc < $DATA$NAME.in.txt > $DATA$NAME.out.txt
