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

char *stro="aaLTdQr7DyHuU";

MPI_Status status;


int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int size,rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    char salt[3]={0};
    salt[0]=stro[0];
    salt[1]=stro[1];
 
    /* Ten fragment kodu nalezy _jakos_ zrównoleglić */
    /* pewnie będzie potrzebna jakaś pętla... */
    if (rank == 0) {
        while(1) {
            int isAnswerReady;
            MPI_Recv(&isAnswerReady, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            if (isAnswerReady) {
                char answer[7];
                MPI_Recv(&answer, 7, MPI_INT, status.MPI_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                printf("%s\n", answer);
                for (int j = 1; j < 27; j++)
                {
                    if (j != status.MPI_SOURCE) {
                        int answerReady = 1;
                        MPI_Send( &answerReady, 1, MPI_INT, j, 1, MPI_COMM_WORLD);
                    }
                }
                return 0;
            }
            for (int j = 1; j < 27; j++)
            {
                int noAnswer = 0;
                MPI_Send( &noAnswer, 1, MPI_INT, j, 0, MPI_COMM_WORLD);
            }
        }
    } else {
        int i1 = 96 + rank;
        for (int i2 = 97; i2 <= 122; i2++) {
            printf("%d in %d\n", rank, i2);
            for (int i3 = 97; i3 <= 122; i3++) {
                for (int i4 = 97; i4 <= 122; i4++) {
                    for (int i5 = 97; i5 <= 122; i5++) {
                        for (int i6 = 97; i6 <= 122; i6++) {
                            char cmp[7] = {i1, i2, i3, i4, i5, i6, '\0'};
                            char * x = crypt(cmp, salt);
                            int msg;
                            if ((strcmp(x,stro))==0) {
                                msg = 1;
                                MPI_Send( &msg, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
                                printf("%d znalazłem!\n", rank);
                                MPI_Send( &cmp, 7, MPI_INT, 0, 0, MPI_COMM_WORLD);
                                return 0;
                            } else {
                                msg = 0;
                                MPI_Send( &msg, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
                            }
                            int isAnswerReady;
                            MPI_Recv(&isAnswerReady, 1, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
                            if (isAnswerReady) {
                                return 0;
                            }
                        }
                    }
                }
            }
        }
    }

    MPI_Finalize();
}
