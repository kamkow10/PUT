#include "Main.h"
#include <SFML/Graphics.hpp>
#include <windows.h>
#include <cstdlib>
#include <time.h>
#include <iostream>
#include <SFML/Audio.hpp>
#include <fstream>

// Wymiary okna ////
#define X 1920    //
#define Y 1080    //
////////////////////

using namespace std;
using namespace sf;

// *** ZMIENNE GLOBALNE ****************************************************************************************************************************************************************************
// *************************************************************************************************************************************************************************************************
int SPEED = 10;													// globalna prêdkosc gry	
Clock zegar, level, TIME;										// zmienne czasowe
bool w_gorze = false;											// zmienna informuj¹ca czy gracz jest na ziemi
bool ruch[6] = { false, false, false, false, false, false };	// tablica informuj¹ca czy przeszkoda jest wruchu
bool po[6] = { false, false, false, false, false, false };		// tablica pomocnicza do "wypuszczania" przeszkód
bool working = true;											// zmienna potrzebna do zapauzowania gry
bool let_it_go = true;											// zmienna pomocnicza do "wypuszczania" przeszkód
bool napisano = false;											// zmienna pomocnicza do wypisywania napisów

// Przeszkody (po 2)
Przeszkoda kolid1_1(X, Y - 80 - 200, 70, 80, "kolid1.png");
Przeszkoda kolid1_2(X, Y - 80 - 200, 70, 80, "kolid1.png");
Przeszkoda kolid2_1(X, Y - 100 - 200, 100, 100, "kolid2.png");
Przeszkoda kolid2_2(X, Y - 100 - 200, 100, 100, "kolid2.png");
Przeszkoda kolid3_1(X, Y - 60 - 200, 90, 60, "kolid3.png");
Przeszkoda kolid3_2(X, Y - 60 - 200, 90, 60, "kolid3.png");

// T³o
Przeszkoda ziemia1(0, Y - 200, 1920, 200, "grass.png");
Przeszkoda ziemia2(1920, Y - 200, 1920, 200, "grass.png");
Przeszkoda ziemia3(3840, Y - 200, 1920, 200, "grass.png");
Przeszkoda tlo1(0, 0, 3840, 880, "tlo.png");
Przeszkoda tlo2(3840, 0, 3840, 880, "tlo.png");
Przeszkoda chmury1(0, 50, 3840, 880, "clouds.png");
Przeszkoda chmury2(3840, 50, 3840, 880, "clouds.png");

// Postaæ
BlueGuy gracz("postac.png", 1);

//	wskazniki potrzebne do renderowania pod³o¿a :
Przeszkoda * ziemia_pierwszy = &ziemia1;
Przeszkoda * ziemia_srodek = &ziemia2;
Przeszkoda * ziemia_ostatni = &ziemia3;

// muzyka
SoundBuffer Bjump, Bdead, Bspeedup, Bvictoria;
Sound jump, dead, speedup, victoria;

// Tekst
Przeszkoda tekst(0, 0, 1920, 1080, "napis.png");
Font czcionka;
Text punkty, wynik, rekord;
int score, record;
// *************************************************************************************************************************************************************************************************
// *************************************************************************************************************************************************************************************************					


// *** FUNKCJE *************************************************************************************************************************************************************************************
// *************************************************************************************************************************************************************************************************
void wyskok(BlueGuy & postac)
{
	if (((postac.sila_wyskoku.y == 0) && (Keyboard::isKeyPressed(Keyboard::Space))) && (w_gorze == false))
	{
		postac.sila_wyskoku.y = -25;
		postac.skok();
		w_gorze = true;
		jump.play();
	}
	else if ((postac.sila_wyskoku.y < 0) && (Keyboard::isKeyPressed(Keyboard::Space)))
	{
		postac.skok();
	}
	else
	{
		if (w_gorze)
		{
			if (postac.sila_wyskoku.y < 0) postac.sila_wyskoku.y = 0;
			postac.skok();
			if (postac.gora() > 730)
			{
				w_gorze = false;
				postac.wroc();
				postac.sila_wyskoku.y = 0;
			}
		}
	}

}
void sprawdz_kolizje(BlueGuy postac, Przeszkoda przeszkoda)
{
	int dod = 30;
	if ((postac.dol() - dod >= przeszkoda.gora()) && (postac.prawa() - dod >= przeszkoda.lewa()) && postac.lewa() <= przeszkoda.prawa() - dod)
	{
		dead.play();
		working = false;
	}
}
void ruch_podloza(Przeszkoda & grass1, Przeszkoda & grass2, Przeszkoda & grass3)
{
	if (ziemia_pierwszy->lewa() >= -1920)
	{
		grass1.ruch();
		grass2.ruch();
		grass3.ruch();
	}
	else
	{
		Przeszkoda * p;
		ziemia_pierwszy->ustaw(ziemia_ostatni->prawa(), 880);
		p = ziemia_pierwszy;
		ziemia_pierwszy = ziemia_srodek;
		ziemia_srodek = ziemia_ostatni;
		ziemia_ostatni = p;

	}
}
void ruch_tla(Przeszkoda & bc1, Przeszkoda & bc2)
{
	if (bc1.lewa() >= -3840)
	{
		bc1.ruch();
		bc2.ruch();
	}
	else
	{
		bc1.wroc();
		bc2.wroc();
	}
}
void dokonaj_ruchu(int wylosowana, int numer, Przeszkoda & obiekt, int rozmiar)
{
	if (((wylosowana == numer) || (ruch[numer])) && (obiekt.pozycja().x >= -rozmiar))
	{
		ruch[numer] = true;
		if (obiekt.lewa() == 1920)
			let_it_go = false;
		obiekt.ruch();
		if ((obiekt.prawa() <= 1600) && (!po[numer]))
		{
			let_it_go = true;
			po[numer] = true;
		}
	}
	else if (!(obiekt.pozycja().x >= -rozmiar))
	{
		obiekt.wroc();
		ruch[numer] = false;
		po[numer] = false;
	}
}
void losowanie_przeszkody()
{
	int los = rand() % 200;
	if (ruch[0] || let_it_go) dokonaj_ruchu(los, 0, kolid1_1, 70);
	if (ruch[1] || let_it_go) dokonaj_ruchu(los, 1, kolid1_2, 70);
	if (ruch[2] || let_it_go) dokonaj_ruchu(los, 2, kolid2_1, 100);
	if (ruch[3] || let_it_go) dokonaj_ruchu(los, 3, kolid2_2, 100);
	if (ruch[4] || let_it_go) dokonaj_ruchu(los, 4, kolid3_1, 60);
	if (ruch[5] || let_it_go) dokonaj_ruchu(los, 5, kolid3_2, 60);
}
void RysujWszystko(RenderWindow & wind)
{
	wind.draw(tlo1);
	wind.draw(tlo2);
	wind.draw(chmury1);
	wind.draw(chmury2);
	wind.draw(ziemia1);
	wind.draw(ziemia2);
	wind.draw(ziemia3);
	wind.draw(kolid1_1);
	wind.draw(kolid1_2);
	wind.draw(kolid2_1);
	wind.draw(kolid2_2);
	wind.draw(kolid3_1);
	wind.draw(kolid3_2);
	wind.draw(gracz);
	if (working)
		wind.draw(punkty);
}
void nadaj_pred()
{
	kolid1_1.nadaj_predkosc(SPEED);
	kolid1_2.nadaj_predkosc(SPEED);
	kolid2_1.nadaj_predkosc(SPEED);
	kolid2_2.nadaj_predkosc(SPEED);
	kolid3_1.nadaj_predkosc(SPEED);
	kolid3_2.nadaj_predkosc(SPEED);
	ziemia1.nadaj_predkosc(SPEED);
	ziemia2.nadaj_predkosc(SPEED);
	ziemia3.nadaj_predkosc(SPEED);
	tlo1.nadaj_predkosc(SPEED / 30.0);
	tlo2.nadaj_predkosc(SPEED / 30.0);
	chmury1.nadaj_predkosc(SPEED / 50.0);
	chmury2.nadaj_predkosc(SPEED / 50.0);
	gracz.przywroc_predkosc();
}
void zwieksz_pred()
{
	if (level.getElapsedTime().asSeconds() > 10)
	{
		speedup.play();
		SPEED += 2;

		kolid1_1.nadaj_predkosc(SPEED);
		kolid1_2.nadaj_predkosc(SPEED);
		kolid2_1.nadaj_predkosc(SPEED);
		kolid2_2.nadaj_predkosc(SPEED);
		kolid3_1.nadaj_predkosc(SPEED);
		kolid3_2.nadaj_predkosc(SPEED);
		ziemia1.nadaj_predkosc(SPEED);
		ziemia2.nadaj_predkosc(SPEED);
		ziemia3.nadaj_predkosc(SPEED);
		tlo1.nadaj_predkosc(SPEED / 30.0);
		tlo2.nadaj_predkosc(SPEED / 30.0);
		chmury1.nadaj_predkosc(SPEED / 50.0);
		chmury2.nadaj_predkosc(SPEED / 50.0);
		gracz.przyspiesz(1.1);
		level.restart();
	}
}
void RESTART()
{
	SPEED = 10;
	zegar.restart();
	level.restart();
	TIME.restart();
	w_gorze = false;
	for (int i = 0;i < 6;i++)
	{
		ruch[i] = false;
		po[i] = false;
	}
	let_it_go = true;
	// Przeszkody
	kolid1_1.wroc();
	kolid1_2.wroc();
	kolid2_1.wroc();
	kolid2_2.wroc();
	kolid3_1.wroc();
	kolid3_2.wroc();
	// Reszta
	ziemia1.wroc();
	ziemia2.wroc();
	ziemia3.wroc();
	tlo1.wroc();
	tlo2.wroc();
	chmury1.wroc();
	chmury2.wroc();

	ziemia_pierwszy = &ziemia1;
	ziemia_srodek = &ziemia2;
	ziemia_ostatni = &ziemia3;

	gracz.wroc();
	gracz.sila_wyskoku.y = 0;

	nadaj_pred();

}
void wczytaj_rekord()
{
	fstream plik;
	plik.open("rekord.txt", ios::in);
	if (plik.good() == false)
	{
		record = 0;
	}
	else
	{
		plik >> record;
	}
	plik.close();
}
void zapisz_rekord()
{
	fstream plik;
	plik.open("rekord.txt", ios::out);
	plik << score;
	plik.close();
}
void wczytaj_dzwiek()
{
	Bjump.loadFromFile("jump.wav");
	Bdead.loadFromFile("dead.wav");
	Bspeedup.loadFromFile("speedup.wav");
	Bvictoria.loadFromFile("victoria.wav");
	jump.setBuffer(Bjump);
	dead.setBuffer(Bdead);
	speedup.setBuffer(Bspeedup);
	victoria.setBuffer(Bvictoria);
}
void wczytaj_tekst()
{
	czcionka.loadFromFile("consola.ttf"); // wczytanie czcionki

	punkty.setFont(czcionka);
	punkty.setCharacterSize(50);
	punkty.setFillColor(sf::Color::Red);
	punkty.setStyle(Text::Bold);
	punkty.setPosition(50, 20);

	wynik.setFont(czcionka);
	wynik.setCharacterSize(100);
	wynik.setFillColor(sf::Color::Red);
	wynik.setStyle(Text::Bold);
	wynik.setPosition(650, 400);

	rekord.setFont(czcionka);
	rekord.setCharacterSize(100);
	rekord.setFillColor(sf::Color::Red);
	rekord.setStyle(Text::Bold);
	rekord.setPosition(600, 550);
}
void zderzenie()
{
	sprawdz_kolizje(gracz, kolid1_1);
	sprawdz_kolizje(gracz, kolid1_2);
	sprawdz_kolizje(gracz, kolid2_1);
	sprawdz_kolizje(gracz, kolid2_2);
	sprawdz_kolizje(gracz, kolid3_1);
	sprawdz_kolizje(gracz, kolid3_2);
}
// *************************************************************************************************************************************************************************************************
// *************************************************************************************************************************************************************************************************




// *********************** /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ******* M A I N ******* /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// *********************** /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main()
{
	RenderWindow okno(VideoMode(X, Y, 32), "Okienko",Style::Fullscreen);
	srand(time(NULL));
	okno.setFramerateLimit(60);
	Event zdarzenie;

	nadaj_pred();		// nadanie prêdkoœci pocz¹tkowej wszytskim obiektom
	wczytaj_dzwiek();	// wczytuje pliki dŸwiêkowe
	wczytaj_tekst();	// wczytuje napisy

	// Muzyka
	Music music;
	music.openFromFile("music.wav");
	music.setLoop(true);
	music.play();
	music.setVolume(60);

	// *************************
	// ***** PÊTLA G£ÓWNA ******
	// *************************

	while (true)
	{

		while (okno.pollEvent(zdarzenie))
		{
			if (zdarzenie.type == Event::KeyPressed)
			{
				// ESC = wy³¹czenie
				if (zdarzenie.key.code == Keyboard::Escape)
				{
					okno.close();
					return 0;
				}
				// Rozpoczêcie gry od nowa po klikniêciu SPACJI
				if (((zdarzenie.key.code == Keyboard::Space) && (!working)) && napisano)
				{
					RESTART();
					working = true;
					napisano = false;
				}
			}
		}

		if (working)
		{
			okno.clear();

			// Sprawdza, czy minelo 10s, je¿eli tak - zwieksza predkosc gry
			zwieksz_pred(); 
			// Wypisuje punkty
			score = (int)(round(10 * TIME.getElapsedTime().asSeconds())); 
			punkty.setString("Punkty: " + to_string(score));
			// Funkcja odpowiadaj¹ca za "wypuszczanie" przeszkód (z czynnikiem losowym)
			losowanie_przeszkody();
			// Ruch t³a
			ruch_tla(tlo1, tlo2);
			ruch_tla(chmury1, chmury2);
			ruch_podloza(ziemia1, ziemia2, ziemia3);
			// Animowanie postaci gracza
			gracz.animacja(zegar);
			// Funkcja zale¿na od akcji gracza, odpowiadaj¹ca za wyskok postaci
			wyskok(gracz);
			// RYSUJE WSZYSTKO NA PLANSZY
			RysujWszystko(okno);
			// Sprawdza mo¿liwe kolizje postaci z przeszkodami
			zderzenie();

			okno.display();
		}
		else
		{
			// Gra siê zatrzyma³a - wypisz wszystkie napisy, je¿eli nie zosta³y wczesniej wypisane
			if (!napisano)
			{
				wczytaj_rekord();
				wynik.setString("Wynik: " + to_string(score));
				// Je¿eli pobito rekord
				if (score > record)
				{
					wynik.setFillColor(sf::Color::Yellow);
					wynik.setStyle(Text::Bold | Text::Underlined);
					rekord.setString("Rekord: " + to_string(score));
					victoria.play();
					zapisz_rekord();
				}
				// Je¿eli nie pobito rekordu
				else
				{
					wynik.setFillColor(sf::Color::Red);
					wynik.setStyle(Text::Bold);
					rekord.setString("Rekord: " + to_string(record));
				}
				okno.clear(Color::Black);
				RysujWszystko(okno);
				okno.draw(tekst);
				okno.draw(wynik);
				okno.draw(rekord);
				okno.display();
				napisano = true;
			}
		}
	}

	return 0;
}
