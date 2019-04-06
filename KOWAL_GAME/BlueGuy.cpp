#include "BlueGuy.h"


using namespace std;
using namespace sf;

BlueGuy::BlueGuy(string plik, float grav)
{
	file = plik;
	tekstura.loadFromFile(plik, sf::IntRect(0, 0, roz_x, roz_y));
	tekstura.setSmooth(true);
	obraz.setTexture(tekstura);
	obraz.setPosition(poz_x, poz_y);
	frame = 1;
	grawitacja = { 0, (float)(grav) };
	sila_wyskoku = { 0,0 };
	czas_zmiany_klatki = 0.1;
}

void BlueGuy::draw(RenderTarget & target, RenderStates states) const
{
	target.draw(this->obraz, states);
}

void BlueGuy::animacja(Clock & time)
{
	if (time.getElapsedTime().asSeconds() > czas_zmiany_klatki)
	{
		tekstura.loadFromFile(file, sf::IntRect(frame * roz_x, 0, roz_x, roz_y));
		obraz.setTexture(tekstura);
		time.restart();
		frame++;
		if (frame > 3)
			frame = 1;
	}
}

void BlueGuy::skok()
{
	sila_wyskoku += grawitacja;
	obraz.move(sila_wyskoku);
	tekstura.loadFromFile(file, sf::IntRect(0, 0, roz_x, roz_y));
	obraz.setTexture(tekstura);
}

void BlueGuy::wroc()
{
	obraz.setPosition(poz_x, poz_y);
}

float BlueGuy::dol()
{
	return obraz.getPosition().y + roz_y;
}

float BlueGuy::prawa()
{
	return obraz.getPosition().x + roz_x;
}

float BlueGuy::gora()
{
	return obraz.getPosition().y;
}

float BlueGuy::lewa()
{
	return obraz.getPosition().x;
}

void BlueGuy::przyspiesz(double x)
{
	czas_zmiany_klatki /= x;
}

void BlueGuy::przywroc_predkosc()
{
	czas_zmiany_klatki = 0.1;
}
