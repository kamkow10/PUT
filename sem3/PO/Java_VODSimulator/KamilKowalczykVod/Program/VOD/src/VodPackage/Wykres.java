package VodPackage;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import javax.swing.JFrame;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.JFreeChart;
import org.jfree.data.time.Day;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.data.xy.XYDataset;

/**
 * Klasa reprezentująca wykres zakupów produktu w czasie
 * @author Kamil Kowalczyk
 */
public class Wykres extends JFrame {

    /**
     *
     * @param applicationTitle
     * @param chartTitle
     * @param p
     */
    public Wykres(String applicationTitle, String chartTitle, Produkt p) {
        super(applicationTitle);
        JFreeChart lineChart = ChartFactory.createTimeSeriesChart(chartTitle, "Dni", "Ilość zakupów", createDataset(p), true, true, false);
        ChartPanel chartPanel = new ChartPanel(lineChart);

        JFrame f = new JFrame(applicationTitle);
        f.setTitle(chartTitle);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        f.setLayout(new BorderLayout(0, 5));
        f.add(chartPanel, BorderLayout.CENTER);
        chartPanel.setMouseWheelEnabled(true);
        chartPanel.setHorizontalAxisTrace(true);
        chartPanel.setVerticalAxisTrace(true);

        f.pack();
        f.setLocationRelativeTo(null);
        f.setVisible(true);
    }
    
    /**
     * Metoda tworzaca dane do wykresu
     * @param p produkt dla którego będzie tworzony wykres
     * @return gotowe dane
     */
    private XYDataset createDataset(Produkt p) {

        TimeSeries series = new TimeSeries("Data");
        TimeSeriesCollection dataset = new TimeSeriesCollection();
        
        Data data = new Data(p.getDataPojawieniaSie().getDzien(),
                p.getDataPojawieniaSie().getMiesiac(),
                p.getDataPojawieniaSie().getRok());
        for (Integer wartosc : p.getDaneDoWykresu()) {
            series.add(new Day(data.getDzien(), data.getMiesiac(), data.getRok()), wartosc);
            data.upload();
        }
        
        dataset.addSeries(series);
        return dataset;
    }

    /**
     *
     * @param p
     */
    public static void create(Produkt p) {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                Wykres cpd = new Wykres("Wykres", "Zakupy w czasie", p);
            }
        });
    }
}
