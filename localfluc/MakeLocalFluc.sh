#!/bin/bash

HELP="MakeLocalFluc.sh <0/1/2/3> <mc/max> <output dir> <mk/output>"
AVERAGE_GAMMA="-0.015913540477747776"
E_CONTACT=12
E_DIPOLE=4

if [ "$#" -ne 4 ]
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

TARGET1="$DATA$NAME.mcalpha"
TARGET2="$DATA$NAME.$LF_METHOD.localfluc"

case "$4" in
	"mk")
		echo "$TARGET1:"
		echo -e "\t$CMD -o $TARGET1 > $TARGET1.progress 2>&1"
		echo
		echo "$TARGET2: localfluc $TARGET1"
		echo -e "\t./localfluc $LF_METHOD < $TARGET1 > $TARGET2 2> $TARGET2.progress"
		echo
	;;
	"data")
		echo "$TARGET1"
	;;
	"output")
		echo "$TARGET2"
	;;
	*)
		echo $HELP
		exit 1
esac
