#ifndef GLOBALH
#define GLOBALH

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <vector>
#include <list>
#include <signal.h>

/* odkomentować, jeżeli się chce DEBUGI */
#define DEBUGER_ON

/* odkomentować, jeżeli się chce spradzanie wsparcia dla wątków */
//#define CHECK_THREADS_ON

/* boolean */
#define TRUE 1
#define FALSE 0

/* używane w wątku głównym, determinuje jak często i na jak długo zmieniają się stany */
#define STATE_CHANGE_PROB 50
#define SEC_IN_STATE 2

#define ROOT 0

/* stany procesu */
typedef enum {
    READY,
    TEAM,
    PREPARING_PAPERWORK,
    PAPERWORK,
    PREPARING_SKELETON,
    SKELETON_GUARDING,
    JOINING
} state_t;
extern state_t state;
extern int rank;
extern int size;

typedef struct {
    int lamport;       /* timestamp (zegar lamporta */
    int src;      /* pole nie przesyłane, ale ustawiane w main_loop */
    int data;     /* przykładowe pole z danymi; można zmienić nazwę na bardziej pasującą */
} packet_t;
extern MPI_Datatype MPI_PAKIET_T;

/* Typy wiadomości */
#define BROADCAST 1
#define INFO 2
#define REQ_JOIN 3
#define ACK_JOIN 4
#define REQ_PAPERWORK 5
#define ACK_PAPERWORK 6
#define REQ_SKELETON 7
#define ACK_SKELETON 8
#define START_WORK 9
#define FINISH 10

/* profesje */
#define HEAD 0
#define BODY 1
#define TAIL 2

/* Inforacja o procesie specialisty: id + specializacja */
typedef struct {
    int id;
    int profession;
} SpecialistInfo;

/* Zbiór danych o sytucacji w programie */
typedef struct {
    std::list<int> jobsList;
    std::vector<SpecialistInfo> specialists;
    std::list<int> readyHeadSpecialists;
    std::list<int> readyBodySpecialists;
    std::list<int> readyTailSpecialists;
    std::vector<int> team;
    int lamportClock = 0;
    int requestPriority;
    int ackCounter = 0;
    std::list<int> waitingSpecialists;
} SpecialistData;

#ifdef DEBUGER_ON
#define debug(FORMAT, LAMPORT, ...) printf("%c[%d;%dm [%d%d]<%d%d%d%d>: " FORMAT "%c[%d;%dm\n",  27, (1+(rank/7))%2, 31+(6+rank)%7, rank/10, rank % 10, LAMPORT / 1000, (LAMPORT % 1000) / 100, (LAMPORT % 100) / 10, LAMPORT % 10, ##__VA_ARGS__, 27,0,37);
#else
#define debug(...) ;
#endif

#ifdef CHECK_THREADS_ON
#define THREADS_CHECKING 1
#else
#define THREADS_CHECKING 0
#endif

#define P_WHITE printf("%c[%d;%dm",27,1,37);
#define P_BLACK printf("%c[%d;%dm",27,1,30);
#define P_RED printf("%c[%d;%dm",27,1,31);
#define P_GREEN printf("%c[%d;%dm",27,1,33);
#define P_BLUE printf("%c[%d;%dm",27,1,34);
#define P_MAGENTA printf("%c[%d;%dm",27,1,35);
#define P_CYAN printf("%c[%d;%d;%dm",27,1,36);
#define P_SET(X) printf("%c[%d;%dm",27,1,31+(6+X)%7);
#define P_CLR printf("%c[%d;%dm",27,0,37);

/* printf ale z kolorkami i automatycznym wyświetlaniem RANK. Patrz debug wyżej po szczegóły, jak działa ustawianie kolorków */
#define println(FORMAT, LAMPORT, ...) printf("%c[%d;%dm [%d%d]<%d%d%d%d>: " FORMAT "%c[%d;%dm\n",  27, (1+(rank/7))%2, 31+(6+rank)%7, rank/10, rank % 10, LAMPORT / 1000, (LAMPORT % 1000) / 100, (LAMPORT % 100) / 10, LAMPORT % 10, ##__VA_ARGS__, 27,0,37);

/* wysyłanie pakietu, skrót: wskaźnik do pakietu (0 oznacza stwórz pusty pakiet), do kogo, z jakim typem */
void sendPacket(int lamport, int data,  int destination, int tag);

void changeState(state_t);


#endif
