#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

char buffer[1024*1024];

int main(int argc, const char *argv[])
{
	FILE *f;
	uint32_t N, alpha_count;
	int32_t nmax;
	char gammastr[128];
	char interstr[128];
	uint32_t total_alphas = 0;
	if (argc<=1)
		return 0;
	for (int fidx=1;fidx<argc;++fidx)
	{
		f = fopen(argv[fidx],"r");
		int r = fscanf(f,"%d\n%d\n%s\n%[^\n]\n%d\n\n",&N,&nmax,gammastr,interstr,&alpha_count);
		if (r!=5)
			return 1;
		fprintf(stderr,
		"%s\n"
		"\tN = %d\n"
		"\tnmax = %d\n"
		"\tgamma = %s\n"
		"\tinteraction = %s\n"
		"\talpha_count = %d\n",
		argv[fidx],N,nmax,gammastr,interstr,alpha_count
		);
		fflush(stderr);
		
		total_alphas += alpha_count;

		fclose(f);
	}
	printf("%d\n%d\n%s\n%s\n%d\n\n",N,nmax,gammastr,interstr,total_alphas);
	for (int fidx=1;fidx<argc;++fidx)
	{
		f = fopen(argv[fidx],"r");
		int r = fscanf(f,"%d\n%d\n%s\n%[^\n]\n%d\n\n",&N,&nmax,gammastr,interstr,&alpha_count);
		if (r!=5)
			return 1;

		for (uint32_t i=0;i<alpha_count;++i)
		{
			fscanf(f,"%[^\n]\n",buffer);
			printf("%s\n",buffer);
		}

		fclose(f);
	}
	return 0;
}
