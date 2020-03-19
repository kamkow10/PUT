package VodPackage;

import java.io.Serializable;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Klasa reprezentująca uzytkownika
 * @author Kamil Kowalczyk
 */
public class Uzytkownik implements Runnable, Serializable {

    private String nazwa;
    private Data dataUrodzenia;
    private String email;
    private String nrKarty;
    private HashSet<Produkt> kupioneProdukty;
    private HashSet<Odcinek> kupioneOdcinki;
    private HashSet<WykupionyFilm> wykupioneFilmy;
    private WykupionyAbonament wykupionyAbonament;
    private transient Thread myThread;

    /**
     *
     */
    public Uzytkownik() {
        Random generator = new Random();
        this.nazwa = "";
        int dlugoscImienia = generator.nextInt(7) + 5;
        for (int i = 0; i < dlugoscImienia; i++) {
            if (i == 0) {
                this.nazwa += (char) (generator.nextInt(26) + 'A');
            } else {
                this.nazwa += (char) (generator.nextInt(26) + 'a');
            }
        }
        this.dataUrodzenia = new Data();
        this.email = this.nazwa + "@gmail.com";
        this.nrKarty = "";
        for (int i = 0; i < 7; i++) {
            if (i == 0) {
                this.nrKarty += generator.nextInt(10);
                this.nrKarty += generator.nextInt(10);
            } else {
                for (int j = 0; j < 4; j++) {
                    this.nrKarty += generator.nextInt(10);
                }
            }
            if (!(i == 6)) {
                this.nrKarty += " ";
            }
        }
        this.kupioneProdukty = new HashSet<>();
        this.kupioneOdcinki = new HashSet<>();
        this.wykupionyAbonament = null;
        this.wykupioneFilmy = new HashSet<>();
        this.myThread = new Thread(this);
    }

    @Override
    public String toString() {
        String abonament = "Brak";
        if (this.wykupionyAbonament != null) {
            abonament = this.wykupionyAbonament.getAbonament().getNazwa();
        }
        return "Nazwa: " + this.nazwa + "\n"
                + "Data urodzenia: " + this.dataUrodzenia.toString() + "\n"
                + "Numer karty kredytowej: " + this.nrKarty + "\n"
                + "E-mail: " + this.email + "\n"
                + "Wykupiony abonament: " + abonament + "\n"
                + "Wykupione produkty: " + "\n" + this.KupioneProduktyToString();
    }

    @Override
    public void run() {
        Random generator = new Random();
        try {
            while (true) {
                Main.threadSleep(generator.nextInt(10000) + 1000);
                synchronized (Main.DOSTEPNE_PRODUKTY) {
                    this.kupProdukt(Main.DOSTEPNE_PRODUKTY);
                }
                if ((this.wykupionyAbonament == null) && (generator.nextInt(3) == 0)) {
                    synchronized (Main.ABONAMENTY) {
                        this.kupAbonament();
                    }
                }
            }
        } catch (InterruptedException ex) {
            Logger.getLogger(Uzytkownik.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    /**
     * Metoda kupująca abonament
     */
    public void kupAbonament() {
        Random generator = new Random();
        int ktory = generator.nextInt(3);
        synchronized (Main.OBECNA_DATA) {
            this.wykupionyAbonament = new WykupionyAbonament(Main.ABONAMENTY.get(2),
                    new Data(Main.OBECNA_DATA.getDzien(), Main.OBECNA_DATA.getMiesiac(), Main.OBECNA_DATA.getRok()));
            this.wykupionyAbonament.getDataZaplaty().upload(30);
        }
        Main.PIENIADZE += Main.ABONAMENTY.get(2).getCena();
    }
    /**
     * Metoda kupująca produkt
     * @param dostepneProdukty
     */
    public void kupProdukt(LinkedList<Produkt> dostepneProdukty) {
        Random generator = new Random();
        Film f;
        Live l;
        Serial s;

        LinkedList<Produkt> llp = new LinkedList<>();
        WykupionyAbonament wa;
        if (this.wykupionyAbonament != null) {
            wa = this.wykupionyAbonament;
        } else {
            wa = new WykupionyAbonament(new Abonament("abonament", 0, 0), new Data());
        }

        llp.addAll(this.kupioneProdukty);
        llp.addAll(wa.getAbonament().getPulaDostepnychProduktow());
        LinkedList<Odcinek> dostepneOdcinki = new LinkedList<>();
        synchronized (Main.DOSTEPNE_PRODUKTY) {
            for (Produkt produkt : Main.DOSTEPNE_PRODUKTY) {
                if ((produkt.getClass() == Serial.class) && (!(wa.getAbonament().getPulaDostepnychProduktow().contains(produkt)))) {
                    Serial serial = (Serial) (produkt);
                    dostepneOdcinki.addAll(serial.getListaOdcinkow());
                }
            }
        }
        while (true) {
            if ((dostepneProdukty.isEmpty())
                    || ((llp.containsAll(dostepneProdukty))) && (this.kupioneOdcinki.containsAll(dostepneOdcinki))) {
                break;
            }
            int ind = generator.nextInt(dostepneProdukty.size());
            if ((!(wa.getAbonament().getPulaDostepnychProduktow().contains(dostepneProdukty.get(ind))))
                    && (!(this.kupioneProdukty.contains(dostepneProdukty.get(ind))))) {
                Main.wykupione++;
                this.kupioneProdukty.add(dostepneProdukty.get(ind));
                Produkt prod = Main.DOSTEPNE_PRODUKTY.get(ind);
                int i = prod.getDaneDoWykresu().getLast() + 1;
                prod.getDaneDoWykresu().set(prod.getDaneDoWykresu().size() - 1, i);
                if (prod.getClass() == Serial.class) {
                    s = (Serial) (prod);
                    Main.PIENIADZE += (s.getCena() * ((100 - s.getDystrybutorProduktu().getStawka()) / 100.0));
                    int ktoryOdcinek = generator.nextInt(s.getListaOdcinkow().size());
                    this.kupioneOdcinki.add((s.getListaOdcinkow().get(ktoryOdcinek)));
                } else if (prod.getClass() == Film.class) {
                    f = (Film) (prod);
                    synchronized (Main.OBECNA_DATA) {
                        this.wykupioneFilmy.add(new WykupionyFilm(f, new Data(f.getDataWaznosci().getDzien(), f.getDataWaznosci().getMiesiac(), f.getDataWaznosci().getRok())));
                    }
                    if (f.getPromocjaNaFilm().isAktywna()) {
                        Main.PIENIADZE += f.getCena() * ((100 - f.getPromocjaNaFilm().getUpust()) / 100.0);
                    } else {
                        Main.PIENIADZE += f.getCena();
                    }
                } else if (prod.getClass() == Live.class) {
                    l = (Live) (prod);
                    if (l.getPromocjaNaLive().isAktywna()) {
                        Main.PIENIADZE += l.getCena() * ((100 - l.getPromocjaNaLive().getUpust()) / 100);
                    } else {
                        Main.PIENIADZE += l.getCena();
                    }
                }
                break;
            } else if ((this.kupioneProdukty.contains(dostepneProdukty.get(ind))
                    && (dostepneProdukty.get(ind).getClass() == Serial.class))) {
                s = (Serial) (dostepneProdukty.get(ind));
                if (this.kupioneOdcinki.containsAll(s.getListaOdcinkow())) {
                    break;
                }
                for (int ktoryOdcinek = 0; ktoryOdcinek < s.getListaOdcinkow().size(); ktoryOdcinek++) {
                    if (!(this.kupioneOdcinki.contains(s.getListaOdcinkow().get(ktoryOdcinek)))) {
                        this.kupioneOdcinki.add((s.getListaOdcinkow().get(ktoryOdcinek)));
                        Main.PIENIADZE += s.getCena();
                        break;
                    }
                }
            }
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
    public Data getDataUrodzenia() {
        return dataUrodzenia;
    }

    /**
     *
     * @param dataUrodzenia
     */
    public void setDataUrodzenia(Data dataUrodzenia) {
        this.dataUrodzenia = dataUrodzenia;
    }

    /**
     *
     * @return
     */
    public String getEmail() {
        return email;
    }

    /**
     *
     * @param email
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     *
     * @return
     */
    public String getNrKarty() {
        return nrKarty;
    }

    /**
     *
     * @param nrKarty
     */
    public void setNrKarty(String nrKarty) {
        this.nrKarty = nrKarty;
    }

    /**
     *
     * @return
     */
    public HashSet<Produkt> getKupioneProdukty() {
        return kupioneProdukty;
    }

    /**
     *
     * @param kupioneProdukty
     */
    public void setKupioneProdukty(HashSet<Produkt> kupioneProdukty) {
        this.kupioneProdukty = kupioneProdukty;
    }

    /**
     *
     * @return
     */
    public WykupionyAbonament getWykupionyAbonament() {
        return wykupionyAbonament;
    }

    /**
     *
     * @param wykupionyAbonament
     */
    public void setWykupionyAbonament(WykupionyAbonament wykupionyAbonament) {
        this.wykupionyAbonament = wykupionyAbonament;
    }

    /**
     *
     * @return
     */
    public HashSet<Odcinek> getKupioneOdcinki() {
        return kupioneOdcinki;
    }

    /**
     *
     * @param kupioneOdcinki
     */
    public void setKupioneOdcinki(HashSet<Odcinek> kupioneOdcinki) {
        this.kupioneOdcinki = kupioneOdcinki;
    }

    /**
     *
     * @return
     */
    public HashSet<WykupionyFilm> getWykupioneFilmy() {
        return wykupioneFilmy;
    }

    /**
     *
     * @param wykupioneFilmy
     */
    public void setWykupioneFilmy(HashSet<WykupionyFilm> wykupioneFilmy) {
        this.wykupioneFilmy = wykupioneFilmy;
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
    
    /**
     * Metoda zamienia liste kupionych produktów na String
     * @return 
     */
    public String KupioneProduktyToString() {
        String res = "";
        Film f = null;
        Live l = null;
        Serial s = null;
        int iterator = 1;

        for (Produkt produkt : kupioneProdukty) {
            if (produkt.getClass() == Serial.class) {
                s = (Serial) (produkt);
                int ile = 0;
                for (Odcinek odcinek : s.getListaOdcinkow()) {
                    if (this.kupioneOdcinki.contains(odcinek)) {
                        ile++;
                    }
                }
                res += iterator + ". " + s.getNazwa()
                        + " (" + s.getClass().getSimpleName()
                        + "), ilość wykupionych odcinków: " + ile + "\n";

            } else if (produkt.getClass() == Film.class) {
                f = (Film) (produkt);
                WykupionyFilm wf = null;
                for (WykupionyFilm wykupionyFilm : wykupioneFilmy) {
                    if (wykupionyFilm.getFilm() == f) {
                        wf = wykupionyFilm;
                        break;
                    }
                }
                res += iterator + ". " + f.getNazwa()
                        + " (" + f.getClass().getSimpleName() + "), "
                        + "Data waznosci: " + wf.getDataWaznosci().toString() + "\n";

            } else if (produkt.getClass() == Live.class) {
                l = (Live) (produkt);
                res += iterator + ". " + l.getNazwa()
                        + " (" + l.getClass().getSimpleName() + "), "
                        + "Data transmisji: " + l.getDataProdukcji().toString() + "\n";
            }
            iterator++;
        }
        return res;
    }

}
