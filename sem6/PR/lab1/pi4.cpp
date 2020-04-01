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
	omp_set_num_threads(4);
	double startOmp = omp_get_wtime();
	#pragma omp parallel
	{
		double sumTemp = 0.0;
		#pragma omp for
		for (i = 0; i<num_steps; i++)
		{
			x = (i + .5)*step;
			sumTemp += 4.0 / (1. + x * x);
		}
		#pragma omp atomic
		sum += sumTemp;
	}
	pi = sum * step;
	double stopOmp = omp_get_wtime() - startOmp;

	printf("Wartosc liczby PI wynosi %15.12f\n", pi);
	printf("Czas przetwarzania wynosi %f sekund", stopOmp);
	return 0;
}