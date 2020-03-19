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
	int frame;								// zmienna przechowuj�ca numer klatki
	double czas_zmiany_klatki;				// zmienna wp�ywaj�ca na szybkos� zmiany klatek animacji

public:
	BlueGuy() = delete;
	~BlueGuy() = default;

	BlueGuy(string plik, float grav);										// konstruktor
	void draw(RenderTarget & target, RenderStates states) const override;	// funkcja do rysownaia na oknie
	void animacja(Clock & time);											// funkcja animuj�ca posta�

	void skok();															// funkcja odpowiadaj�ca za skok
	Vector2f grawitacja;													//  zmienna potrzbena do przeprowadzenia wyskoku
	Vector2f sila_wyskoku;													//  zmienna potrzbena do przeprowadzenia wyskoku

	void wroc();															// wraca na pozycj� startow�

	float gora();															// zwraca pozycj� g�rnej kraw�dzi
	float lewa();															// zwraca pozycj� lewej kraw�dzi
	float dol();															// zwraca pozycj� dolnej kraw�dzi
	float prawa();															// zwraca pozycj� prawej kraw�dzi

	void przyspiesz(double);												// funkcja przyspieszaj�ca animacj�
	void przywroc_predkosc();												// funkcja ustawiaj�ca domy�ln� pr�dko�c animacji
};

