ALL=localfluc

%.out.txt: %.in.txt localfluc
	time ./localfluc < $< > $@

localfluc: localfluc.c
	gcc -march=native -O3 localfluc.c -o localfluc

.PHONY: all clean

all: $(ALL)

clean:
	rm -f $(ALL)
