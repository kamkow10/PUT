package VodPackage;

import java.io.Serializable;
import java.util.Random;

/**
 * Klasa reprezentująca transmisje na żywo
 * @author Kamil Kowalczyk
 */
public class Live extends Produkt implements Serializable{

    private Promocja promocjaNaLive;

    /**
     *
     * @param dysProd
     */
    public Live(Dystrybutor dysProd) {
        super(dysProd);
        Data d = new Data(Main.OBECNA_DATA.getDzien(), Main.OBECNA_DATA.getMiesiac(), Main.OBECNA_DATA.getRok());
        Random generator = new Random();
        int zaIleDni = generator.nextInt(31) + 3;
        d.upload(zaIleDni);
        this.setDataProdukcji(d);
        this.promocjaNaLive = new Promocja();
    }

    @Override
    public String toString() {
        return super.toString()
                + this.promocjaNaLive.toString(this.getCena()) + "\n";
    }

    /**
     *
     * @return
     */
    public Promocja getPromocjaNaLive() {
        return promocjaNaLive;
    }

    /**
     *
     * @param promocjaNaLive
     */
    public void setPromocjaNaLive(Promocja promocjaNaLive) {
        this.promocjaNaLive = promocjaNaLive;
    }

}
