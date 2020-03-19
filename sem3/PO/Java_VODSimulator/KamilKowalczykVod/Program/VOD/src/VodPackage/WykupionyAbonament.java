package VodPackage;

import java.io.Serializable;

/**
 * Klasa reprezentuje abonament zakupiony przez użytkownika
 * @author Kamil Kowalczyk
 */
public class WykupionyAbonament implements Serializable{
    private Abonament abonament;
    private Data dataZaplaty;

    /**
     *
     * @param abonament
     * @param dataZaplaty
     */
    public WykupionyAbonament(Abonament abonament, Data dataZaplaty) {
        this.abonament = abonament;
        this.dataZaplaty = dataZaplaty;
    }

    /**
     *
     * @return
     */
    public Abonament getAbonament() {
        return abonament;
    }

    /**
     *
     * @param abonament
     */
    public void setAbonament(Abonament abonament) {
        this.abonament = abonament;
    }

    /**
     *
     * @return
     */
    public Data getDataZaplaty() {
        return dataZaplaty;
    }

    /**
     *
     * @param dataZaplaty
     */
    public void setDataZaplaty(Data dataZaplaty) {
        this.dataZaplaty = dataZaplaty;
    }
    
    
}
