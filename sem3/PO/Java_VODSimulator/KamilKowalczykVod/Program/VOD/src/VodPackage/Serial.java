package VodPackage;

import java.io.Serializable;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Random;

/**
 * Klasa reprezentująca serial
 * @author Kamil Kowalczyk
 */
public class Serial extends Produkt implements Serializable{
    private String gatunek;
    private HashSet<String> listaAktorow;
    private int sezony;
    private LinkedList<Odcinek> listaOdcinkow;

    /**
     *
     * @param dysProd
     */
    public Serial(Dystrybutor dysProd) {
        super(dysProd);
        Random generator = new Random();
        String[] gatunki = {"Sensacyjny", "Dramat", "Komedia", "Dla dzieci", "Dokumentalny", "Akcja"};
        String[] imiona = {"John", "Michael", "Adam", "Robert", "Emanuel", "Olivier", "Jessica", "Eddie", "Sammon", "Dennis", "Kobe", "Tomek", "Grzegorz", "Alicja", "Karolina", "Eugeniusz"};
        String[] nazwiska = {"Depp", "Pitt", "Kolonko", "Snow", "Leszczyk", "Jackson", "Mercury", "Bird", "Walles", "Brzezyszczykiewicz", "Zidan", "Travollta", "Esperado", "Blue", "Wall", "Sienkiewicz"};

        this.gatunek = gatunki[generator.nextInt(gatunki.length)];
        int ile = generator.nextInt(7) + 1;
        this.listaAktorow = new HashSet<>();
        for (int i = 0; i < ile; i++) {
            this.listaAktorow.add(imiona[generator.nextInt(imiona.length)] + " " + nazwiska[generator.nextInt(nazwiska.length)]);
        }
        this.sezony = generator.nextInt(5) + 1;
        this.listaOdcinkow = new LinkedList<>();
        ile = generator.nextInt(5) + 4;
        Data dataOdc = this.getDataProdukcji();
        int dlugosc = ((generator.nextInt(5) + 1) * 10);
        for (int i = 0; i < sezony; i++) {
            for (int j = 0; j < ile; j++) {
                Odcinek odc = new Odcinek(dataOdc,dlugosc + generator.nextInt(10));
                this.listaOdcinkow.add(odc);
            }
        }
    }
    
    @Override
    public String toString() {
        return super.toString() + 
                "Gatunek: " + this.gatunek + "\n" +
                "Aktorzy: " + this.getListaAktorow() + "\n" +
                "Sezony: " + this.sezony + "\n" +
                "Cena za jeden odcinek: " + this.getCena() + "$ \n" +
                "Lista odcinkow: " + "\n" + this.listaOdcinkowToString() + "\n";
    }

    /**
     *
     * @return
     */
    public String getGatunek() {
        return gatunek;
    }

    /**
     *
     * @param gatunek
     */
    public void setGatunek(String gatunek) {
        this.gatunek = gatunek;
    }

    /**
     *
     * @return
     */
    public String getListaAktorow() {
        String re = "";
        for (String string : this.listaAktorow) {
            re += string + ", ";
        }
        return re.substring(0, re.length()-2);
    }

    /**
     *
     * @param listaAktorow
     */
    public void setListaAktorow(HashSet<String> listaAktorow) {
        this.listaAktorow = listaAktorow;
    }

    /**
     *
     * @return
     */
    public int getSezony() {
        return sezony;
    }

    /**
     *
     * @param sezony
     */
    public void setSezony(int sezony) {
        this.sezony = sezony;
    }

    /**
     *
     * @return
     */
    public String listaOdcinkowToString() {
        String re = "";
        int S=1, E=1;
        String Se = "", Ep = "";
        for (Odcinek odc : this.listaOdcinkow) {
            if (S < 10) Se = "0" + S;
            else        Se = "" + S;
            if (E < 10) Ep = "0" + E;
            else        Ep = "" + E;
            re += "S" + Se + "E" + Ep + ": Data premiery: " + odc.getDataPremiery().toString() + ", dlugosc: " + odc.getDlugosc() + " min \n";
            E++;
            if (E > this.listaOdcinkow.size()/this.sezony) {
                E = 1;
                S++;
            }
        }
        return re;
    }

    /**
     *
     * @return
     */
    public LinkedList<Odcinek> getListaOdcinkow() {
        return listaOdcinkow;
    }
    
    /**
     *
     * @param listaOdcinkow
     */
    public void setListaOdcinkow(LinkedList<Odcinek> listaOdcinkow) {
        this.listaOdcinkow = listaOdcinkow;
    }
    
}
