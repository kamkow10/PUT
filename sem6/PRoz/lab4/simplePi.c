#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <math.h>

#define ITERATIONS 1000000000
#define PRECISION 1000000

int main(int argc,char **argv)
{
    srand(time(NULL));
    int pointsInCircle = 0;
    for (int i = 0; i < ITERATIONS; i++)
    {
        long double x = (long double)(rand() % PRECISION) / (long double)(PRECISION);
        long double y = (long double)(rand() % PRECISION) / (long double)(PRECISION);
        long double distance = pow(x, 2) + pow(y, 2);
        if (distance <= 1.0) pointsInCircle++;
    }
    long double pi = ((long double)(4) * pointsInCircle) / (long double)(ITERATIONS); 
    printf("PI = %.17Lg\n", pi);
    return 0;
}
