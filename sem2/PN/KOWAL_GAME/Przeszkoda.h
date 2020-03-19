#pragma once
#include <SFML/Graphics.hpp>

using namespace std;
using namespace sf;

class Przeszkoda : public Drawable
{
private:
	float roz_x, roz_y; // rozmiar
	float poz_x, poz_y; // pozycja
	Texture tekstura;	// grafika
	Sprite obraz;		// sprajt
	Vector2f predkosc;  // wektor predkosci

public:
	Przeszkoda() = delete;
	~Przeszkoda() = default;

	Przeszkoda(float X, float Y, float x, float y, string plik);			// konstruktor
	void draw(RenderTarget & target, RenderStates states) const override;	// funkcja do rysownaia na oknie

	void ruch();															// ruch obiektu
	void nadaj_predkosc(float x);											// nadanie predko�ci x
	void wroc();															// wraca na pozycj� startow�

	Vector2f pozycja();														// zwraca wektor aktualnej pozycji
	float gora();															// zwraca pozycj� g�rnej kraw�dzi
	float lewa();															// zwraca pozycj� lewej kraw�dzi
	float dol();															// zwraca pozycj� dolnej kraw�dzi
	float prawa();															// zwraca pozycj� prawej kraw�dzi

	void ustaw(float, float);												// funkcja ustawiaj�ca obiekt na poczatkowej pozycji
};

