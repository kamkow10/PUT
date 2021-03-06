import opennlp.tools.lemmatizer.DictionaryLemmatizer;
import opennlp.tools.namefind.NameFinderME;
import opennlp.tools.namefind.TokenNameFinderModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.stemmer.PorterStemmer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.util.Span;

import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;


public class MovieReviewStatictics
{
    private static final String DOCUMENTS_PATH = "movies/";
    private int _verbCount = 0;
    private int _nounCount = 0;
    private int _adjectiveCount = 0;
    private int _adverbCount = 0;
    private int _totalTokensCount = 0;

    private PrintStream _statisticsWriter;

    private SentenceModel _sentenceModel;
    private TokenizerModel _tokenizerModel;
    private DictionaryLemmatizer _lemmatizer;
    private PorterStemmer _stemmer;
    private POSModel _posModel;
    private TokenNameFinderModel _peopleModel;
    private TokenNameFinderModel _placesModel;
    private TokenNameFinderModel _organizationsModel;

    public static void main(String[] args)
    {
        MovieReviewStatictics statictics = new MovieReviewStatictics();
        statictics.run();
    }

    private void run()
    {
        try
        {
            initModelsStemmerLemmatizer();

            File dir = new File(DOCUMENTS_PATH);
            File[] reviews = dir.listFiles((d, name) -> name.endsWith(".txt"));

            _statisticsWriter = new PrintStream("statistics.txt", "UTF-8");

            Arrays.sort(reviews, Comparator.comparing(File::getName));
            for (File file : reviews)
            {
                System.out.println("Movie: " + file.getName().replace(".txt", ""));
                _statisticsWriter.println("Movie: " + file.getName().replace(".txt", ""));

                String text = new String(Files.readAllBytes(file.toPath()));
                processFile(text);

                _statisticsWriter.println();
            }

            overallStatistics();
            _statisticsWriter.close();

        } catch (IOException ex)
        {
            Logger.getLogger(MovieReviewStatictics.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void initModelsStemmerLemmatizer()
    {
        try {
            _sentenceModel = new SentenceModel(Paths.get("models/en-sent.bin"));
            _peopleModel = new TokenNameFinderModel(Paths.get("models/en-ner-person.bin"));
            _organizationsModel = new TokenNameFinderModel(Paths.get("models/en-ner-organization.bin"));
            _placesModel = new TokenNameFinderModel(Paths.get("models/en-ner-location.bin"));
            _lemmatizer = new DictionaryLemmatizer(Paths.get("models/en-lemmatizer.dict"));
            _stemmer = new PorterStemmer();
            _posModel = new POSModel(Paths.get("models/en-pos-maxent.bin"));
            _tokenizerModel = new TokenizerModel(Paths.get("models/en-token.bin"));
        } catch (IOException ex) {
            Logger.getLogger(MovieReviewStatictics.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void processFile(String text)
    {
        // TODO: process the text to find the following statistics:
        // For each movie derive:
        //    - number of sentences
        //    - number of tokens
        //    - number of (unique) stemmed forms

        //    - number of (unique) words from a dictionary (lemmatization)
        //    -  people
        //    - locations
        //    - organisations

        // TODO + compute the following overall (for all movies) POS tagging statistics:
        //    - percentage number of adverbs (class variable, private int _verbCount = 0)
        //    - percentage number of adjectives (class variable, private int _nounCount = 0)
        //    - percentage number of verbs (class variable, private int _adjectiveCount = 0)
        //    - percentage number of nouns (class variable, private int _adverbCount = 0)
        //    + update _totalTokensCount




        // ------------------------------------------------------------------

        // TODO derive sentences (update noSentences variable)
        SentenceDetectorME sentenceDetectorME = new SentenceDetectorME(_sentenceModel);
        int noSentences = sentenceDetectorME.sentDetect(text).length;

        // TODO derive tokens and POS tags from text
        TokenizerME tokenizerME = new TokenizerME(_tokenizerModel);
        String[] tokens = tokenizerME.tokenize(text);
        int noTokens = tokens.length;

        POSTaggerME posTaggerME = new POSTaggerME(_posModel);
        String[] tags = posTaggerME.tag(tokens);

        // TODO perform stemming (use derived tokens)
        Set<String> uniqueForms = new HashSet<>();
        for (String s : tokens) {
            s = s.toLowerCase().replaceAll("[^a-z0-9]", "");
            if (!s.isEmpty())
                uniqueForms.add(_stemmer.stem(s));
        }
        int noStemmed = uniqueForms.size();


        // TODO perform lemmatization (use derived tokens)
        Set<String> uniqueForms2 = new HashSet<>();
        Collections.addAll(uniqueForms2, _lemmatizer.lemmatize(tokens, tags));
        int noWords = uniqueForms2.size();


        // TODO derive people, locations, organisations (use tokens),
        NameFinderME nameFinderME = new NameFinderME(_peopleModel);
        Span people[] = nameFinderME.find(tokens);
        NameFinderME nameFinderME2 = new NameFinderME(_placesModel);
        Span locations[] = nameFinderME2.find(tokens);
        NameFinderME nameFinderME3 = new NameFinderME(_organizationsModel);
        Span organisations[] = nameFinderME3.find(tokens);

        // TODO update overall statistics - use tags and check first letters
        for (String tag : tags) {
            if (tag.charAt(0) == 'V')
                _verbCount++;
            else if (tag.charAt(0) == 'R')
                _adverbCount++;
            else if (tag.charAt(0) == 'N')
                _nounCount++;
            else if (tag.charAt(0) == 'J')
                _adjectiveCount++;
        }
        _totalTokensCount += tokens.length;

        // ------------------------------------------------------------------

        saveResults("Sentences", noSentences);
        saveResults("Tokens", noTokens);
        saveResults("Stemmed forms (unique)", noStemmed);
        saveResults("Words from a dictionary (unique)", noWords);

        saveNamedEntities("People", people, tokens);
        saveNamedEntities("Locations", locations, tokens);
        saveNamedEntities("Organizations", organisations, tokens);
    }


    private void saveResults(String feature, int count)
    {
        String s = feature + ": " + count;
        System.out.println("   " + s);
        _statisticsWriter.println(s);
    }

    private void saveNamedEntities(String entityType, Span spans[], String tokens[])
    {
        StringBuilder s = new StringBuilder(entityType + ": ");
        for (int sp = 0; sp < spans.length; sp++)
        {
            for (int i = spans[sp].getStart(); i < spans[sp].getEnd(); i++)
            {
                s.append(tokens[i]);
                if (i < spans[sp].getEnd() - 1) s.append(" ");
            }
            if (sp < spans.length - 1) s.append(", ");
        }

        System.out.println("   " + s);
        _statisticsWriter.println(s);
    }

    private void overallStatistics()
    {
        _statisticsWriter.println("---------OVERALL STATISTICS----------");
        DecimalFormat f = new DecimalFormat("#0.00");

        if (_totalTokensCount == 0) _totalTokensCount = 1;
        String verbs = f.format(((double) _verbCount * 100) / _totalTokensCount);
        String nouns = f.format(((double) _nounCount * 100) / _totalTokensCount);
        String adjectives = f.format(((double) _adjectiveCount * 100) / _totalTokensCount);
        String adverbs = f.format(((double) _adverbCount * 100) / _totalTokensCount);

        _statisticsWriter.println("Verbs: " + verbs + "%");
        _statisticsWriter.println("Nouns: " + nouns + "%");
        _statisticsWriter.println("Adjectives: " + adjectives + "%");
        _statisticsWriter.println("Adverbs: " + adverbs + "%");

        System.out.println("---------OVERALL STATISTICS----------");
        System.out.println("Adverbs: " + adverbs + "%");
        System.out.println("Adjectives: " + adjectives + "%");
        System.out.println("Verbs: " + verbs + "%");
        System.out.println("Nouns: " + nouns + "%");
    }

}
