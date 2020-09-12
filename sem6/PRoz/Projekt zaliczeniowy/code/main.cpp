#include "main.h"
#include "specjalista.h"
#include "zleceniodawca.h"
/* wątki */
#include <pthread.h>

/* sem_init sem_destroy sem_post sem_wait */
//#include <semaphore.h>
/* flagi dla open */
//#include <fcntl.h>

state_t state = READY;
volatile char end = FALSE;
int size, rank;
MPI_Datatype MPI_PAKIET_T;

void    check_thread_support(int provided) {
    printf("THREAD SUPPORT: chcemy %d. Co otrzymamy?\n", provided);
    switch (provided) {
        case MPI_THREAD_SINGLE:
            printf("Brak wsparcia dla wątków, kończę\n");
            /* Nie ma co, trzeba wychodzić */
            fprintf(stderr, "Brak wystarczającego wsparcia dla wątków - wychodzę!\n");
            MPI_Finalize();
            exit(-1);
            break;
        case MPI_THREAD_FUNNELED:
            printf("tylko te wątki, ktore wykonaly mpi_init_thread mogą wykonać wołania do biblioteki mpi\n");
            break;
        case MPI_THREAD_SERIALIZED:
            /* Potrzebne zamki wokół wywołań biblioteki MPI */
            printf("tylko jeden watek naraz może wykonać wołania do biblioteki MPI\n");
            break;
        case MPI_THREAD_MULTIPLE:
            printf("Pełne wsparcie dla wątków\n"); /* tego chcemy. Wszystkie inne powodują problemy */
            break;
        default:
            printf("Nikt nic nie wie\n");
    }
}

void inicjuj(int *argc, char ***argv) {
    int provided;
    MPI_Init_thread(argc, argv, MPI_THREAD_MULTIPLE, &provided);
    if (THREADS_CHECKING)
        check_thread_support(provided);

    const int nitems = 3;
    int blocklengths[3] = {1, 1, 1};
    MPI_Datatype typy[3] = {MPI_INT, MPI_INT, MPI_INT};

    MPI_Aint offsets[3];
    offsets[0] = offsetof(packet_t, lamport);
    offsets[1] = offsetof(packet_t, src);
    offsets[2] = offsetof(packet_t, data);

    MPI_Type_create_struct(nitems, blocklengths, offsets, typy, &MPI_PAKIET_T);
    MPI_Type_commit(&MPI_PAKIET_T);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
}

/* usunięcie zamkków, czeka, aż zakończy się drugi wątek, zwalnia przydzielony typ MPI_PAKIET_T
   wywoływane w funkcji main przed końcem
*/
void finalizuj() {
    MPI_Type_free(&MPI_PAKIET_T);
    MPI_Finalize();
}

void sendPacket(int lamport, int data,  int destination, int tag) {
    packet_t * pkt = new packet_t;
    pkt->src = rank;
    pkt->lamport = lamport;
    pkt->data = data;
    MPI_Send(pkt, 1, MPI_PAKIET_T, destination, tag, MPI_COMM_WORLD);
    delete pkt;
}

void changeState(state_t newState) {
    state = newState;
}


int main(int argc, char **argv) {
    inicjuj(&argc, &argv);
    int B;
    int S;
    if (argc == 3) {
        B = atoi(argv[1]);
        S = atoi(argv[2]);
        if (rank == 0) {
            printf("Parametry ustawiono:\nB = %d\nS = %d\n", B, S);
            if (B <= 0 || S <= 0)
                printf("UWAGA! Wielkość sekcji krytycznej jest mniejsza niż 1. Program się zakleszczy!\n");
        }
    } else {
        if (rank == 0)
            fprintf(stderr, "Niepoprawna liczba parametrów. Wymagane: 2, otrzymane: %d\n", argc - 1);
        exit(-1);
    }
    
    if (rank == 0)
        jobMakerLoop();
    else
        specialistLoop(B, S);

    finalizuj();
    return 0;
}

