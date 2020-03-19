#include <netinet/in.h>
#include <netdb.h>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <sys/epoll.h>
#include <cstring>
#include <csignal>
#include <string>
#include <map>
#include <vector>
#include <errno.h>
#include <iostream>
#include <thread>
#include <QMetaObject>
#include <qobjectdefs.h>
#include <string.h>
#include <arpa/inet.h>

#include "statuses.hpp"
#include "player.hpp"
#include "client.h"
#include "constants.h"
#include "mainwindow.h"

class MainWindow;

Client::Client(char *addr)
{
    srvAddr = addr;
    gettingDataThread = new GettingDataThread(this);
}

void Client::init(){
    bindAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    startClient();
    startConnection();
    char msg[20];
    readData(clientFd, msg, sizeof(msg));
    cout << msg << endl;
    if (strcmp("SERVER-OK\0", msg) == 0) {
        while (connected) {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
        std::cout << "Out of main loop" << std::endl;
        closeClient();
    } else if (strcmp("SERVER-MAX\0", msg) == 0) {
        cout << "session max" << endl;
        closeClient();
        GUI->closeOnMaxPlayers();
    }
    return;
}

void Client::activateConnectionProcess(const char* proccesName) {
    char msg[512];
    strcpy(msg, proccesName);
    writeData(clientFd, msg, sizeof(msg));
}

void Client::startClient(void){
    if((clientFd = socket(AF_INET, SOCK_STREAM, 0)) < 0 ){
        perror("Failed to create socket.\n");
        exit(SOCKET_CREATE);
    }
}

void Client::closeClient(void){
    shutdown(clientFd, SHUT_RDWR);
    close(clientFd);
}

void Client::startConnection(){
    int err;
    if (srvAddr != nullptr){
        if (!validateIpAddress(srvAddr)){
            perror("Wrong ip address format!\n");
            exit(WRONG_IP);
        } else {
            err = getaddrinfo(srvAddr, "55555", &hints, &resolved);
        }
    } else {
        err = getaddrinfo("192.168.0.100", "55555", &hints, &resolved);
    }
    if (err || !resolved){
        perror("Resolving address failed!\n");
        exit(GETADDRINFO_ERROR);
    }
    if ( connect(clientFd, resolved->ai_addr, resolved->ai_addrlen) < 0){
        perror("Failed to connect.\n");
        exit(SOCKET_CONNECT);
    }
    freeaddrinfo(resolved);
}

bool Client::validateIpAddress(const std::string &ipAddress){
    struct sockaddr_in sa;
    int result = inet_pton(AF_INET, ipAddress.c_str(), &(sa.sin_addr));
    return result == 1;
}

ssize_t Client::readData(int fd, char * buffer, ssize_t buffsize){
    auto ret = read(fd, buffer, buffsize);
    std::cout << "Read " << ret << " bytes from server" << std::endl;
    if (ret==-1) {
        perror("Read failed\n");
    } else if (ret==0) {
        GUI->onLostedConnection();
    }
    return ret;
}

void Client::writeData(int fd, char * buffer, ssize_t count){
    auto ret = write(fd, buffer, count);
    std::cout << "Send " << ret << " bytes to server" << std::endl;
    if(ret==-1) GUI->onLostedConnection();
    if(ret!=count) perror("Send less than requested to server\n");
}

int Client::authorize(char *log, char *pass, int authKind) {
    activateConnectionProcess(ConnectionProcesses::VALIDATION);
    char msg1[10];
    snprintf(msg1, sizeof(msg1), "%d", authKind);
    writeData(clientFd, msg1, sizeof(msg1));
    char msg2[100];
    strcpy(msg2, log);
    strcat(msg2, "-");
    strcat(msg2, pass);
    writeData(clientFd, msg2, sizeof(msg2));
    memset(msg2, 0, sizeof(msg2));
    readData(clientFd, msg2, sizeof(msg2));
    if (strncmp(msg2, "AUTH-FAIL", 9) == 0) {
        return AuthorizationStatus::FAILED;
    } else if (strncmp(msg2, "AUTH-OK", 7) == 0) {
        login = log;
        password = pass;
        return AuthorizationStatus::SUCCESSFUL;
    } else {
        return AuthorizationStatus::ERROR;
    }
}

int Client::goToSession(int id) {
    activateConnectionProcess(ConnectionProcesses::SESSION_JOIN);
    char msg1[20];
    snprintf(msg1, sizeof(msg1), "%d", id);
    writeData(clientFd, msg1, sizeof(msg1));
    if (id == 0) {
        char msg3[100];
        std::string s = GUI->getSrvName();
        currentSessionName = s;
        strcpy(msg3, s.c_str());
        writeData(clientFd, msg3, sizeof(msg3));
        isHost = true;
    } else {
        for(auto &elem : *(availableSessions)) {
            if (elem.first == id) {
                currentSessionName = elem.second.first;
                break;
            }
        }
        isHost = false;
    }
    char msg2[100];
    readData(clientFd, msg2, sizeof(msg2));
    if (strncmp(msg2, "SESSION-MAX\0", 9) == 0) {
        return SessionMessage::MAX;
    } else if (strcmp(msg2, "SESSION-BUSY\0") == 0) {
        return SessionMessage::BUSY;
    } else if (strcmp(msg2, "SESSION-KILLED\0") == 0) {
        return SessionMessage::KILLED;
    } else if (strcmp(msg2, "SESSION-GOOD\0") == 0) {
        char msgNum[20];
        readData(clientFd, msgNum, sizeof(msgNum));
        inSessionID = std::string(msgNum);
        std::cout << "inSessionID: " << inSessionID << std::endl;
        if (id == 0) {
            return SessionMessage::CREATED;
        } else {
            return SessionMessage::JOINED;
        }
    } else {
        std::cout << "ERROR. Readed data: " << msg2 << std::endl;
        return SessionMessage::SESSION_ERROR;
    }
}

int Client::createSession() {
    return goToSession(0);
}

void Client::startGame() {
    char msg1[100];
    strcpy(msg1, "PLAYER-READY\0");
    writeData(clientFd, msg1, sizeof(msg1));
    startRound();
}

void Client::startRound() {
    char msg2[100];
    readData(clientFd, msg2, sizeof(msg2));
    if (strcmp(msg2, "PLAYER-CHECK1\0") == 0) {
        memset(msg2, 0, sizeof(msg2));
        readData(clientFd, msg2, sizeof(msg2));
    }
    if (strcmp(msg2, "ROUND-START\0") == 0) {
        cout << "ROUND STARTED" << endl;
        if (GUI->reJoin) {
            char playerData[600];
            readData(clientFd, playerData, sizeof(playerData));
            char* s;
            s = strtok(playerData,":");
            long int numPlayers = strtol(s, nullptr, 10);
            for( int i =0; i < numPlayers; i++ ) {
                s = strtok(NULL, "-");
                std::string player(s);
                s = strtok(NULL, ",");
                int points = strtol(s, nullptr, 10);
                GUI->playersScores.insert(std::pair(player, points));
            }
            GUI->reJoin = false;
        }
        char wordMsg[200];
        readData(clientFd, wordMsg, sizeof(wordMsg));
        std::string word(wordMsg);
        GUI->prepareRound(word);
    } else if (strcmp(msg2, "SESSION-TIMEOUT") == 0) {
        cout << "ROUND TIMEOUT" << endl;
        GUI->onTimeout();
        waitForPlayers();
    } else if (strcmp(msg2, "GAME-OVER\0") == 0) {
        cout << "GAME OVER" << endl;
        GUI->gameOver();
    } else if (strcmp(msg2, "SESSION-KILL\0") == 0) {
        cout << "GAME OVER" << endl;
        GUI->gameOver();
    } else if (strcmp(msg2, "PLAYER-CHECK2\0") == 0) {
        GUI->onTimeout();
        memset(msg2, 0, sizeof(msg2));
        readData(clientFd, msg2, sizeof(msg2));
        if (strcmp(msg2, "ROUND-START\0") == 0) {
            cout << "ROUND STARTED" << endl;
            char wordMsg[200];
            readData(clientFd, wordMsg, sizeof(wordMsg));
            std::string word(wordMsg);
            GUI->prepareRound(word);
        } else if (strcmp(msg2, "SESSION-KILL\0") == 0) {
            GUI->gameOver();
        }
    }
}

void Client::waitForPlayers() {
    char msg2[100];
    readData(clientFd, msg2, sizeof(msg2));
    if (strcmp(msg2, "PLAYER-CHECK2\0") == 0) {
        memset(msg2, 0, sizeof(msg2));
        readData(clientFd, msg2, sizeof(msg2));
        if (strcmp(msg2, "ROUND-START\0") == 0) {
            cout << "ROUND STARTED" << endl;
            char wordMsg[200];
            readData(clientFd, wordMsg, sizeof(wordMsg));
            std::string word(wordMsg);
            GUI->prepareRound(word);
        } else if (strcmp(msg2, "SESSION-KILL\0") == 0) {
            GUI->gameOver();
        }
    }
}

void Client::onRoundFinish(bool winner) {
    if (winner) {
        auto stop = std::chrono::steady_clock::now();
        auto time_span = static_cast<std::chrono::duration<double>>(stop - GUI->startTimeMeasuring);
        char msgTime[100];
        sprintf(msgTime, "%.2f", time_span.count());
        writeData(clientFd, msgTime, sizeof(msgTime));
    } else {
        char msgLost[100];
        strcpy(msgLost, "PLAYER-LOST\0");
        writeData(clientFd, msgLost, sizeof(msgLost));
    }
}

int Client::checkIfAlreadyInGame() {
    char msg[100];
    readData(clientFd, msg, sizeof(msg));
    if (strcmp(msg, "AUTH-JOIN-EXISTS\0") == 0) {
        return AlreadyInGame::YES;
    } else {
        return AlreadyInGame::NO;
    }
}

void Client::sendIfWantsToRejoin(bool wantsToRejoin) {
    char msg[100];
    if (wantsToRejoin)
        strcpy(msg, ConnectionProcesses::JOINING_TO_EXISTING_SESSION);
    else
        strcpy(msg, ConnectionProcesses::NO_JOINING_TO_EXISTING_SESSION);
    writeData(clientFd, msg, sizeof(msg));
}

void Client::sendProgress(int part) {
    char msg[100];
    sprintf(msg, "%d-4", part);
    writeData(clientFd, msg, sizeof(msg));
}







