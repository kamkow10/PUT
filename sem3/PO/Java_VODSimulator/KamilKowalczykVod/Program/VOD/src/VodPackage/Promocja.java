package VodPackage;

import java.io.Serializable;
import java.util.Random;

/**
 * Klasa reprezentująca promocję
 * @author Kamil Kowalczyk
 */
public class Promocja implements Serializable{

    private Data dataRozpoczecia;
    private Data dataZakonczenia;
    /**
     * * Procentowy upust (5-50%)
     */
    private int upust;
    private boolean aktywna;

    /**
     *
     */
    public Promocja() {
        Random generator = new Random();
        this.aktywna = generator.nextBoolean();
        this.dataRozpoczecia = new Data(Main.OBECNA_DATA.getDzien(), Main.OBECNA_DATA.getMiesiac(), Main.OBECNA_DATA.getRok());
        this.dataZakonczenia = new Data(Main.OBECNA_DATA.getDzien(), Main.OBECNA_DATA.getMiesiac(), Main.OBECNA_DATA.getRok());
        int dlugoscPromocji = generator.nextInt(31) + 3;
        this.dataZakonczenia.upload(dlugoscPromocji);
        this.upust = generator.nextInt(46) + 5;
    }

    /**
     *
     * @param cena
     * @return
     */
    public String toString(int cena) {
        String promo;
        if (this.isAktywna()) {
            promo = "PROMOCJA: Kup teraz, a zaplacisz " + String.format("%.2f", cena * ((100 - this.getUpust()) / 100.0)) + "$ (-" + this.getUpust() + "%) !!!" + "\n"
                    + "Waznosc promocji: od " + this.getDataRozpoczecia() + " do " + this.getDataZakonczenia();
        } else {
            promo = "Cena: " + cena + "$";
        }
        return promo;
    }

    /**
     *
     * @return
     */
    public Data getDataRozpoczecia() {
        return dataRozpoczecia;
    }

    /**
     *
     * @param dataRozpoczecia
     */
    public void setDataRozpoczecia(Data dataRozpoczecia) {
        this.dataRozpoczecia = dataRozpoczecia;
    }

    /**
     *
     * @return
     */
    public Data getDataZakonczenia() {
        return dataZakonczenia;
    }

    /**
     *
     * @param dataZakonczenia
     */
    public void setDataZakonczenia(Data dataZakonczenia) {
        this.dataZakonczenia = dataZakonczenia;
    }

    /**
     *
     * @return
     */
    public int getUpust() {
        return upust;
    }

    /**
     *
     * @param upust
     */
    public void setUpust(int upust) {
        this.upust = upust;
    }

    /**
     *
     * @return
     */
    public boolean isAktywna() {
        return aktywna;
    }

    /**
     *
     * @param aktywna
     */
    public void setAktywna(boolean aktywna) {
        this.aktywna = aktywna;
    }

}
