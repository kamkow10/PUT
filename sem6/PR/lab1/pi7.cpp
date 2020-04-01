#include <stdio.h>
#include <time.h>
#include <iostream>
#include <omp.h>

using namespace std;

long long num_steps = 100000000;
double step;

int main(int argc, char* argv[])
{
	const int threads = 2;
	omp_set_num_threads(threads);
	volatile double tab[50];

	for (int ind = 0; ind < 50; ind++) {
		tab[ind] = 0;
		tab[ind + 1] = 0;
		double x, pi, sum = 0.0;
		int i;
		step = 1. / (double)num_steps;
		double startOmp = omp_get_wtime();
		#pragma omp parallel
		{
			#pragma omp for
			for (i = 0; i<num_steps; i++)
			{
				x = (i + .5)*step;
				tab[ind + omp_get_thread_num()] += 4.0 / (1. + x * x);
			}
		}
		sum = tab[ind] + tab[ind + 1];
		pi = sum * step;
		double stopOmp = omp_get_wtime() - startOmp;

		printf("====== tab[%d], tab[%d] ======\n", ind, ind + 1);
		printf("Wartosc liczby PI wynosi %15.12f\n", pi);
		printf("Czas przetwarzania wynosi %f sekund\n\n", stopOmp);
	}
	return 0;
}