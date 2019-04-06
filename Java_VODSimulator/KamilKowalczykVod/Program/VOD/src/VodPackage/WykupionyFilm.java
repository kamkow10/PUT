package VodPackage;

import java.io.Serializable;

/**
 * Klasa reprezentuje wykupiony przez uzytkownika film
 * @author Kamil Kowalczyk
 */
public class WykupionyFilm implements Serializable {
    private Film film;
    private Data dataWaznosci;

    /**
     *
     * @param film
     * @param dataWykupienia
     */
    public WykupionyFilm(Film film, Data dataWykupienia) {
        this.film = film;
        this.dataWaznosci = dataWykupienia;
    }

    /**
     *
     * @return
     */
    public Film getFilm() {
        return film;
    }

    /**
     *
     * @param film
     */
    public void setFilm(Film film) {
        this.film = film;
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
    
}
