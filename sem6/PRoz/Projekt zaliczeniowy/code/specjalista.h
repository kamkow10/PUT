#ifndef SPECJALISTA_H
#define SPECJALISTA_H

#include <algorithm>

/* pętla główna procesu specjalisty, cała logika wysyłania i reakcji na wiadomości w różnych stanach */
void specialistLoop(int B, int S);

std::string listToString(std::list<int> list);

std::string listToString(std::vector<int> list);

std::string listToString(std::vector<SpecialistInfo> list);

std::string professionToString(int profession);

void sendInfoToAllSpecialists();

void putSpecialistToProperProfessionList(SpecialistInfo specialist);

void recvInfoFromAllSpecialists();

void tryAssignJob();

void printFullDebugInfo();

void *startPaperWorkThread(void *ptr);

void *startWorkThread(void *ptr);

void paperWork();

void work();

void sendReqToAllSpecialists(int reqKind);

bool isSpecialistHavingHigherPriority(int priorityToCompare, int id);

void addNewReadySpeciallist(int id);

void updateLamportClock(int recevedLamportClock);

void sendAckToWaitingSpecialists(int ackKind);

void sendStartWorkMessage();

#endif
