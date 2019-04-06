package VodPackage;

import java.io.Serializable;

/**
 * Klasa reprezentująca odcinek serialu
 * @author Kamil Kowalczyk
 */
public class Odcinek implements Serializable{
    private Data dataPremiery;
    private int dlugosc;

    /**
     *
     * @param dataPremiery
     * @param dlugosc
     */
    public Odcinek(Data dataPremiery, int dlugosc) {
        this.dataPremiery = dataPremiery;
        this.dlugosc = dlugosc;
    }
    
    /**
     *
     * @return
     */
    public Data getDataPremiery() {
        return dataPremiery;
    }

    /**
     *
     * @param dataPremiery
     */
    public void setDataPremiery(Data dataPremiery) {
        this.dataPremiery = dataPremiery;
    }

    /**
     *
     * @return
     */
    public int getDlugosc() {
        return dlugosc;
    }

    /**
     *
     * @param dlugosc
     */
    public void setDlugosc(int dlugosc) {
        this.dlugosc = dlugosc;
    }
    
}
