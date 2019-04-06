package VodPackage;

import java.io.Serializable;
import java.util.Random;

/**
 * Klasa reprezentująca datę
 * @author Kamil Kowalczyk
 */
public class Data implements Comparable<Data>, Serializable {

    private int dzien;
    private int miesiac;
    private int rok;

    /**
     *
     */
    public Data() {
        this(1980, 2018);
    }

    /**
     * Konstruktor stosowany, gdy chcemy by nasza data była z przedziału Od Do
     * @param Od rok od którego będziemy losować datę
     * @param Do rok do którego będziemy losować datę
     */
    public Data(int Od, int Do) {
        Random generator = new Random();
        this.rok = generator.nextInt(Do - Od) + Od;
        this.miesiac = generator.nextInt(12) + 1;
        if ((this.rok % 4 == 0) && (this.miesiac == 2)) {
            this.dzien = generator.nextInt(29) + 1;
        } else if (this.miesiac == 2) {
            this.dzien = generator.nextInt(28) + 1;
        } else if ((this.miesiac == 1)
                || (this.miesiac == 3)
                || (this.miesiac == 5)
                || (this.miesiac == 7)
                || (this.miesiac == 8)
                || (this.miesiac == 10)
                || (this.miesiac == 12)) {
            this.dzien = generator.nextInt(31) + 1;
        } else {
            this.dzien = generator.nextInt(31) + 1;
        }
    }

    /**
     *
     * @param dzien
     * @param miesiac
     * @param rok
     */
    public Data(int dzien, int miesiac, int rok) {
        this.dzien = dzien;
        this.miesiac = miesiac;
        this.rok = rok;
    }

    @Override
    public String toString() {
        String s = "";
        if (this.dzien < 10) {
            s += "0" + this.dzien + ".";
        } else {
            s += this.dzien + ".";
        }
        if (this.miesiac < 10) {
            s += "0" + this.miesiac + ".";
        } else {
            s += this.miesiac + ".";
        }
        s += this.rok;
        return s;
    }

    @Override
    public int compareTo(Data o) {
        if ((this.rok > o.rok)
                || ((this.rok == o.rok) && (this.miesiac > o.miesiac))
                || ((this.rok == o.rok) && (this.miesiac == o.miesiac) && (this.dzien > o.dzien))) {
            return 1;
        } else if ((this.rok == o.rok) && (this.miesiac == o.miesiac) && (this.dzien == o.dzien)) {
            return 0;
        } else {
            return -1;
        }
    }

    /**
     * Metoda inkrementująca datę
     */
    public void upload() {
        switch (this.miesiac) {
            case 2:
                switch (this.rok % 4) {
                    case 0:
                        switch (this.dzien) {
                            case 29:
                                this.dzien = 1;
                                this.miesiac = 3;
                                break;
                            default:
                                this.dzien++;
                                break;
                        }
                        break;
                    default:
                        switch (this.dzien) {
                            case 28:
                                this.dzien = 1;
                                this.miesiac = 3;
                                break;
                            default:
                                this.dzien++;
                                break;
                        }
                        break;
                }
                break;
            case 1:
            case 3:
            case 5:
            case 7:
            case 8:
            case 10:
            case 12:
                switch (this.dzien) {
                    case 31:
                        if (this.miesiac == 12) {
                            this.dzien = 1;
                            this.miesiac = 1;
                            this.rok++;
                        } else {
                            this.dzien = 1;
                            this.miesiac++;
                        }
                        break;
                    default:
                        this.dzien++;
                        break;
                }
                break;
            default:
                switch (this.dzien) {
                    case 30:
                        this.dzien = 1;
                        this.miesiac++;
                        break;
                    default:
                        this.dzien++;
                        break;
                }
                break;
        }
    }

    /**
     *
     * @param ileDni
     */
    public void upload(int ileDni) {
        for (int i = 0; i < ileDni; i++) {
            this.upload();
        }
    }

    /**
     *
     * @return
     */
    public int getDzien() {
        return dzien;
    }

    /**
     *
     * @param dzien
     */
    public void setDzien(int dzien) {
        this.dzien = dzien;
    }

    /**
     *
     * @return
     */
    public int getMiesiac() {
        return miesiac;
    }

    /**
     *
     * @param miesiac
     */
    public void setMiesiac(int miesiac) {
        this.miesiac = miesiac;
    }

    /**
     *
     * @return
     */
    public int getRok() {
        return rok;
    }

    /**
     *
     * @param rok
     */
    public void setRok(int rok) {
        this.rok = rok;
    }

}
