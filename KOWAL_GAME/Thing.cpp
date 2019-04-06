#include "Thing.h"

using namespace std;
using namespace sf;

Thing::Thing(float X, float Y, string plik)
{
	tekstura.loadFromFile(plik, sf::IntRect(0, 0, X, Y));
	tekstura.setSmooth(true);
	obraz.setTexture(tekstura);
}
