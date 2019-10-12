ALL=localfluc combine ../figures/fig6.eps

.PHONY: all
all: $(ALL)

localfluc.mk: MakeLocalFluc.sh
	./MakeLocalFluc.sh 0 mc data/ mk > localfluc.mk
	./MakeLocalFluc.sh 1 mc data/ mk >> localfluc.mk
	./MakeLocalFluc.sh 2 mc data/ mk >> localfluc.mk
	./MakeLocalFluc.sh 3 mc data/ mk >> localfluc.mk

include localfluc.mk

LF_DATA=$(shell ./MakeLocalFluc.sh 0 mc data/ data)
LF_DATA+=$(shell ./MakeLocalFluc.sh 1 mc data/ data)
LF_DATA+=$(shell ./MakeLocalFluc.sh 2 mc data/ data)
LF_DATA+=$(shell ./MakeLocalFluc.sh 3 mc data/ data)

LOCALFLUC=$(shell ./MakeLocalFluc.sh 0 mc data/ output)
LOCALFLUC+=$(shell ./MakeLocalFluc.sh 1 mc data/ output)
LOCALFLUC+=$(shell ./MakeLocalFluc.sh 2 mc data/ output)
LOCALFLUC+=$(shell ./MakeLocalFluc.sh 3 mc data/ output)

../figures/fig6.eps: $(LOCALFLUC)
	./PlotSub.py $^ $@

localfluc: localfluc.c
	gcc -march=native -O3 -flto localfluc.c -lm -o localfluc

combine: combine.c
	gcc -march=native -O3 -flto combine.c -o combine

.PHONY: clean
clean:
	rm -f localfluc.mk
	rm -f $(ALL)
	rm -f $(LOCALFLUC)
	rm -f $(LF_DATA)
	rm -f data/*.progress
