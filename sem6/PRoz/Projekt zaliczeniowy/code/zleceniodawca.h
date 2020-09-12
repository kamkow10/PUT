#ifndef ZLECENIODAWCA_H
#define ZLECENIODAWCA_H

/* pętla główna procesu zleceniodawcy, tworzy co losowy czas zlecenia */
void jobMakerLoop();

/* wątek odbierający wiadmości, jedynym jego zadaniem jest aktualizowanie zegara Lamporta */
void *startListenThread(void *ptr);

/* wątek komunikacyjny: odbieranie wiadomości i reagowanie na nie poprzez zmiany stanu */
void *startMonitor(void *ptr);

#endif
