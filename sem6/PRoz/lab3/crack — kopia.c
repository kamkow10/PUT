#include <mpi.h>
#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

/* 4 literowe
aa5UYq6trT5u.
bahAZ9Hk7SCf6
ddoo3WocSpthU
jkmD2RlhoMyuA
zzm4NUIIb7VIk
kkv864igyJC9o

5 literowe
aaSPfLTmjh3fU

6 literowe
aaLTdQr7DyHuU 
*/

char *stro="aa5UYq6trT5u.";


int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int size,rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    char cmp[5]={0};

    char salt[3]={0};
    salt[0]=stro[0];
    salt[1]=stro[1];

    /* Ten fragment kodu nalezy _jakos_ zrównoleglić */
    /* pewnie będzie potrzebna jakaś pętla... */
    char * x=crypt(cmp, salt);

    if ((strcmp(x,stro))==0)
    {
            /* w docelowej wersji przeslac odgadnięte hasło masterowi */
	    printf("Udalo sie: %s %s %s\n", cmp, x, stro);
            MPI_Finalize();
	    exit(0);
    }
    /* Koniec fragmentu kodu */

    MPI_Finalize();
}
