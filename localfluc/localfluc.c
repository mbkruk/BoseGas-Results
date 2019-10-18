#define _USE_MATH_DEFINES
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <immintrin.h>
#include <time.h>
#include <string.h>

#define MODE_MAX 64
#define SAMPLE_RATE_MAX 32768
#define BIN_COUNT 101
#define SKIP 2

#define MIN(a,b) ((a)<(b) ? (a) : (b))
#define MAX(a,b) ((a)>(b) ? (a) : (b))

const double tau = 2.0*M_PI;

double sqr(double x)
{
	return x*x;
}

double xx[SAMPLE_RATE_MAX] __attribute__((aligned(32)));
double yy[SAMPLE_RATE_MAX] __attribute__((aligned(32)));
double zz[SAMPLE_RATE_MAX] __attribute__((aligned(32)));

__m256d const *mx = (__m256d*)xx;
__m256d const *my = (__m256d*)yy;
__m256d const *mz = (__m256d*)yy;

double re[MODE_MAX] __attribute__((aligned(32)));
double im[MODE_MAX] __attribute__((aligned(32)));

double coskx[MODE_MAX*SAMPLE_RATE_MAX] __attribute__((aligned(32)));
double sinkx[MODE_MAX*SAMPLE_RATE_MAX] __attribute__((aligned(32)));

int main(int argc, const char *argv[])
{
	if (argc!=2)
	{
		err:
		fprintf(stderr,"localfluc <mc/max> < input > output\n");
		fflush(stderr);
		return 1;
	}
	int method;
	if (!strcmp(argv[1],"mc"))
		method = 1;
	else
	if (!strcmp(argv[1],"max"))
		method = 0;
	else
		goto err;
	uint32_t N, alpha_count;
	int32_t nmax;
	double gamma;
	int r = scanf("%d\n%d\n%lf\n%*[^\n]\n%d\n\n",&N,&nmax,&gamma,&alpha_count);
	if (r!=4)
		return 1;
	fprintf(stderr,
	"N = %d\n"
	"nmax = %d\n"
	"gamma = %lf\n"
	"alpha_count = %d\n",
	N,nmax,gamma,alpha_count
	);
	fflush(stderr);

	const uint32_t ntotal = 2*nmax+1;
	const uint32_t bin_size = 16*nmax;
	const uint32_t sample_rate = BIN_COUNT*bin_size;

	for (uint32_t i=0;i<sample_rate;++i)
		xx[i] = (double)i/(double)sample_rate-0.5;

	size_t bin_total = BIN_COUNT*(size_t)alpha_count;
	double *bins = malloc(sizeof(double)*bin_total);
	for (size_t i=0;i<bin_total;++i)
		bins[i] = 0.0;

	const double dx = 1.0/sample_rate;

	for (int32_t n=-nmax;n<=nmax;++n)
	{
		uint32_t j = nmax+n;
		for (uint32_t i=0;i<sample_rate;++i)
		{
			coskx[sample_rate*j+i] = cos(tau*xx[i]*(double)n);
			sinkx[sample_rate*j+i] = sin(tau*xx[i]*(double)n);
		}
	}

	time_t lt = time(0);

	for (uint32_t aidx=0;aidx<alpha_count;aidx++)
	{
		for (uint32_t i=0;i<ntotal;++i)
			scanf("%lf",re+i);
		for (uint32_t i=0;i<ntotal;++i)
			scanf("%lf",im+i);

		if (aidx%SKIP)
			continue;

		double x, y;

		x = 0.0;
		for (uint32_t i=0;i<ntotal;++i)
			x += re[i]*re[i]+im[i]*im[i];
		if (fabs(x-(double)N)>0.01)
		{
			fprintf(stderr,"alpha set %d not normalized\n",aidx);
			fflush(stderr);
		}
		//fprintf(stderr,"last %lf\n",im[ntotal-1]);

		// wave profile
		for (uint32_t i=0;i<sample_rate;++i)
		{
			yy[i] = 0.0;
			zz[i] = 0.0;
		}
		for (uint32_t j=0;j<ntotal;++j)
		{
			for (uint32_t i=0;i<sample_rate;++i)
			{
				x = coskx[sample_rate*j+i];
				y = sinkx[sample_rate*j+i];
				yy[i] += re[j]*x-im[j]*y;
				zz[i] += re[j]*y+im[j]*x;
			}
		}
		for (uint32_t i=0;i<sample_rate;++i)
			yy[i] = yy[i]*yy[i]+zz[i]*zz[i];

		uint32_t shift;

		if (method) // mc
		{
			// center of mass (on a circle)
			x = y = 0.0;
			for (uint32_t i=0;i<sample_rate;++i)
			{
				x += yy[i]*cos(tau*xx[i]);
				y += yy[i]*sin(tau*xx[i]);
			}
			x /= (double)sample_rate;
			y /= (double)sample_rate;

			double angle = atan2(y,x);

			shift = MIN(MAX((int32_t)((angle/tau+0.5)*(double)sample_rate),0),sample_rate-1);
		}
		else // max
		{
			// maximum abs value
			shift = 0;
			double vmax = yy[shift];
			for (uint32_t i=shift+1;i<sample_rate;++i)
			if (yy[i]>vmax)
			{
				vmax = yy[i];
				shift = i;
			}
		}

		for (uint32_t i=0, j;i<sample_rate;++i)
		{
			j = (i+sample_rate+sample_rate/2-shift)%sample_rate;
			j /= bin_size;
			bins[BIN_COUNT*aidx+j] += 0.5*(yy[i]+yy[(i+1)%sample_rate])*dx;
		}

		if (!((aidx+SKIP)%1024))
		{
			fprintf(stderr,"%.3lf done\n",(aidx+1)/(double)alpha_count);
			fflush(stderr);
		}

		/*if (aidx!=1337)
			continue;

		for (uint32_t i=0;i<sample_rate;++i)
			printf(" %lf",xx[i]);
		printf("\n");
		for (uint32_t i=0;i<sample_rate;++i)
			printf(" %lf",yy[(i+sample_rate+sample_rate/2+shift)%sample_rate]);
		printf("\n");

		return 0;*/
	}

	double *mean = malloc(sizeof(double)*BIN_COUNT);
	double *std = malloc(sizeof(double)*BIN_COUNT);

	for (uint32_t j=0;j<BIN_COUNT;++j)
	{
		mean[j] = 0.0;
		for (uint32_t i=0;i<alpha_count;i+=SKIP)
			mean[j] += bins[BIN_COUNT*i+j];
		mean[j] /= (double)(alpha_count/SKIP);
	}

	for (uint32_t j=0;j<BIN_COUNT;++j)
	{
		std[j] = 0.0;
		for (uint32_t i=0;i<alpha_count;i+=SKIP)
			std[j] += sqr(bins[BIN_COUNT*i+j]-mean[j]);
		std[j] /= (double)(alpha_count/SKIP-1);
		std[j] = sqrt(std[j]);
	}

	for (uint32_t j=0;j<BIN_COUNT;++j)
	{
		printf("%lf\n",std[j]/mean[j]);
	}

	free(bins);
	free(mean);
	free(std);

	return 0;
}
