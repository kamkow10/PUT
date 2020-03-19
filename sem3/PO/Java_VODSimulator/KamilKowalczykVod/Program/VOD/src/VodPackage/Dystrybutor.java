package VodPackage;

import java.io.Serializable;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Klasa reprezentująca dystrybutora
 * @author Kamil Kowalczyk
 */
public class Dystrybutor implements Runnable, Serializable {

    private String nazwa;
    private LinkedList<Produkt> dodaneProdukty;
    private transient Thread myThread;
    /**
     * Nalezny % dochodów z produktów tego dystrybutora
     */
    private int stawka;

    /**
     *
     */
    public Dystrybutor() {
        Random generator = new Random();
        this.stawka = generator.nextInt(21) + 10;
        char[] c = {(char) (generator.nextInt(26) + 'A'), (char) (generator.nextInt(26) + 'A'), (char) (generator.nextInt(26) + 'A')};
        this.nazwa = Character.toString(c[0]) + Character.toString(c[1]) + Character.toString(c[2]);
        this.dodaneProdukty = new LinkedList<>();
        this.myThread = new Thread(this);
    }

    @Override
    public void run() {
        Random generator = new Random();
        try {
            while (true) {
                Main.threadSleep(generator.nextInt(1000) + 5000);
                synchronized (Main.DOSTEPNE_PRODUKTY) {
                    this.addProdukt();
                }
                synchronized (this) {
                    this.renegocjujUmowe();
                }
            }
        } catch (InterruptedException ex) {
            Logger.getLogger(Dystrybutor.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    @Override
    public String toString() {
        String products = "";
        int i = 1;
        for (Produkt produkt : this.dodaneProdukty) {
            products += i + ". " + produkt.getNazwa() + " (" + produkt.getClass().getSimpleName() + ")\n";
            i++;
        }
        return "Nazwa: " + this.nazwa + "\n"
                + "Stawka: " + this.stawka + "%\n"
                + "Wypuszczone produkty: \n" + products;

    }

    /**
     * Dodanie produktu do systemu
     */
    public void addProdukt() {
        Random generator = new Random();
        Produkt p;
        int los = generator.nextInt(5) + 1;
        if (los == 1) {
            p = new Live(this);
        } else if ((los == 2) || (los == 3)) {
            p = new Serial(this);
            synchronized (Main.ABONAMENTY) {
                Main.ABONAMENTY.get(2).getPulaDostepnychProduktow().add(p);
                if ((generator.nextInt(15) + 1) != 5) {
                    Main.ABONAMENTY.get(0).getPulaDostepnychProduktow().add(p);
                    Main.ABONAMENTY.get(1).getPulaDostepnychProduktow().add(p);
                }
            }
        } else {
            p = new Film(this);
            synchronized (Main.ABONAMENTY) {
                Main.ABONAMENTY.get(2).getPulaDostepnychProduktow().add(p);
                if ((generator.nextInt(5) + 1) != 5) {
                    Main.ABONAMENTY.get(0).getPulaDostepnychProduktow().add(p);
                    Main.ABONAMENTY.get(1).getPulaDostepnychProduktow().add(p);
                }
            }
        }
        Main.DOSTEPNE_PRODUKTY.add(p);
        this.dodaneProdukty.add(p);
    }

    /**
     * Renegocjacja umowy
     */
    private void renegocjujUmowe() {
        Random generator = new Random();
        if ((generator.nextInt(15) == 0) && (this.stawka < 50)) {
            this.stawka++;
        }
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
    public LinkedList<Produkt> getDodaneProdukty() {
        return dodaneProdukty;
    }

    /**
     *
     * @param dodaneProdukty
     */
    public void setDodaneProdukty(LinkedList<Produkt> dodaneProdukty) {
        this.dodaneProdukty = dodaneProdukty;
    }

    /**
     *
     * @return
     */
    public int getStawka() {
        return stawka;
    }

    /**
     *
     * @param stawka
     */
    public void setStawka(int stawka) {
        this.stawka = stawka;
    }

    /**
     *
     * @return
     */
    public Thread getMyThread() {
        return myThread;
    }

    /**
     *
     * @param myThread
     */
    public void setMyThread(Thread myThread) {
        this.myThread = myThread;
    }

}
