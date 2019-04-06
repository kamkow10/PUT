#include <iostream>
#include <string>
#include <time.h>
#include <cstdlib>
#include <vector>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <random>
#include <chrono>
#include <iomanip>
#include <stdlib.h>
using namespace std;

// Lista struktur
/*
*   1. Mrówka - Odpowiednik ciężarówki.
*   2. Wierzchołek - Struktura przechowywująca informacje o kliencie.
*   3. Rozwiązanie - Struktura przechowywująca najważniejsze informacje,
*	   związane z danym rozwiązaniem problemu. 
*/

//--------------------------------------- STRUKTURY -------------------------------------------------------------------

struct Mrowka
{
	int x, y;							// Położenie mrówki
	long double trasa = 0;				// Trasa pokonana
	int towar = 0;						// Załadunek mrowki
	bool koniec = false;				// Czy wszystko obeszła
	vector<int> odwiedzone_wierzcholki; // Lista odwiedzonych wierzchołków
	int indeks_obecnego_wierzcholka;

	string printMe() // Funkcja zwracająca literał będący listą
	{				 // odwiedzonych wierzchołków przez mrówkę.
		string s;
		for (int i = 0; i < odwiedzone_wierzcholki.size(); i++)
			s += to_string(odwiedzone_wierzcholki[i]) + " ";
		s += "\n";
		return s;
	}
};

struct Wierzcholek
{
	int indeks, x, y, popyt, czas_gotowosci, czas_zakonczenia, czas_obslugi;
};

struct Rozwiazanie
{
	int liczba_ciezarowek;
	long double laczna_dlugosc_tras;
	vector<Mrowka> mrowki_uzyte_do_rozwiazania;
	bool puste = true; //Zmienna do main'a
};

//-----------------------------------------------------------------------------------------------------------\\

//--------------------------------------- ZMIENNE GLOBALNE -----------------------------------------------------------\\

vector<Wierzcholek> wierzcholki;			   // roboczy wektor na ktorym przeprowadzane sa operacje poszukiwania najlepszego rozwiazania
vector<Wierzcholek> wczytane_wierzcholki;	  // wektor przechowujacy wczytane z pliku wierzcholki
int pojemnosc_ciezarowek;					   // pojemnosc ciezarowek
long double **macierz_feromonow;			   // tablica feromonow krawedzi
long double **macierz_odleglosci_wierzcholkow; //tablica odleglosci

// Parametry
long double alfa = 2;
long double beta = 2;
long double parowanie = 0.2;
int Q = 1000000; // feromony
const long double domyslny_feromon = 1;

//----------------------------------------------------------------------------------------------------------------------------\\


/* Lista funkcji:
*   1. Wczytywanie wierzchołków instancji.
*   2. Wczytywanie pojemności ciężarówek instancji.
*   3. Obliczanie odległości pomiedzy dwoma punktami.
*   4. Obliczanie prawdopodobieństwa wyboru wierzchołka 'w' dla mrówki 'a'.
*   5. Wyznaczanie wierzcholka do odwiedzenia priorytetem zachłannym.
*	6. Wyznaczanie wierzcholka do odwiedzenia mrowkowo, po feromonach.
*   6. Nakładanie feromonów na trasach.
*	7. Obliczanie czasu tras wszystkich mrowek.
*	8. Generowanie losowych liczb z danego przedzialu.
*/

//------------------------------------------PROTOTYPY FUNKCJI ----------------------------------------------------------------\\


// Wczytywanie instancji
vector<Wierzcholek> readPoints(string filename);

// Wczytywanie pojemnosci ciezarowek
int readCapacity(string filename);

// Obliczanie dystansu
long double distance(int x1, int y1, int x2, int y2);

// Funkcja obliczajaca prawdopodobienstwo wybor wierzcholka "w" dla mrowki "ant"
long double propabilityFunction(Mrowka ant, Wierzcholek w);

int SELECT_GREEDY(Mrowka ant);

// Funkcja wyznaczajaca wierzcho�ek
int SELECT(Mrowka ant);

// Nakładanie feromonu przez mrowke
void addPheromons(Mrowka ant);

// Sumowanie objazdow ciezarowek
long double sumTime(vector<Mrowka> c);

thread_local std::mt19937 gen{std::random_device{}()};
template <typename T>
T random(T min, T max)
{
	using dist = conditional_t<
		is_integral<T>::value,
		uniform_int_distribution<T>,
		uniform_real_distribution<T>>;
	return dist{min, max}(gen);
}

//-------------------------------------------------------------------------------------------------------------\\


//------------------------------------------------------------------------------------------------------------------\\
// ------------------------------------------------*** MAIN ***-------------------------------------------------------\\

/* // Główne kroki:
*  1. Wczytaj dane.
*  2. Stwórz tablice do przechowywania wartosci feromonow i odlegosci, pomiedzy wierzchołkami. 
*  3. Na początku, aktywowana jest pojedyncza iteracja algorytmu z wyborem zachłannym, 
	  dajacym duze wartosci feromonow. Dzieki czemu, pozniejsze iteracje beda szukac 
	  wariacji zorientowanych wokol tej trasy.
*  4. Po niej, kolejne iteracje mrowkowe, do czasu zakonczenia programu, w tym parowanie i nakladanie 
*	  feromonow.
*  5. Wyniki. 
*/

int main(int argc, char *argv[])
{
	cout << "---------Start Programu---------\n"
		 << endl;

	// Start pomiaru czasu.
	clock_t start, koniec;
	start = (clock() / CLOCKS_PER_SEC);
	koniec = (clock() / CLOCKS_PER_SEC);
	int sekundy = 60;				   // Program trwa do 1 sekundy domyślnie.
	int licznik_iteracji_programu = 0; // Ile razy wykonał się algorytm.
	bool zachlanny = true;			   // Zmienna uruchamiająca wybor zachłanny. (1 iteracja)

	// Wczytanie danych
	string sciezka_pliku;
	if (argc > 1)
	{
		sciezka_pliku = argv[1];
		if (((sciezka_pliku[sciezka_pliku.size() - 1] != 't') ||
			 (sciezka_pliku[sciezka_pliku.size() - 2] != 'x') ||
			 (sciezka_pliku[sciezka_pliku.size() - 3] != 't') ||
			 (sciezka_pliku[sciezka_pliku.size() - 4] != '.')))
		{
			cout << "Odczyt domyslnej instancji: input.txt" << endl;
			sciezka_pliku = "input.txt";
		}
		else
		{
			cout << "Odczyt instancji: " << sciezka_pliku << endl;
		};
	}
	else
	{
		sciezka_pliku = "input.txt";
	}
	if (argc > 2)
	{
		sekundy = atoi(argv[2]);
	};
	if (argc > 3)
	{
		alfa = strtold(argv[3], NULL);
	};
	if (argc > 4)
	{
		::beta = strtold(argv[4], NULL);
	};
	if (argc > 5)
	{
		parowanie = strtold(argv[5], NULL);
	}
	if (argc > 6)
	{
		Q = atoi(argv[6]);
	}
	cout << "Czas dzialania ustawiono na " << sekundy << " sek " << endl;
	cout << "Ustawiono alfę na: " << alfa << endl;
	cout << "Ustawiono betę na: " << ::beta << endl;
	cout << "Ustawiono parowanie = " << parowanie * 100 << "%" << endl;
	cout << "Ustawiono Q = " << fixed << Q << endl;
	cout << "\n"
		 << endl;
	pojemnosc_ciezarowek = readCapacity(sciezka_pliku);
	wczytane_wierzcholki = readPoints(sciezka_pliku);

	// Tworzenie macierzy feromonow i odlegosci dla kazdej pary wierzcholkow
	macierz_feromonow = new long double *[wczytane_wierzcholki.size()];
	macierz_odleglosci_wierzcholkow = new long double *[wczytane_wierzcholki.size()];
	for (int i = 0; i < wczytane_wierzcholki.size(); i++) //dla danej lczby wierzcholkow
	{
		macierz_feromonow[i] = new long double[wczytane_wierzcholki.size()];
		macierz_odleglosci_wierzcholkow[i] = new long double[wczytane_wierzcholki.size()];
		for (int j = 0; j < wczytane_wierzcholki.size(); j++)
		{
			if (i == j) //Jeśli wierzchołek sam ze soba, to nie ma feromonów, a jego odleglosc od siebie samego to 0
			{
				macierz_feromonow[i][j] = 0;
				macierz_odleglosci_wierzcholkow[i][j] = 0;
			}
			else //Dwa różne wierzchołki, dostają wartość domyślną feromonów, oraz obliczana jest odległość między nimi
			{
				macierz_feromonow[i][j] = domyslny_feromon;
				macierz_odleglosci_wierzcholkow[i][j] = distance(wczytane_wierzcholki[i].x, wczytane_wierzcholki[i].y, wczytane_wierzcholki[j].x, wczytane_wierzcholki[j].y);
			}
		}
	};

	bool working, brak_wyniku, uplynal_czas = false;

	Rozwiazanie DOBRE_ROZWIAZANIE; // Zmienna przechowująca najlepsze ze znalezionych rozwiazań.

	cout << "Dane wczytane, rozpoczynam prace.\n"
		 << endl;

	// ****** START ALGORYTMU *************************************************
	while (koniec - start <= sekundy * 1)
	{
		wierzcholki = wczytane_wierzcholki;

		working = true;		 // Zapetlone ddzialanie algorytmu, tak dlugo jak
		brak_wyniku = false; // Jeśli nie znaleziono rozwiązania problemu to true.

		vector<Mrowka> mrowisko; // Przechowuje wszystkie mrówki powołane do życia. :-)
		int it = -1;

		if (zachlanny)
		{
			while (working)
			{
				Mrowka c;
				c.koniec = false;				//Na poczatku, mrówka nie moze miec konca
				c.towar = pojemnosc_ciezarowek; // Dostaje zaladunek
				c.trasa = 0;					// Dystans 0
				c.x = wierzcholki[0].x;			// Ustawienie polozenia w bazie
				c.y = wierzcholki[0].y;
				mrowisko.push_back(c);		 // Dodaje mrowke do zbioru
				it++;						 //Numer mrowki
				while (!mrowisko[it].koniec) //Tak dlugo jak mrowka moze odwiedzic wierzch
				{
					int gdzie = SELECT_GREEDY(mrowisko[it]);	   //Wybor zachlanny
					if ((mrowisko[it].trasa == 0) && (gdzie == 0)) //Jezeli wybor zwroci wierz. w bazie to koniec
					{
						brak_wyniku = true;
						cout << "Nie mozna bylo dojechac wcale do jednego wierzcholka" << endl;
						break;
					}
					mrowisko[it].towar -= wierzcholki[gdzie].popyt; //Mrowka oddaje czesc zasobow
					int e = wierzcholki[gdzie].czas_gotowosci;		//Zmienne do priorytetu
					long double c = distance(mrowisko[it].x, mrowisko[it].y, wierzcholki[gdzie].x, wierzcholki[gdzie].y);
					long double oczekiwanie = e - (mrowisko[it].trasa + c);			 // Gotowy czas - (przebyta droga+trasa do wierzch)
					if (oczekiwanie <= 0)											 //Jesli nie trzeba czekac
						mrowisko[it].trasa += (c + wierzcholki[gdzie].czas_obslugi); //Do trasy dojazd i czas obslugi
					else															 //Jesli trzeba czekac to jeszcze dodaj czas oczekiwania
						mrowisko[it].trasa += (c + wierzcholki[gdzie].czas_obslugi + oczekiwanie);
					mrowisko[it].x = wierzcholki[gdzie].x; //Mrowka wchodzi do wierzcholka
					mrowisko[it].y = wierzcholki[gdzie].y;
					if (gdzie) //Jesli jest wiecej niz jeden wierzcholek (z listy przetwarzanych)
					{		   //To dodaj wybrany
						mrowisko[it].odwiedzone_wierzcholki.push_back(wierzcholki[gdzie].indeks);
						wierzcholki.erase(wierzcholki.begin() + gdzie); //Usuwa wierzcholek od pozycji poczatkowej
					}
					else //Jezeli nie ma wierzcholkow to koniec
						mrowisko[it].koniec = true;
				}
				if (wierzcholki.size() == 1) //Koniec petli gdy zostal jeden do wyboru
					working = false;
				if (brak_wyniku)
					break;
			}
		}
		else
		{
			while (working)
			{
				Mrowka m;
				m.koniec = false;
				m.towar = pojemnosc_ciezarowek;
				m.trasa = 0;
				m.x = wierzcholki[0].x;
				m.y = wierzcholki[0].y;
				m.indeks_obecnego_wierzcholka = 0;
				mrowisko.push_back(m);
				it++;
				while (!mrowisko[it].koniec)
				{
					int gdzie = SELECT(mrowisko[it]); //Wybor mrowkowy
					if ((mrowisko[it].trasa == 0) && (gdzie == 0))
					{
						brak_wyniku = true;
						cout << "Nie mozna bylo dojechac wcale do jednego wierzcholka" << endl;
						break;
					}
					for (int i = 0; i < wierzcholki.size(); i++)
					{
						if (wierzcholki[i].indeks == gdzie)
						{
							gdzie = i;
							break;
						}
					}
					mrowisko[it].towar -= wierzcholki[gdzie].popyt;
					int e = wierzcholki[gdzie].czas_gotowosci;
					long double c = macierz_odleglosci_wierzcholkow[mrowisko[it].indeks_obecnego_wierzcholka][wierzcholki[gdzie].indeks];
					long double oczekiwanie = e - (mrowisko[it].trasa + c);
					if (oczekiwanie <= 0)
						mrowisko[it].trasa += (c + wierzcholki[gdzie].czas_obslugi);
					else
						mrowisko[it].trasa += (c + wierzcholki[gdzie].czas_obslugi + oczekiwanie);
					mrowisko[it].x = wierzcholki[gdzie].x;
					mrowisko[it].y = wierzcholki[gdzie].y;
					mrowisko[it].indeks_obecnego_wierzcholka = wierzcholki[gdzie].indeks;
					if (gdzie)
					{
						mrowisko[it].odwiedzone_wierzcholki.push_back(wierzcholki[gdzie].indeks);
						wierzcholki.erase(wierzcholki.begin() + gdzie);
					}
					else
						mrowisko[it].koniec = true;
				}
				if (wierzcholki.size() == 1)
					working = false;
				if (brak_wyniku)
					break;
				koniec = (clock() / CLOCKS_PER_SEC);
				if (!(koniec - start <= sekundy * 1))
				{
					uplynal_czas = true;
					break;
				}
			}
		}
		if (uplynal_czas)
			break;

		if (brak_wyniku)
		{
			fstream file;
			file.open("output.txt", ios::out);
			file << -1;
			break;
		}

		zachlanny = false;
		// Wszystkie operacje oraz zapisywanie rozwiazania jezeli jest lepsze
		if ((DOBRE_ROZWIAZANIE.puste) || ((DOBRE_ROZWIAZANIE.liczba_ciezarowek > mrowisko.size()) || ((DOBRE_ROZWIAZANIE.liczba_ciezarowek == mrowisko.size()) && (DOBRE_ROZWIAZANIE.laczna_dlugosc_tras > sumTime(mrowisko)))))
		{
			DOBRE_ROZWIAZANIE.liczba_ciezarowek = mrowisko.size();
			DOBRE_ROZWIAZANIE.laczna_dlugosc_tras = sumTime(mrowisko);
			DOBRE_ROZWIAZANIE.mrowki_uzyte_do_rozwiazania = mrowisko;
			DOBRE_ROZWIAZANIE.puste = false;

			cout << DOBRE_ROZWIAZANIE.liczba_ciezarowek << " " << DOBRE_ROZWIAZANIE.laczna_dlugosc_tras << endl;

			// Parowanie feromonow
			for (int i = 0; i < wczytane_wierzcholki.size(); i++)
				for (int j = 0; j < wczytane_wierzcholki.size(); j++)
					macierz_feromonow[i][j] = (1.0 - parowanie) * macierz_feromonow[i][j];

			// Nakladanie feromonow
			for (int i = 0; i < mrowisko.size(); i++)
				addPheromons(mrowisko[i]);
		}

		licznik_iteracji_programu++;
		koniec = clock() / CLOCKS_PER_SEC;
	}
	// ****** KONIEC ALGORYTMU *************************************************
	if (licznik_iteracji_programu == 0)
	{
		cout << "Program nie zdarzyl wykonac sie ani razu!" << endl;
		cout << "Program konczy dzialanie." << endl;
	}

	else
	{
		cout << "Ile razy wykonal sie algorytm: " << licznik_iteracji_programu << endl;

		cout << "Koniec, trwa zapis do pliku" << endl;
		if (!brak_wyniku)
		{
			fstream file;
			file.open("output.txt", ios::out);
			file << DOBRE_ROZWIAZANIE.liczba_ciezarowek << " " << fixed << DOBRE_ROZWIAZANIE.laczna_dlugosc_tras << endl;
			for (int i = 0; i < DOBRE_ROZWIAZANIE.liczba_ciezarowek; i++)
				file << DOBRE_ROZWIAZANIE.mrowki_uzyte_do_rozwiazania[i].printMe();
		}
		cout << "Zapisano :-)" << endl;
	}

	return 0;
};

//==============================================================================================================\\


//---------------------------------------------------Funkcje----------------------------------------------------\\

//Wczytaj wierzcholki
vector<Wierzcholek> readPoints(string filename)
{
	fstream file;
	file.open(filename, ios::in);
	if (!file.good())
	{
		cout << "Blad przy otwieraniu pliku " << filename << endl;
		exit(0);
	}
	string s; // pomocnicza zmienna
	for (int i = 0; i < 8; i++)
		getline(file, s);

	bool stop = false;
	vector<Wierzcholek> V;
	while (!file.eof())
	{
		Wierzcholek v;
		int buffer;
		for (int j = 0; j < 7; j++)
		{
			file >> buffer;
			if (file.eof())
			{
				stop = true;
				break;
			}
			switch (j)
			{
			case 0:
				v.indeks = buffer;
				break;
			case 1:
				v.x = buffer;
				break;
			case 2:
				v.y = buffer;
				break;
			case 3:
				v.popyt = buffer;
				break;
			case 4:
				v.czas_gotowosci = buffer;
				break;
			case 5:
				v.czas_zakonczenia = buffer;
				break;
			case 6:
				v.czas_obslugi = buffer;
				break;
			}
		}
		if (stop)
			break;
		else
			V.push_back(v);
	}

	file.close();

	return V;
}

// Wczytywanie pojemnosci ciezarowek
int readCapacity(string filename)
{
	fstream file;
	file.open(filename, ios::in);
	if (!file.good())
	{
		cout << "Blad przy otwieraniu pliku " << filename << endl;
		exit(0);
	}
	string s; // zmienna pomocnicza
	for (int i = 0; i < 4; i++)
		getline(file, s);
	int capacity;
	file >> capacity;
	file >> capacity;
	return capacity;

	file.close();
}

// Obliczanie dystansu miedzy dwoma punktami
long double distance(int x1, int y1, int x2, int y2)
{
	return sqrt((pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2)));
}

// Funkcja obliczajaca prawdopodobienstwo wyboru wierzcholka "w" dla mrowki "ant"
long double propabilityFunction(Mrowka ant, Wierzcholek w)
{
	if (macierz_odleglosci_wierzcholkow[ant.indeks_obecnego_wierzcholka][w.indeks]) //Jesli nie zerowa odleglosc
		return (pow(macierz_feromonow[ant.indeks_obecnego_wierzcholka][w.indeks], alfa) * pow(1.0 / macierz_odleglosci_wierzcholkow[ant.indeks_obecnego_wierzcholka][w.indeks], ::beta));
	else //Jesli zerowa (nie dzielimy przez 0)
		return (pow(macierz_feromonow[ant.indeks_obecnego_wierzcholka][w.indeks], alfa));
}

int SELECT_GREEDY(Mrowka ant)
{
	if (wierzcholki.size() == 1) //Jesli tylko jeden wierzcholek w przetwarzanych to zwroc 0
		return 0;
	else
	{
		long double *priorytet = new long double[wierzcholki.size()];
		for (int i = 1; i < wierzcholki.size(); i++) //Dla przetwarzanych wierzch wypelnij tablice priorytetow
		{
			long double c = distance(ant.x, ant.y, wierzcholki[i].x, wierzcholki[i].y);
			long double e = wierzcholki[i].czas_gotowosci;
			long double t = ant.trasa;
			priorytet[i] = max(t + c, e);
		}

		int j;
		int selected;
		for (j = 1; j < wierzcholki.size(); j++) //Jak moze dac towar i dojechac w czasie do wierzch
		{
			if ((ant.towar >= wierzcholki[j].popyt) &&
				(ant.trasa + distance(ant.x, ant.y, wierzcholki[j].x, wierzcholki[j].y) < wierzcholki[j].czas_zakonczenia))
			{ // To wtedy trasa to priorytet i czas obslugi i dojechanie do bazy
				long double travel = priorytet[j] + wierzcholki[j].czas_obslugi + distance(wierzcholki[j].x, wierzcholki[j].y, wierzcholki[0].x, wierzcholki[0].y);
				if (!(travel > wierzcholki[0].czas_zakonczenia)) //Jezeli znajdzie taki co zdarzy dojechac w czasie do bazy to wybierz
				{
					selected = j;
					break;
				}
			}
		}
		if (j == wierzcholki.size())
			return 0;
		else
		{
			for (int i = 1; i < wierzcholki.size(); i++) //jeszcze raz sprawdza, tym razem porownuje wyniki, czy znajdzie lepszy
			{
				long double travel = priorytet[i] + wierzcholki[i].czas_obslugi + distance(wierzcholki[i].x, wierzcholki[i].y, wierzcholki[0].x, wierzcholki[0].y);
				if (!(travel > wierzcholki[0].czas_zakonczenia))
				{
					if ((ant.towar >= wierzcholki[i].popyt) && (ant.trasa + distance(ant.x, ant.y, wierzcholki[i].x, wierzcholki[i].y) < wierzcholki[i].czas_zakonczenia))
					{
						if (priorytet[i] < priorytet[selected])
							selected = i;
						else if (priorytet[i] == priorytet[selected])
						{
							if (wierzcholki[i].czas_obslugi < wierzcholki[selected].czas_obslugi)
								selected = i;
						}
					}
				}
			}
			return selected;
		}
		delete[] priorytet;
	}
}

// Funkcja wyznaczajaca wierzcho�ek
int SELECT(Mrowka ant)
{
	if (wierzcholki.size() == 1)
		return 0;
	else
	{
		vector<Wierzcholek> dostepneWierzcholki;
		for (int j = 1; j < wierzcholki.size(); j++)
		{ // Jesli moze dac towar i dojechac
			long double odleglosc = macierz_odleglosci_wierzcholkow[ant.indeks_obecnego_wierzcholka][wierzcholki[j].indeks];
			if ((ant.towar >= wierzcholki[j].popyt) && (ant.trasa + odleglosc < (long double)wierzcholki[j].czas_zakonczenia))
			{
				long double travel = max(odleglosc + ant.trasa, (long double)wierzcholki[j].czas_gotowosci) + wierzcholki[j].czas_obslugi + macierz_odleglosci_wierzcholkow[wierzcholki[j].indeks][wierzcholki[0].indeks];
				if (!(travel > wierzcholki[0].czas_zakonczenia))
				{ //Jak zdarzy wrocic do dodaj do dostepnych
					dostepneWierzcholki.push_back(wierzcholki[j]);
				}
			}
		}
		if (dostepneWierzcholki.size() == 0)
			return 0;
		else
		{ //Rozklad prawdopodobienstwa dla dostepnych wierzcholkow
			long double *przedzialyPrawdopodobienstwa = new long double[dostepneWierzcholki.size()];
			long double sumaPrawdopodobienstwa = 0;
			for (int i = 0; i < dostepneWierzcholki.size(); i++)
				sumaPrawdopodobienstwa += propabilityFunction(ant, dostepneWierzcholki[i]);
			long double prawdopodobienstwo;
			for (int i = 0; i < dostepneWierzcholki.size(); i++)
			{
				prawdopodobienstwo = propabilityFunction(ant, dostepneWierzcholki[i]) / sumaPrawdopodobienstwa;
				if (i)
					przedzialyPrawdopodobienstwa[i] = przedzialyPrawdopodobienstwa[i - 1] + prawdopodobienstwo;
				else
					przedzialyPrawdopodobienstwa[i] = prawdopodobienstwo;
			}

			long double wylosowana = random(0.00000, 1.00000);
			int selected = 0;

			for (int i = 0; i < dostepneWierzcholki.size(); i++)
			{
				if (i == 0)
				{
					if ((wylosowana >= 0) && (wylosowana <= przedzialyPrawdopodobienstwa[i]))
					{
						selected = i;
						break;
					}
				}
				else
				{
					if ((wylosowana >= przedzialyPrawdopodobienstwa[i - 1]) && (wylosowana <= przedzialyPrawdopodobienstwa[i]))
					{
						selected = i;
						break;
					}
				}
			}

			delete[] przedzialyPrawdopodobienstwa;
			return dostepneWierzcholki[selected].indeks;
		}
	}
}

// Nakładanie feromonu przez mrowke
void addPheromons(Mrowka ant)
{
	macierz_feromonow[0][ant.odwiedzone_wierzcholki[0]] += Q / ant.trasa;
	macierz_feromonow[ant.odwiedzone_wierzcholki[ant.odwiedzone_wierzcholki.size() - 1]][0] += Q / ant.trasa;
	for (int i = 0; i < ant.odwiedzone_wierzcholki.size() - 1; i++)
		macierz_feromonow[ant.odwiedzone_wierzcholki[i]][ant.odwiedzone_wierzcholki[i + 1]] += Q / ant.trasa;
}

// Sumowanie objazdow ciezarowek
long double sumTime(vector<Mrowka> c)
{
	long double sum = 0;
	for (int i = 0; i < c.size(); i++) //Dla kazdej mrowki
		sum += c[i].trasa;
	return sum;
}