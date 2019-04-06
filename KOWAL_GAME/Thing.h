#pragma once
#include <SFML/Graphics.hpp>

using namespace std;
using namespace sf;

class Thing
{
private:
	Texture tekstura;
	Sprite obraz;
	float x, y; // rozmiar obiektu
public:
	Thing()=delete;
	~Thing()=default;
	Thing(float X, float Y, string plik);


};

