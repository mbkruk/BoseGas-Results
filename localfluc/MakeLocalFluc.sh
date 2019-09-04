#!/bin/bash

HELP="MakeLocalFluc.sh <0/1/2/3> <mc/max> <output dir>"
AVERAGE_GAMMA="-0.011871523554730593"
E_CONTACT=8
E_DIPOLE=3
MC_COUNT=32

if [ "$#" -ne 3 ]
then
	echo $HELP
	exit 1
fi

LF_METHOD=$2
DATA=$3

case "$1" in
	"0")
	NAME="n1-e${E_CONTACT}-contact"
	CMD="bgmc -N 100 -n 1 -e $E_CONTACT -g $AVERAGE_GAMMA -a"
	;;
	"1")
	NAME="n3-e${E_CONTACT}-contact"
	CMD="bgmc -N 100 -n 3 -e $E_CONTACT -g $AVERAGE_GAMMA -a"
	;;
	"2")
	NAME="n1-e${E_DIPOLE}-dipole-0.060"
	CMD="bgmc -N 100 -n 1 -e $E_DIPOLE -g $AVERAGE_GAMMA -I ../intcoeff/dipol-0.060.in -a"
	;;
	"3")
	NAME="n3-e${E_DIPOLE}-dipole-0.060"
	CMD="bgmc -N 100 -n 3 -e $E_DIPOLE -g $AVERAGE_GAMMA -I ../intcoeff/dipol-0.060.in -a"
	;;
	*)
	echo $HELP
	exit 1
esac

for N in $(seq -f "%0${#MC_COUNT}g" 1 $MC_COUNT)
do
	echo "### $N/$MC_COUNT ###"
	$CMD -o $DATA$NAME-$N.txt
done

./combine $DATA$NAME-*.txt > $DATA$NAME.in.txt

./localfluc $LF_METHOD < $DATA$NAME.in.txt > $DATA$NAME.$LF_METHOD.out.txt
