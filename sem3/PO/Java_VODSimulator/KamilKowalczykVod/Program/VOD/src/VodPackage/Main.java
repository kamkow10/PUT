package VodPackage;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;

/**
 * Główna klasa Main
 * @author Kamil Kowalczyk
 */
public class Main {
    /**
     * Aktualna ilość pieniędzy
     */
    public static float PIENIADZE = 0;
    /**
     * Lista dostępnych produktów w systemie
     */
    public static final LinkedList<Produkt> DOSTEPNE_PRODUKTY = new LinkedList<>();
    /**
     * Liczba wykupionych dotychczas produktów
     */
    public static int wykupione = 0;
    /**
     * Obecna data
     */
    public static Data OBECNA_DATA = new Data(1, 1, 2019);
    /**
     * Lista użytkowników
     */
    public static LinkedList<Uzytkownik> UZYTKOWNICY = new LinkedList<>();
    /**
     * Lista dystrybutorów
     */
    public static LinkedList<Dystrybutor> DYSTRYBUTORZY = new LinkedList<>();
    /**
     * Dystrybutor uzytkownik. Jest to domyślny dystrybutor przy tworzeniu produktów w panule kontrolnym.
     */
    public static Dystrybutor USER = new Dystrybutor();
    /**
     * Lista dostępnych w systemie abonamentów
     */
    public static ArrayList<Abonament> ABONAMENTY = new ArrayList<>();
    /**
     * GUI Swing - środowisko multimedialne
     */
    public static SymulatorVOD vodFrame = new SymulatorVOD();
    /**
     * Wątek aktualizujący datę po upływie okreslonego czasu
     */
    public static Thread czasThread = new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                try {
                    Main.threadSleep(5000);
                    synchronized (Main.OBECNA_DATA) {
                        Main.OBECNA_DATA.upload();
                    }
                    synchronized (Main.zmianaDaty) {
                        Main.zmianaDaty = true;
                    }
                } catch (InterruptedException ex) {
                    Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
    });
    /**
     * Czy OBECNA_DATA została zmieniona przez czasThread
     */
    public static Boolean zmianaDaty = false;
    /**
     * Jeżeli ustawione na TRUE - Pauza jest aktywna
     */
    public static Boolean PAUZA = false;
    /**
     * Miesięczna opłata za utrzymanie systemu
     */
    public static Integer MIESIECZNA_OPLATA = 0;
    /**
     * Lista gormadzaca informacje o tym czy kolejne miesiące były stratne
     */
    public static LinkedList<Boolean> STRATY = new LinkedList<>();
    /**
     * Wątek reagujący w momencie zmiany daty. Posiada wiele funkcji:
     * - Spłata należności po upływie miesiąca
     * - Usuwanie livewów które już się odbyły
     * - Usuwanie promocji których termin się skończył
     * - Pobieranie opłat od użytkowników za abonament
     * - Aktualizowanie dat ważności filmów
     * - Usuwanie filmów po upływie daty ważnoścu z kont uzytkowników
     */
    public static Thread kontrolaZmianyDniaThread = new Thread(new Runnable() {
        @Override
        public void run() {
            while (true) {
                try {
                    Thread.sleep(100);
                    if (Main.zmianaDaty) {
                        // Spłata należności po upływie miesiąca
                        synchronized (Main.OBECNA_DATA) {
                            if (Main.OBECNA_DATA.getDzien() == 1) {
                                JOptionPane.showMessageDialog(null,
                                        "Opłata miesięczna:\n"
                                        + Main.PIENIADZEtoString(Main.PIENIADZE) + " - " + Main.PIENIADZEtoString(Main.MIESIECZNA_OPLATA)
                                        + " = " + Main.PIENIADZEtoString(Main.PIENIADZE - Main.MIESIECZNA_OPLATA));
                                synchronized (Main.MIESIECZNA_OPLATA) {
                                    Main.PIENIADZE -= Main.MIESIECZNA_OPLATA;
                                }
                                if (Main.PIENIADZE < 0) {
                                    Main.STRATY.add(true);
                                } else {
                                    Main.STRATY.add(false);
                                }
                                if (Main.STRATY.size() >= 3) {
                                    if (Main.STRATY.get(Main.STRATY.size() - 1)
                                            && Main.STRATY.get(Main.STRATY.size() - 2)
                                            && Main.STRATY.get(Main.STRATY.size() - 3)) {
                                        JOptionPane.showMessageDialog(null, 
                                                "Symulacja generowała 3 miesiące z rzedu straty, więc się kończy :(");
                                        System.exit(0);
                                    }
                                }
                            }
                        }
                        // Usuwanie livewów które już się odbyły
                        Live l = null;
                        synchronized (Main.DOSTEPNE_PRODUKTY) {
                            for (Produkt produkt : Main.DOSTEPNE_PRODUKTY) {
                                produkt.getDaneDoWykresu().add(0);
                            }
                        }
                        LinkedList<Produkt> llp = new LinkedList<>();
                        synchronized (Main.DOSTEPNE_PRODUKTY) {
                            for (Produkt produkt : Main.DOSTEPNE_PRODUKTY) {
                                if (produkt.getClass() == Live.class) {
                                    l = (Live) (produkt);
                                    if (l.getDataProdukcji().compareTo(OBECNA_DATA) == -1) {
                                        llp.add(produkt);
                                    }
                                }
                            }
                        }
                        for (Produkt produkt : llp) {
                            synchronized (Main.DOSTEPNE_PRODUKTY) {
                                Main.DOSTEPNE_PRODUKTY.remove(produkt);
                            }
                            synchronized (Main.UZYTKOWNICY) {
                                for (Uzytkownik uzytkownik : Main.UZYTKOWNICY) {
                                    if (uzytkownik.getKupioneProdukty().contains(produkt)) {
                                        uzytkownik.getKupioneProdukty().remove(produkt);
                                    }
                                }
                            }
                            synchronized (Main.DYSTRYBUTORZY) {
                                for (Dystrybutor dystrybutor : Main.DYSTRYBUTORZY) {
                                    if (dystrybutor.getDodaneProdukty().contains(produkt)) {
                                        dystrybutor.getDodaneProdukty().remove(produkt);
                                    }
                                }
                            }
                            synchronized (Main.UZYTKOWNICY) {
                                for (Uzytkownik uzytkownik : Main.UZYTKOWNICY) {
                                    if (uzytkownik.getKupioneProdukty().contains(produkt)) {
                                        uzytkownik.getKupioneProdukty().remove(produkt);
                                    }
                                }
                            }
                            produkt = null;
                        }

                        // Usuwanie promocji których termin się skończył
                        synchronized (Main.DOSTEPNE_PRODUKTY) {
                            Film film;
                            Live live;
                            for (Produkt produkt : Main.DOSTEPNE_PRODUKTY) {
                                synchronized (produkt) {
                                    if (produkt.getClass() == Film.class) {
                                        film = (Film) (produkt);
                                        if (film.getPromocjaNaFilm().getDataZakonczenia().compareTo(Main.OBECNA_DATA) == -1) {
                                            film.getPromocjaNaFilm().setAktywna(false);
                                        }
                                    }
                                    if (produkt.getClass() == Live.class) {
                                        live = (Live) (produkt);
                                        if (live.getPromocjaNaLive().getDataZakonczenia().compareTo(Main.OBECNA_DATA) == -1) {
                                            live.getPromocjaNaLive().setAktywna(false);
                                        }
                                    }
                                }
                            }
                        }

                        // Pobieranie opłat od użytkowników za abonament
                        synchronized (Main.UZYTKOWNICY) {
                            for (Uzytkownik uzytkownik : Main.UZYTKOWNICY) {
                                if (uzytkownik.getWykupionyAbonament() != null) {
                                    if (uzytkownik.getWykupionyAbonament().getDataZaplaty().compareTo(Main.OBECNA_DATA) == 0) {
                                        Main.PIENIADZE += uzytkownik.getWykupionyAbonament().getAbonament().getCena();
                                        uzytkownik.getWykupionyAbonament().getDataZaplaty().upload(30);
                                    }
                                }
                            }
                        }

                        // Aktualizowanie dat ważności filmów
                        Film f = null;
                        synchronized (Main.DOSTEPNE_PRODUKTY) {
                            for (Produkt produkt : Main.DOSTEPNE_PRODUKTY) {
                                if (produkt.getClass() == Film.class) {
                                    f = (Film) (produkt);
                                    f.getDataWaznosci().upload();
                                }
                            }
                        }

                        // Usuwanie filmów po upływie daty ważnoścu z kont uzytkowników
                        LinkedList<WykupionyFilm> llp2 = new LinkedList<>();
                        synchronized (Main.UZYTKOWNICY) {
                            for (Uzytkownik uzytkownik : Main.UZYTKOWNICY) {
                                synchronized (uzytkownik) {
                                    for (WykupionyFilm wykupionyFilm : uzytkownik.getWykupioneFilmy()) {
                                        if (wykupionyFilm.getDataWaznosci().compareTo(Main.OBECNA_DATA) == -1) {
                                            llp2.add(wykupionyFilm);
                                        }
                                    }
                                }
                            }
                        }
                        for (WykupionyFilm wykupionyFilm : llp2) {
                            synchronized (Main.UZYTKOWNICY) {
                                for (Uzytkownik uzytkownik : Main.UZYTKOWNICY) {
                                    if (uzytkownik.getWykupioneFilmy().contains(wykupionyFilm)) {
                                        synchronized (uzytkownik.getKupioneProdukty()) {
                                            uzytkownik.getKupioneProdukty().remove(wykupionyFilm.getFilm());
                                        }
                                        synchronized (uzytkownik.getWykupioneFilmy()) {
                                            uzytkownik.getWykupioneFilmy().remove(wykupionyFilm);
                                        }
                                        Main.wykupione--;
                                    }
                                }
                            }
                        }
                        synchronized (Main.zmianaDaty) {
                            Main.zmianaDaty = false;
                        }
                    }
                } catch (InterruptedException ex) {
                    Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }

    });
    /**
     * Formatuje liczbę do formatu String w formie pieniężnej
     * @param x liczba
     * @return String w formie pieniężnej
     */
    public static String PIENIADZEtoString(float x) {
        return String.format("%.2f", x);
    }
    /**
     * Formatuje liczbę do formatu String w formie pieniężnej
     * @param x liczba
     * @return String w formie pieniężnej
     */
    public static String PIENIADZEtoString(int x) {
        return String.format("%.2f", (float) x);
    }
    /**
     * Tworzy nowego użytkownika
     */
    public static void newUzytkownik() {
        Uzytkownik u1 = new Uzytkownik();
        synchronized (Main.UZYTKOWNICY) {
            Main.UZYTKOWNICY.add(u1);
        }
        u1.getMyThread().start();
    }
    /**
     * Tworzy nowego dystrybutora
     */
    public static void newDystrybutor() {
        Dystrybutor d1 = new Dystrybutor();

        synchronized (Main.DYSTRYBUTORZY) {
            Main.DYSTRYBUTORZY.add(d1);
        }
        d1.getMyThread().start();
    }
    /**
     * Metoda sleep z uwzględnieniem czekania na zwolnienie pauzy
     * @param milisekundy długość czekania w milisek.
     * @throws java.lang.InterruptedException
     */
    public static void threadSleep(int milisekundy) throws InterruptedException {
        for (int i = 0; i < milisekundy / 100; i++) {
            Thread.sleep(100);
            while (Main.PAUZA) {
                Thread.sleep(10);
            }
        }
    }
    
    /**
     * Główna funkcja programu
     * @param args
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        Main.vodFrame.main();
        Main.vodFrame.setVisible(true);
    }
}
