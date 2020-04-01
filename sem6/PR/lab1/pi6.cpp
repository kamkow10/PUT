#include <stdio.h>
#include <time.h>
#include <iostream>
#include <omp.h>

using namespace std;

long long num_steps = 1000000000;
double step;

int main(int argc, char* argv[])
{
	double x, pi, sum = 0.0;
	int i;
	step = 1. / (double)num_steps;
	const int threads = 2;
	omp_set_num_threads(threads);
	double sums[threads];
	for (int j = 0; j < threads; j++)
		sums[j] = 0;
	double startOmp = omp_get_wtime();
	#pragma omp parallel
	{
		#pragma omp for
		for (i = 0; i<num_steps; i++)
		{
			x = (i + .5)*step;
			sums[omp_get_thread_num()] += 4.0 / (1. + x * x);
		}
	}
	for (int k = 0; k < threads; k++)
		sum += sums[k];
	pi = sum * step;
	double stopOmp = omp_get_wtime() - startOmp;

	printf("Wartosc liczby PI wynosi %15.12f\n", pi);
	printf("Czas przetwarzania wynosi %f sekund", stopOmp);
	return 0;
}