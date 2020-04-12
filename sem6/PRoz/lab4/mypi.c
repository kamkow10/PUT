#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>
#include <time.h>

#define PROCESSES 10
#define ITERATIONS 1000000000
#define PRECISION 1000000
#define ROOT 0
#define MSG_TAG 100

int main(int argc,char **argv)
{
    int size,tid;
    int R;

    MPI_Init(&argc, &argv); 

    MPI_Comm_size( MPI_COMM_WORLD, &size );
    MPI_Comm_rank( MPI_COMM_WORLD, &tid );

    srand(time(NULL));
    unsigned long long int pointsInCircle = 0;
    for (int i = 0; i < ITERATIONS; i++)
    {
        long double x = (long double)(rand() % PRECISION) / (long double)(PRECISION);
        long double y = (long double)(rand() % PRECISION) / (long double)(PRECISION);
        long double distance = pow(x, 2) + pow(y, 2);
        if (distance <= 1.0) pointsInCircle++;
    }
    // printf("PI = %.17Lg\n", pi);

    if ( tid == 0 ) {
        for (int i = 1; i < PROCESSES; i++)
        {
            unsigned long long int recvPoints;
            MPI_Recv( &recvPoints, 1, MPI_UNSIGNED_LONG_LONG, i, MPI_ANY_TAG, MPI_COMM_WORLD, NULL);
            pointsInCircle += recvPoints;
        }                       
        long double pi = ((long double)(4) * pointsInCircle) / ((long double)(ITERATIONS) * (long double)(PROCESSES));                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        printf("PI = %.17Lg\n", pi);
    } else {
        MPI_Send( &pointsInCircle, 1, MPI_UNSIGNED_LONG_LONG, ROOT, MSG_TAG, MPI_COMM_WORLD );
    }

    MPI_Finalize();
}
