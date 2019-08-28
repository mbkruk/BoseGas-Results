ALL="localfluc combine"

localfluc: localfluc.c
	gcc -march=native -O3 localfluc.c -o localfluc

combine: combine.c
	gcc -march=native -O3 combine.c -o combine

.PHONY: all clean

all: $(ALL)

clean:
	rm -f $(ALL)
