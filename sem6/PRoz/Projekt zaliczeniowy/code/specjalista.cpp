#include "main.h"
#include "specjalista.h"

int B; // liczba dostępnych biurek w gildii
int S; // liczba dostępnych szkieletów

pthread_mutex_t lamportMutex = PTHREAD_MUTEX_INITIALIZER;

MPI_Status status;
SpecialistData *myData; // lokalny zbiór wszystkich danych o programie

void specialistLoop(int B, int S) {
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);
    debug("Proces uruchomiony na maszynie %s", 0, processor_name);

    myData = new SpecialistData;
    sendInfoToAllSpecialists();
    debug("Wysłano wiadomości INFO do wszystkich procesów", 0);
    recvInfoFromAllSpecialists();
    debug("Odebrano wiadomości INFO od wszystkich procesów", 0);
    changeState(READY);
    while (TRUE) {
        packet_t * recvPacket = new packet_t;
        MPI_Recv(recvPacket, 1, MPI_PAKIET_T, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        pthread_mutex_lock(&lamportMutex);
        updateLamportClock(recvPacket->lamport);
        switch (status.MPI_TAG) {
            case BROADCAST:
                myData->jobsList.push_back(recvPacket->data);
                println("Otrzymałem wiadomość, ze powstało nowe zlecenie o id %d", myData->lamportClock, recvPacket->data);
                printFullDebugInfo();
                tryAssignJob();
                break;
            case REQ_PAPERWORK:
                if (state == PAPERWORK || (state == PREPARING_PAPERWORK && (isSpecialistHavingHigherPriority(recvPacket->data, recvPacket->src)))) {
                    myData->waitingSpecialists.push_back(recvPacket->src);
                    debug("Otrzymałem REQ_PAPERWORK od %d, lecz się nie zgadzam", myData->lamportClock, recvPacket->src);
                } else {
                    debug("Otrzymałem REQ_PAPERWORK od %d, i odsyłam ACK_PAPERWORK", myData->lamportClock, recvPacket->src);
                    myData->lamportClock++;
                    sendPacket(myData->lamportClock, 0, recvPacket->src, ACK_PAPERWORK);
                }
                break;
            case ACK_PAPERWORK:
                if (state == PREPARING_PAPERWORK) {
                    debug("Otrzymałem ACK_PAPERWORK od %d", myData->lamportClock, recvPacket->src);
                    myData->ackCounter++;
                    if (myData->ackCounter == size - B - 1) {
                        println("Dostałem się do sekcji biurek. Rozpoczynam robotę papierkową.",
                                myData->lamportClock);
                        paperWork();
                        myData->ackCounter = 0;
                        changeState(PAPERWORK);
                    }
                }
                break;
            case REQ_SKELETON:
                if ((state == SKELETON_GUARDING) ||
                    (state == PREPARING_SKELETON && (isSpecialistHavingHigherPriority(recvPacket->data, recvPacket->src)))) {
                    myData->waitingSpecialists.push_back(recvPacket->src);
                    debug("Otrzymałem REQ_SKELETON od %d, lecz się nie zgadzam", myData->lamportClock, recvPacket->src);
                } else {
                    debug("Otrzymałem REQ_SKELETON od %d, i odsyłam ACK_SKELETON", myData->lamportClock, recvPacket->src);
                    myData->lamportClock++;
                    sendPacket(myData->lamportClock, 0, recvPacket->src, ACK_SKELETON);
                }
                break;
            case ACK_SKELETON:
                if (state == PREPARING_SKELETON) {
                    debug("Otrzymałem ACK_SKELETON od %d", myData->lamportClock, recvPacket->src);
                    myData->ackCounter++;
                    if (myData->ackCounter == size - S - 1) {
                        println("Dostałem się do sekcji smoków. Wysyłam informację do %d, że może rozpocząć pracę",
                                myData->lamportClock, myData->team[2]);
                        sendStartWorkMessage();
                        myData->ackCounter = 0;
                        changeState(SKELETON_GUARDING);
                    }
                }
                break;
            case REQ_JOIN:
                if ((state == JOINING) && (isSpecialistHavingHigherPriority(recvPacket->data, recvPacket->src))) {
                    myData->waitingSpecialists.push_back(recvPacket->src);
                    debug("Otrzymałem REQ_JOIN od %d, lecz się nie zgadzam", myData->lamportClock, recvPacket->src);
                } else {
                    debug("Otrzymałem REQ_JOIN od %d, i odsyłam ACK_JOIN", myData->lamportClock, recvPacket->src);
                    if (myData->team.size() > 0) {
                        if (((rank == myData->team[0]) && (recvPacket->src == myData->team[1])) ||
                            ((rank == myData->team[1]) && (recvPacket->src == myData->team[2]))) {
                            debug("Wnioskuję, że %d zakończył pracę, więc mogę teraz zacząć swoją część",
                                  myData->lamportClock, recvPacket->src);
                            println("Rozpoczynam swoją część pracy", myData->lamportClock);
                            work();
                        }
                    }
                    myData->lamportClock++;
                    addNewReadySpeciallist(recvPacket->src);
                    sendPacket(myData->lamportClock, 0, recvPacket->src, ACK_JOIN);
                    tryAssignJob();
                }
                break;
            case ACK_JOIN:
                if (state == JOINING) {
                    debug("Otrzymałem ACK_JOIN od %d", myData->lamportClock, recvPacket->src);
                    myData->ackCounter++;
                    if (myData->ackCounter == size - 1) {
                        println("Przechodze w stan gotowości", myData->lamportClock);
                        debug("Sprawdzam, czy ktoś nie czeka na ACK_JOIN", myData->lamportClock);
                        sendAckToWaitingSpecialists(ACK_JOIN);
                        myData->ackCounter = 0;
                        changeState(READY);
                        addNewReadySpeciallist(rank);
                        tryAssignJob();
                    }
                }
                break;
            case START_WORK:
                if ((recvPacket->src == myData->team[0]) && (state == TEAM)) {
                    debug("Otrzymałem START_WORK od %d", myData->lamportClock, recvPacket->src);
                    println("Rozpoczynam swoją część pracy", myData->lamportClock);
                    work();
                }
                break;
            // Na polecenie "exit" albo "quit" zakończ proces
            case FINISH:
                return;
            default:
                break;
        }
        delete recvPacket;
        pthread_mutex_unlock(&lamportMutex);
    }
}

std::string listToString(std::list<int> list) {
    std::string res = "[ ";
    for (int elem : list)
        res += std::to_string(elem) + ", ";
    if (list.size() > 0)
        res = res.substr(0, res.size() - 2);
    res += " ]";
    return res;
}

std::string listToString(std::vector<int> list) {
    std::string res = "[ ";
    for (int elem : list)
        res += std::to_string(elem) + ", ";
    if (list.size() > 0)
        res = res.substr(0, res.size() - 2);
    res += " ]";
    return res;
}

std::string listToString(std::vector <SpecialistInfo> list) {
    std::string res = "[ ";
    for (SpecialistInfo spec : list)
        res += std::to_string(spec.id) + "-" + professionToString(spec.profession) + ", ";
    if (list.size() > 0)
        res = res.substr(0, res.size() - 2);
    res += " ]";
    return res;
}

std::string professionToString(int profession) {
    switch (profession) {
        case HEAD:
            return "HEAD";
        case BODY:
            return "BODY";
        case TAIL:
            return "TAIL";
        default:
            return "UNKNOWN";
    }
}

void sendInfoToAllSpecialists() {
    for (int i = 1; i < size; i++) {
        sendPacket(myData->lamportClock, rank % 3, i, INFO);
    }
}

void putSpecialistToProperProfessionList(SpecialistInfo specialist) {
    switch (specialist.profession) {
        case HEAD:
            myData->readyHeadSpecialists.push_back(specialist.id);
            break;
        case BODY:
            myData->readyBodySpecialists.push_back(specialist.id);
            break;
        case TAIL:
            myData->readyTailSpecialists.push_back(specialist.id);
            break;
    }
}

void recvInfoFromAllSpecialists() {
    for (int i = 1; i < size; i++) {
        packet_t * recvPacket = new packet_t;
        MPI_Recv(recvPacket, 1, MPI_PAKIET_T, i, INFO, MPI_COMM_WORLD, &status);
        SpecialistInfo specialist;
        specialist.id = i;
        specialist.profession = recvPacket->data;
        myData->specialists.push_back(specialist);
        putSpecialistToProperProfessionList(specialist);
    }
}

bool isSpecialistAbleToTakeJob() {
    return (myData->readyHeadSpecialists.front() == rank) ||
           (myData->readyBodySpecialists.front() == rank) ||
           (myData->readyTailSpecialists.front() == rank);
}

void tryAssignJob() {
    if ((myData->readyHeadSpecialists.size() == 0) ||
        (myData->readyBodySpecialists.size() == 0) ||
        (myData->readyTailSpecialists.size() == 0) ||
        (myData->jobsList.size() == 0)) {
        return;
    } else {
        if (isSpecialistAbleToTakeJob()) {
            myData->team.push_back(myData->readyHeadSpecialists.front());
            myData->team.push_back(myData->readyBodySpecialists.front());
            myData->team.push_back(myData->readyTailSpecialists.front());
            std::sort(myData->team.begin(), myData->team.end());
            println("Przyjmuję zlecenie o id %d", myData->lamportClock, myData->jobsList.front());
            if (rank == myData->team[0]) {
                // println("Zaczynam ubiegać się o wstęp do jednego z szkieletów", myData->lamportClock);
                // changeState(PREPARING_SKELETON);
                // sendReqToAllSpecialists(REQ_SKELETON);
                println("Zaczynam ubiegać się o wstęp do gildii aby wykonać robotę papierkową", myData->lamportClock);
                changeState(PREPARING_PAPERWORK);
                sendReqToAllSpecialists(REQ_PAPERWORK);
            } else {
                println("Czekam aż kolega z zespołu da znak, że mogę zaczynać pracę", myData->lamportClock);
                changeState(TEAM);
            }
        }
        myData->readyHeadSpecialists.pop_front();
        myData->readyBodySpecialists.pop_front();
        myData->readyTailSpecialists.pop_front();
        myData->jobsList.pop_front();
    }
}

void printFullDebugInfo() {
    if (rank == 1) {
        debug("===================== FULL DEBUG INFO ===========================", myData->lamportClock);
        debug("Lista zleceń: %s", myData->lamportClock, listToString(myData->jobsList).c_str());
        debug("Lista specjalistów: %s", myData->lamportClock, listToString(myData->specialists).c_str());
        debug("Specialiści od głowy:   %s", myData->lamportClock, listToString(myData->readyHeadSpecialists).c_str());
        debug("Specialiści od tułowia: %s", myData->lamportClock, listToString(myData->readyBodySpecialists).c_str());
        debug("Specialiści od ogona:   %s", myData->lamportClock, listToString(myData->readyTailSpecialists).c_str());
        debug("Moja drużyna: %s", myData->lamportClock, listToString(myData->team).c_str());
        debug("=================================================================", myData->lamportClock);
    }
}

void *startPaperWorkThread(void *ptr) {
    srandom(rank + myData->lamportClock);
    int timeInWork = (random() % 3) + 2;
    sleep(timeInWork);
    pthread_mutex_lock(&lamportMutex);
    println("Praca papierkowa wykonana", myData->lamportClock);
    debug("Sprawdzam, czy ktoś nie czeka na ACK_PAPERWORK", myData->lamportClock);
    sendAckToWaitingSpecialists(ACK_PAPERWORK);
    println("Zwalniam sekcję biurek oraz zaczynam ubiegać się o dostęp do szkieletu", myData->lamportClock);
    changeState(PREPARING_SKELETON);
    sendReqToAllSpecialists(REQ_SKELETON);
    pthread_mutex_unlock(&lamportMutex);
}

void *startWorkThread(void *ptr) {
    srandom(rank + myData->lamportClock);
    int timeInWork = (random() % 3) + 2;
    sleep(timeInWork);
    pthread_mutex_lock(&lamportMutex);
    changeState(JOINING);
    myData->ackCounter = 1; // akceptacja od samego siebie
    if (rank == myData->team[0]) {
        println("SMOK WSKRZESONY", myData->lamportClock);
        debug("Sprawdzam, czy ktoś nie czeka na ACK_SKELETON", myData->lamportClock);
        sendAckToWaitingSpecialists(ACK_SKELETON);
    }
    println("Zakończyłem pracę. Zaczynam ubiegać się o przejście w stan gotowości", myData->lamportClock);
    myData->team.clear();
    sendReqToAllSpecialists(REQ_JOIN);
    pthread_mutex_unlock(&lamportMutex);
}

void paperWork() {
    pthread_t paperWorkThread;
    pthread_create(&paperWorkThread, NULL, startPaperWorkThread, 0);
}

void work() {
    pthread_t workThread;
    pthread_create(&workThread, NULL, startWorkThread, 0);
}

void sendReqToAllSpecialists(int reqKind) {
    myData->lamportClock++;
    myData->requestPriority = myData->lamportClock;
    for (int i = 0; i < size; i++) {
        if (i == rank) continue;
        sendPacket(myData->lamportClock, myData->requestPriority, i, reqKind);
    }
}

bool isSpecialistHavingHigherPriority(int priorityToCompare, int id) {
    if (myData->requestPriority < priorityToCompare)
        return true;
    else if (myData->requestPriority == priorityToCompare)
        return rank < id;
    else
        return false;
}

void addNewReadySpeciallist(int id) {
    switch (myData->specialists[id - 1].profession) {
        case HEAD:
            myData->readyHeadSpecialists.push_back(id);
            break;
        case BODY:
            myData->readyBodySpecialists.push_back(id);
            break;
        case TAIL:
            myData->readyTailSpecialists.push_back(id);
            break;
    }
}

void updateLamportClock(int recevedLamportClock) {
    myData->lamportClock = std::max(myData->lamportClock, recevedLamportClock) + 1;
}

void sendAckToWaitingSpecialists(int ackKind) {
    if (myData->waitingSpecialists.size() == 0) {
        debug("Nikt nie czeka", myData->lamportClock);
    } else {
        myData->lamportClock++;
        for (int id : myData->waitingSpecialists) {
            debug("Przesyłam ACK do czekającego procesu o id %d", myData->lamportClock, id);
            sendPacket(myData->lamportClock, 0, id, ackKind);
        }
        myData->waitingSpecialists.clear();
    }
}

void sendStartWorkMessage() {
    myData->lamportClock++;
    sendPacket(myData->lamportClock, 0, myData->team[2], START_WORK);
}
