#include "main.h"
#include "zleceniodawca.h"

int lamportClock;
pthread_mutex_t listenMutex = PTHREAD_MUTEX_INITIALIZER;
bool shouldFinish = false;
volatile bool signalCatched = false;

void jobMakerLoop() {
    srandom(rank);
    lamportClock = 0;
    pthread_t listenThread, monitorThread;
    sleep(SEC_IN_STATE);
    pthread_create(&listenThread, NULL, startListenThread, 0);
    pthread_create(&monitorThread, NULL, startMonitor, 0);
    int jobId = 1;
    while (!shouldFinish) {
        pthread_mutex_lock(&listenMutex);
        int perc = random() % 100;
        if (perc < STATE_CHANGE_PROB) {
            println("@@@ NOWE ZLECENIE #%d @@@", lamportClock, jobId);
            sleep(SEC_IN_STATE); // to nam zasymuluje, że wiadomość trochę leci w kanale
            // bez tego algorytm formalnie błędny za każdym razem dawałby poprawny wynik
            for (int i = 1; i < size; i++)
                sendPacket(lamportClock, jobId, i, BROADCAST);
            jobId++;
        }
        pthread_mutex_unlock(&listenMutex);
        sleep(SEC_IN_STATE);
    }
    pthread_join(listenThread, NULL);
    pthread_join(monitorThread, NULL);
    return;
}

void *startListenThread(void *ptr) {
    packet_t* packet = new packet_t;
    MPI_Status status;
    while (!shouldFinish) {
        MPI_Recv(packet, 1, MPI_PAKIET_T, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        if (status.MPI_TAG == FINISH) {
            shouldFinish = true;
        }
        pthread_mutex_lock(&listenMutex);
        lamportClock = std::max(lamportClock, packet->lamport) + 1;
        pthread_mutex_unlock(&listenMutex);
    }
}

/* monitor to osobny wątek istniejący tylko u ROOTa, komunikujący się z użytkownikiem */
/* Ponieważ wprowadza on dodatkowe komplikacje w debugowaniu, można go wyciąć przy implementacji
   tematów projektów */

void *startMonitor(void *ptr)
{
    /* Obrazuje pętlę odbierającą komendy od użytkownika */
    char *instring, *token, *saveptr;
    instring = (char*)malloc(sizeof(char) * 100);
    println("### Wpisz \"exit\" lub \"quit\" aby zakończyć działanie programu ###", 0);
    int newline;
    while (TRUE) {
        fgets( instring, 99, stdin);
        newline = strcspn(instring, "\n");
        instring[newline]=0; 
        token = strtok_r(instring, " ", &saveptr);
        if (signalCatched || (strcmp(token, "exit") == 0) || (strcmp(token, "quit") == 0)) {
            printf("Zakańczam działanie programu...\n");
            int i;
            for (i = 0; i < size; i++)
		        sendPacket(0, 0, i, FINISH);
            break;
        }
    }
    free(instring);
}
