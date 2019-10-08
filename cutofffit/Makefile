DATA=data/N100_beta0.03625.exact.txt
DATA+=data/N100_beta0.03625_nmax4.cf.txt
DATA+=data/N100_beta0.03625_nmax5.cf.txt
DATA+=data/N100_beta0.03625_nmax3.cf.txt
PLOTS=../figures/fig1.eps

.PHONY: all
all: $(DATA) $(PLOTS)

data/N100_beta0.03625.exact.txt: PNexExact.wls
	./PNexExact.wls 100 0.03625 > $@

data/N100_beta0.03625_nmax3.cf.txt: PNexCF.wls
	./PNexCF.wls 100 3 0.03625 > $@

data/N100_beta0.03625_nmax4.cf.txt: PNexCF.wls
	./PNexCF.wls 100 4 0.03625 > $@

data/N100_beta0.03625_nmax5.cf.txt: PNexCF.wls
	./PNexCF.wls 100 5 0.03625 > $@

%.eps: $(DATA)
	./Plot.py $(DATA) $@

.PHONY: clean
clean:
	rm -f data/*.txt
	rm -f $(PLOTS)
