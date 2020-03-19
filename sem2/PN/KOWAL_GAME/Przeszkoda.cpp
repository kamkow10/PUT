#include "Przeszkoda.h"

using namespace std;
using namespace sf;

Przeszkoda::Przeszkoda(float X, float Y, float x, float y, string plik)
{
	poz_x = X; poz_y = Y;
	roz_x = x; roz_y = y;
	tekstura.loadFromFile(plik, sf::IntRect(0, 0, x, y));
	tekstura.setSmooth(true);
	obraz.setTexture(tekstura);
	obraz.setPosition(X, Y);
}

void Przeszkoda::ruch()
{
	obraz.move(this->predkosc);
}

void Przeszkoda::nadaj_predkosc(float x)
{
	this->predkosc.x = -x;
}

void Przeszkoda::draw(RenderTarget & target, RenderStates states) const
{
	target.draw(this->obraz, states);
}

Vector2f Przeszkoda::pozycja()
{
	return obraz.getPosition();
}

void Przeszkoda::wroc()
{
	obraz.setPosition(poz_x, poz_y);
}

float Przeszkoda::gora()
{
	return obraz.getPosition().y;
}

float Przeszkoda::lewa()
{
	return obraz.getPosition().x;
}

float Przeszkoda::dol()
{
	return obraz.getPosition().y + roz_y;
}

float Przeszkoda::prawa()
{
	return obraz.getPosition().x + roz_x;
}

void Przeszkoda::ustaw(float x, float y)
{
	obraz.setPosition(x, y);
}