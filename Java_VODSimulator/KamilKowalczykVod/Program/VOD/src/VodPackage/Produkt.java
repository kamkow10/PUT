package VodPackage;

import java.io.Serializable;
import java.util.*;

/**
 * Klasa reprezentująca produkt
 * @author Kamil Kowalczyk
 */
public abstract class Produkt implements Serializable{

    private String nazwa;
    private String opis;
    private Data dataProdukcji;
    private int czasTrwania;
    private Dystrybutor dystrybutorProduktu;
    private HashSet<String> krajeProdukcji;
    private double ocenaUzytkownikow;
    private int cena;
    private Data dataPojawieniaSie;
    private LinkedList<Integer> daneDoWykresu;

    /**
     *
     * @param dysProd
     */
    public Produkt(Dystrybutor dysProd) {
        String[] przymiotniki = {"Red", "Blue", "Yellow", "Green", "Black", "Strong", "Amazing", "Funny", "Long", "Our", "Short", "Next", "Beautiful", "Bloody", "Scary", "Sad", "Lovely", "Lonely"};
        String[] rzeczowniki = {"Army", "Collage", "Dog", "War", "God", "Movie", "Film", "Star", "Prison", "Break", "Cat", "Friend", "Color", "Show", "Battle", "Lake", "Animals", "Dragon", "Warrior", "Game", "Adventure"};
        String[] opisy = {
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
            "In German-occupied Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazi Germans.",
            "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
            "A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery",
            "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
            "In the slums of Rio, two kids' paths diverge as one struggles to become a photographer and the other a kingpin.",
            "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."};
        String[] kraje = {"Poland", "England", "USA", "China", "Japan", "Norway", "Germany", "Italy", "Ireland", "France", "Denmark", "Austria"};

        Random generator = new Random();
        this.nazwa = przymiotniki[generator.nextInt(przymiotniki.length)] + " " + rzeczowniki[generator.nextInt(rzeczowniki.length)];
        this.opis = opisy[generator.nextInt(opisy.length)];
        this.dataProdukcji = new Data();
        this.czasTrwania = generator.nextInt(150) + 20;
        this.dystrybutorProduktu = dysProd;

        int iloscKrajow = generator.nextInt(3) + 1;
        this.krajeProdukcji = new HashSet();
        for (int i = 0; i < iloscKrajow; i++) {
            this.krajeProdukcji.add(kraje[generator.nextInt(12)]);
        }
        this.ocenaUzytkownikow = generator.nextFloat() * 10;
        this.cena = generator.nextInt(5) + 1;
        this.dataPojawieniaSie
                = new Data(Main.OBECNA_DATA.getDzien(),
                        Main.OBECNA_DATA.getMiesiac(),
                        Main.OBECNA_DATA.getRok());
        this.daneDoWykresu = new LinkedList<>();
        this.daneDoWykresu.add(0);
    }

    @Override
    public String toString() {
        return "Nazwa: " + this.nazwa + "\n"
                + "Opis: " + this.opis + "\n"
                + "Data produkcji: " + this.dataProdukcji.toString() + "\n"
                + "Data pojawienia sie: " + this.dataPojawieniaSie.toString() + "\n"
                + "Czas trwania: " + this.czasTrwania + " min\n"
                + "Dystrybutor: " + this.dystrybutorProduktu.getNazwa() + "\n"
                + "Kraje produkcji: " + this.getKrajeProdukcji() + "\n"
                + "Ocena uzytkownikow: " + String.format("%.2f", this.ocenaUzytkownikow) + "\n";
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
    public String getOpis() {
        return opis;
    }

    /**
     *
     * @param opis
     */
    public void setOpis(String opis) {
        this.opis = opis;
    }

    /**
     *
     * @return
     */
    public Data getDataProdukcji() {
        return dataProdukcji;
    }

    /**
     *
     * @param dataProdukcji
     */
    public void setDataProdukcji(Data dataProdukcji) {
        this.dataProdukcji = dataProdukcji;
    }

    /**
     *
     * @return
     */
    public int getCzasTrwania() {
        return czasTrwania;
    }

    /**
     *
     * @param czasTrwania
     */
    public void setCzasTrwania(int czasTrwania) {
        this.czasTrwania = czasTrwania;
    }

    /**
     *
     * @return
     */
    public Dystrybutor getDystrybutorProduktu() {
        return dystrybutorProduktu;
    }

    /**
     *
     * @param dystrybutorProduktu
     */
    public void setDystrybutorProduktu(Dystrybutor dystrybutorProduktu) {
        this.dystrybutorProduktu = dystrybutorProduktu;
    }

    /**
     *
     * @return
     */
    public String getKrajeProdukcji() {
        String re = "";
        for (String string : this.krajeProdukcji) {
            re += string + ", ";
        }
        return re.substring(0, re.length() - 2);
    }

    /**
     *
     * @param krajeProdukcji
     */
    public void setKrajeProdukcji(HashSet<String> krajeProdukcji) {
        this.krajeProdukcji = krajeProdukcji;
    }

    /**
     *
     * @return
     */
    public double getOcenaUzytkownikow() {
        return ocenaUzytkownikow;
    }

    /**
     *
     * @param ocenaUzytkownikow
     */
    public void setOcenaUzytkownikow(double ocenaUzytkownikow) {
        this.ocenaUzytkownikow = ocenaUzytkownikow;
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
    public Data getDataPojawieniaSie() {
        return dataPojawieniaSie;
    }

    /**
     *
     * @param dataPojawieniaSie
     */
    public void setDataPojawieniaSie(Data dataPojawieniaSie) {
        this.dataPojawieniaSie = dataPojawieniaSie;
    }

    /**
     *
     * @return
     */
    public LinkedList<Integer> getDaneDoWykresu() {
        return daneDoWykresu;
    }

    /**
     *
     * @param daneDoWykresu
     */
    public void setDaneDoWykresu(LinkedList<Integer> daneDoWykresu) {
        this.daneDoWykresu = daneDoWykresu;
    }

}
