#include <iostream>
#include <string>
#include <time.h>
#include <cstdlib>
#include <vector>
#include <fstream>
#include <cmath>
#include <algorithm>

using namespace std;

// STRUKTURY ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct Ciezarowka
{
    int x, y;
	long double trasa = 0;
	int towar = 0;
	bool koniec = false;
	vector<int> odwiedzone;

	string printMe()
	{
		string s;
		for (int i = 0; i < odwiedzone.size(); i++)
			s += to_string(odwiedzone[i]) + " ";
		s += "\n";
		return s;
	}
};

struct Wierzcholek
{
	int indeks, x, y, demand, readyTime, endTime, serviceTime;
};

// ZMIENNE GLOBALNE ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

vector<Wierzcholek> wierzcholki;
int capacity;

// FUNKCJE /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Wy�wietlanie danych
void dataPrinter()
{
	for (int i = 0; i < wierzcholki.size(); i++)
	{
		cout << "Wierzcholek " << wierzcholki[i].indeks << ": ";
		for (int j = 1; j < 7; j++)
		{
			int x;
			switch (j)
			{
			case 1:
				x = wierzcholki[i].x;
				break;
			case 2:
				x = wierzcholki[i].y;
				break;
			case 3:
				x = wierzcholki[i].demand;
				break;
			case 4:
				x = wierzcholki[i].readyTime;
				break;
			case 5:
				x = wierzcholki[i].endTime;
				break;
			case 6:
				x = wierzcholki[i].serviceTime;
				break;
			}
			cout << x << " ";
		}
		cout << endl;
	}
}

// Wczytywanie instancji
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
				v.demand = buffer;
				break;
			case 4:
				v.readyTime = buffer;
				break;
			case 5:
				v.endTime = buffer;
				break;
			case 6:
				v.serviceTime = buffer;
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

// Obliczanie dystansu
long double distance(int x1, int y1, int x2, int y2)
{
	return sqrt((pow(abs(x1 - x2), 2) + pow(abs(y1 - y2), 2)));
}

// Funkcja wyznaczajaca wierzcho�ek
int SELECT(Ciezarowka truck)
{
	if (wierzcholki.size() == 1)
		return 0;
	else
	{
		long double *priorytet = new long double[wierzcholki.size()];
		for (int i = 1; i < wierzcholki.size(); i++)
		{
			long double c = distance(truck.x, truck.y, wierzcholki[i].x, wierzcholki[i].y);
			long double e = wierzcholki[i].readyTime;
			long double t = truck.trasa;
			priorytet[i] = max(t + c, e);
		}

		int j;
		int selected;
		for (j = 1; j < wierzcholki.size(); j++)
		{
			if ((truck.towar >= wierzcholki[j].demand) &&
				(truck.trasa + distance(truck.x, truck.y, wierzcholki[j].x, wierzcholki[j].y) < wierzcholki[j].endTime))
			{
				long double travel = priorytet[j] + wierzcholki[j].serviceTime + distance(wierzcholki[j].x, wierzcholki[j].y, wierzcholki[0].x, wierzcholki[0].y);
				if (!(travel > wierzcholki[0].endTime))
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
			for (int i = 1; i < wierzcholki.size(); i++)
			{
				long double travel = priorytet[i] + wierzcholki[i].serviceTime + distance(wierzcholki[i].x, wierzcholki[i].y, wierzcholki[0].x, wierzcholki[0].y);
				if (!(travel > wierzcholki[0].endTime))
				{
					if ((truck.towar >= wierzcholki[i].demand) && (truck.trasa + distance(truck.x, truck.y, wierzcholki[i].x, wierzcholki[i].y) < wierzcholki[i].endTime))
					{
						if (priorytet[i] < priorytet[selected])
							selected = i;
						else if (priorytet[i] == priorytet[selected])
						{
							if (wierzcholki[i].serviceTime < wierzcholki[selected].serviceTime)
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

// Sumowanie objazd�w ci�ar�wek
long double sumTime(vector<Ciezarowka> c)
{
	long double sum = 0;
	for (int i = 0; i < c.size(); i++)
		sum += c[i].trasa;
	return sum;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// *** MAIN *** ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(int argc, char *argv[])
{
	
	bool working = true;
	bool noSolution = false;
	string filename;
	if (argc > 1)
		filename = argv[1];
	else
		filename = "input.txt";
	capacity = readCapacity(filename);
	wierzcholki = readPoints(filename);

	cout << "Obliczam, czekaj . . ." << endl;

	vector<Ciezarowka> trucks;
	int it = -1;
	while (working)
	{
		Ciezarowka c;
		c.koniec = false;
		c.towar = capacity;
		c.trasa = 0;
		c.x = wierzcholki[0].x;
		c.y = wierzcholki[0].y;
		trucks.push_back(c);
		it++;
		while (!trucks[it].koniec)
		{
			int gdzie = SELECT(trucks[it]);
			if ((trucks[it].trasa == 0) && (gdzie == 0))
			{
				noSolution = true;
				cout << "Nie mozna bylo dojechac wcale do jednego wierzcholka" << endl;
				break;
			}
			trucks[it].towar -= wierzcholki[gdzie].demand;
			int e = wierzcholki[gdzie].readyTime;
			long double c = distance(trucks[it].x, trucks[it].y, wierzcholki[gdzie].x, wierzcholki[gdzie].y);
			long double oczekiwanie = e - (trucks[it].trasa + c);
			if (oczekiwanie <= 0)
				trucks[it].trasa += (c + wierzcholki[gdzie].serviceTime);
			else
				trucks[it].trasa += (c + wierzcholki[gdzie].serviceTime + oczekiwanie);
			trucks[it].x = wierzcholki[gdzie].x;
			trucks[it].y = wierzcholki[gdzie].y;
			if (gdzie)
			{
				trucks[it].odwiedzone.push_back(wierzcholki[gdzie].indeks);
				wierzcholki.erase(wierzcholki.begin() + gdzie);
			}
			else
				trucks[it].koniec = true;
		}
		if (wierzcholki.size() == 1)
			working = false;
		if (noSolution)
			break;
	}

	fstream file;
	file.open("output.txt", ios::out);
	if (noSolution)
	{
		file << -1;
	}
	else
	{
		file << trucks.size() << " " << fixed << sumTime(trucks) << endl;
		for (int i = 0; i < trucks.size(); i++)
			file << trucks[i].printMe();
	}

	cout << "Koniec! :)" << endl;
	return 0;
}