#pragma once
#include <SFML/Graphics.hpp>
#include "Przeszkoda.h"

using namespace std;
using namespace sf;

class BlueGuy : public Drawable
{
private:
	const float poz_x = 500, poz_y = 730;	// pozycja
	const float roz_x = 120, roz_y = 150;	// rozmiar
	string file;							// plik z obrazkiem
	Texture tekstura;						// grafika
	Sprite obraz;							// sprajt
	int frame;								// zmienna przechowuj¹ca numer klatki
	double czas_zmiany_klatki;				// zmienna wp³ywaj¹ca na szybkosæ zmiany klatek animacji

public:
	BlueGuy() = delete;
	~BlueGuy() = default;

	BlueGuy(string plik, float grav);										// konstruktor
	void draw(RenderTarget & target, RenderStates states) const override;	// funkcja do rysownaia na oknie
	void animacja(Clock & time);											// funkcja animuj¹ca postaæ

	void skok();															// funkcja odpowiadaj¹ca za skok
	Vector2f grawitacja;													//  zmienna potrzbena do przeprowadzenia wyskoku
	Vector2f sila_wyskoku;													//  zmienna potrzbena do przeprowadzenia wyskoku

	void wroc();															// wraca na pozycjê startow¹

	float gora();															// zwraca pozycjê górnej krawêdzi
	float lewa();															// zwraca pozycjê lewej krawêdzi
	float dol();															// zwraca pozycjê dolnej krawêdzi
	float prawa();															// zwraca pozycjê prawej krawêdzi

	void przyspiesz(double);												// funkcja przyspieszaj¹ca animacjê
	void przywroc_predkosc();												// funkcja ustawiaj¹ca domyœln¹ prêdkoœc animacji
};

