package VodPackage;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;

/**
 * Klasa reprezentująca film
 * @author Kamil Kowalczyk
 */
public class Film extends Produkt implements Serializable{

    private String gatunek;
    private HashSet<String> listaAktorow;
    private HashSet<String> linkiDoZwiastunow;
    private Data dataWaznosci;
    private Promocja promocjaNaFilm;

    /**
     *
     * @param dysProd
     */
    public Film(Dystrybutor dysProd) {
        super(dysProd);
        Random generator = new Random();
        String[] gatunki = {"Sensacyjny", "Dramat", "Komedia", "Dla dzieci", "Dokumentalny", "Akcja"};
        String[] imiona = {"John", "Michael", "Adam", "Robert", "Emanuel", "Olivier", "Jessica", "Eddie", "Sammon", "Dennis", "Kobe", "Tomek", "Grzegorz", "Alicja", "Karolina", "Eugeniusz"};
        String[] nazwiska = {"Depp", "Pitt", "Kolonko", "Snow", "Leszczyk", "Jackson", "Mercury", "Bird", "Walles", "Brzezyszczykiewicz", "Zidan", "Travollta", "Esperado", "Blue", "Wall", "Sienkiewicz"};
        String[][] linki = {{"1link1", "1link2", "1link3"}, {"2link1", "2link2", "2link3"}, {"3link1", "3link2", "3link3"}};

        this.gatunek = gatunki[generator.nextInt(gatunki.length)];
        int ile = generator.nextInt(7) + 1;
        this.listaAktorow = new HashSet<>();
        for (int i = 0; i < ile; i++) {
            this.listaAktorow.add(imiona[generator.nextInt(imiona.length)] + " " + nazwiska[generator.nextInt(nazwiska.length)]);
        }
        int los = generator.nextInt(linki.length);
        this.linkiDoZwiastunow = new HashSet<>();
        this.linkiDoZwiastunow.addAll(Arrays.asList(linki[los]));
        int dniWaznosci = generator.nextInt(30) + 1;
        this.dataWaznosci = new Data(Main.OBECNA_DATA.getDzien(), Main.OBECNA_DATA.getMiesiac(), Main.OBECNA_DATA.getRok());
        this.dataWaznosci.upload(dniWaznosci);
        this.promocjaNaFilm = new Promocja();
    }

    @Override
    public String toString() {
        return super.toString()
                + "Gatunek: " + this.gatunek + "\n"
                + "Aktorzy: " + this.getListaAktorow() + "\n"
                + "Linki do zwiastunow: " + this.getLinkiDoZwiastunow() + "\n"
                + "Data waznosci: " + this.dataWaznosci.toString() + "\n"
                + this.promocjaNaFilm.toString(this.getCena()) + "\n";
    }

    /**
     *
     * @return
     */
    public String getGarunek() {
        return gatunek;
    }

    /**
     *
     * @param garunek
     */
    public void setGarunek(String garunek) {
        this.gatunek = garunek;
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
        return re.substring(0, re.length() - 2);
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
    public String getLinkiDoZwiastunow() {
        String re = "";
        for (String string : this.linkiDoZwiastunow) {
            re += string + ", ";
        }
        return re.substring(0, re.length() - 2);
    }

    /**
     *
     * @param linkiDoZwiastunow
     */
    public void setLinkiDoZwiastunow(HashSet<String> linkiDoZwiastunow) {
        this.linkiDoZwiastunow = linkiDoZwiastunow;
    }

    /**
     *
     * @return
     */
    public Data getDataWaznosci() {
        return dataWaznosci;
    }

    /**
     *
     * @param dataWaznosci
     */
    public void setDataWaznosci(Data dataWaznosci) {
        this.dataWaznosci = dataWaznosci;
    }

    /**
     *
     * @return
     */
    public Promocja getPromocjaNaFilm() {
        return promocjaNaFilm;
    }

    /**
     *
     * @param promocjaNaFilm
     */
    public void setPromocjaNaFilm(Promocja promocjaNaFilm) {
        this.promocjaNaFilm = promocjaNaFilm;
    }

}
