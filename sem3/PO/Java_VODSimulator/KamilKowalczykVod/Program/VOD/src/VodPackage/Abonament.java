package VodPackage;

import java.io.Serializable;
import java.util.LinkedList;

/**
 * Klasa reprezentująca Abonament, który mogą zakupić użytkownicy
 * @author Kamil Kowalczyk
 */
public class Abonament implements Serializable {

    private String nazwa;
    private int cena;
    private int liczbaUrzadzen;
    private LinkedList<Produkt> pulaDostepnychProduktow;

    /**
     *
     * @param nazwa
     * @param cena
     * @param liczbaUrzadzen
     */
    public Abonament(String nazwa, int cena, int liczbaUrzadzen) {
        this.nazwa = nazwa;
        this.cena = cena;
        this.liczbaUrzadzen = liczbaUrzadzen;
        this.pulaDostepnychProduktow = new LinkedList<>();
    }

    @Override
    public String toString() {
        return "Typ abonamentu: " + this.nazwa + "\n"
                + "Miesięczna cena abonamentu: " + this.cena + "$\n"
                + "Ilość urządzeń: " + this.liczbaUrzadzen + "\n"
                + "Produkty objęte abonamentem: \n" + this.pulaDostepnychProduktowToString();
    }

    /**
     * Zamiana puli dostępnych produktów na String
     * @return 
     */
    public String pulaDostepnychProduktowToString() {
        String res = "";
        int i = 1;
        synchronized (this) {
            for (Produkt produkt : this.pulaDostepnychProduktow) {
                res += i++ + ". " + produkt.getNazwa() + " (" + produkt.getClass().getSimpleName() + ")\n";
            }
        }
        return res;
    }

    /**
     *
     * @return
     */
    public String getNazwa() {
        return nazwa;
    }

    /**
     *
     * @param nazwa
     */
    public void setNazwa(String nazwa) {
        this.nazwa = nazwa;
    }

    /**
     *
     * @return
     */
    public int getCena() {
        return cena;
    }

    /**
     *
     * @param cena
     */
    public void setCena(int cena) {
        this.cena = cena;
    }

    /**
     *
     * @return
     */
    public int getLiczbaUrzadzen() {
        return liczbaUrzadzen;
    }

    /**
     *
     * @param liczbaUrzadzen
     */
    public void setLiczbaUrzadzen(int liczbaUrzadzen) {
        this.liczbaUrzadzen = liczbaUrzadzen;
    }

    /**
     *
     * @return
     */
    public LinkedList<Produkt> getPulaDostepnychProduktow() {
        return pulaDostepnychProduktow;
    }

    /**
     *
     * @param pulaDostepnychProduktow
     */
    public void setPulaDostepnychProduktow(LinkedList<Produkt> pulaDostepnychProduktow) {
        this.pulaDostepnychProduktow = pulaDostepnychProduktow;
    }

}
