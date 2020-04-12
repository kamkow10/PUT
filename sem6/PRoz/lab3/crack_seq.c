// #include <mpi.h>
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


int main(int argc, char **argv)
{
//    MPI_Init(&argc, &argv);
//
//    int size,rank;
//    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
//    MPI_Comm_size(MPI_COMM_WORLD, &size);

// ASCII: 97 - 122

    char salt[3]={0};
    salt[0]=stro[0];
    salt[1]=stro[1];

    // 4

    // for (int i1 = 97; i1 <= 122; i1++) {
    //     for (int i2 = 97; i2 <= 122; i2++) {
    //         for (int i3 = 97; i3 <= 122; i3++) {
    //             for (int i4 = 97; i4 <= 122; i4++) {
    //                 char cmp[5] = {i1, i2, i3, i4, '\0'};
    //                 char * x = crypt(cmp, salt);
    //                 if ((strcmp(x,stro))==0) {
    //                     printf("Udalo sie: %s %s %s\n", cmp, x, stro);
    //                     return 0;
    //                     /* w docelowej wersji przeslac odgadnięte hasło masterowi */
    //                     /*MPI_Finalize();*/
    //                 }
    //             }
    //         }
    //     }
    // }

    // 5

    // for (int i1 = 97; i1 <= 122; i1++) {
    //     for (int i2 = 97; i2 <= 122; i2++) {
    //         for (int i3 = 97; i3 <= 122; i3++) {
    //             for (int i4 = 97; i4 <= 122; i4++) {
    //                 for (int i5 = 97; i5 <= 122; i5++) {
    //                     char cmp[6] = {i1, i2, i3, i4, i5, '\0'};
    //                     char * x = crypt(cmp, salt);
    //                     if ((strcmp(x,stro))==0) {
    //                         printf("Udalo sie: %s %s %s \n", cmp, x, stro);
    //                         return 0;
    //                         /* w docelowej wersji przeslac odgadnięte hasło masterowi */
    //                         /*MPI_Finalize();*/
    //                     }
    //                 }
    //             }
    //         }
    //     }
    // }

    // 6

    for (int i1 = 97; i1 <= 122; i1++) {
        for (int i2 = 97; i2 <= 122; i2++) {
            for (int i3 = 97; i3 <= 122; i3++) {
                for (int i4 = 97; i4 <= 122; i4++) {
                    for (int i5 = 97; i5 <= 122; i5++) {
                        for (int i6 = 97; i6 <= 122; i6++) {
                            char cmp[7] = {i1, i2, i3, i4, i5, i6, '\0'};
                            char * x = crypt(cmp, salt);
                            if ((strcmp(x,stro))==0) {
                                printf("Udalo sie: %s %s %s \n", cmp, x, stro);
                                return 0;
                                /* w docelowej wersji przeslac odgadnięte hasło masterowi */
                                /*MPI_Finalize();*/
                            }
                        }
                    }
                }
            }
        }
    }

//    MPI_Finalize();
}
