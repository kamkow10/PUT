import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.langdetect.Language;
import opennlp.tools.langdetect.LanguageDetectorME;
import opennlp.tools.langdetect.LanguageDetectorModel;
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
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

public class OpenNLP {

    public static String LANG_DETECT_MODEL = "models/langdetect-183.bin";
    public static String TOKENIZER_MODEL = "models/en-token.bin";
    public static String SENTENCE_MODEL = "models/en-sent.bin";
    public static String POS_MODEL = "models/en-pos-maxent.bin";
    public static String CHUNKER_MODEL = "models/en-chunker.bin";
    public static String LEMMATIZER_DICT = "models/en-lemmatizer.dict";
    public static String NAME_MODEL = "models/en-ner-person.bin";
    public static String ENTITY_XYZ_MODEL = "models/en-ner-xyz.bin";

	public static void main(String[] args) throws IOException
    {
		OpenNLP openNLP = new OpenNLP();
		openNLP.run();
	}

	public void run() throws IOException
    {

//		languageDetection();
//		 tokenization();
//         sentenceDetection();
//		 posTagging();
//		 lemmatization();
//		 stemming();
//		 chunking();
		 nameFinding();
	}

	private void languageDetection() throws IOException
    {
		File modelFile = new File(LANG_DETECT_MODEL);
		LanguageDetectorModel model = new LanguageDetectorModel(modelFile);

		LanguageDetectorME ldme = new LanguageDetectorME(model);


		String text = "";
//		text = "cats";

//		 text = "cats like milk";
		 text = "Many cats like milk because in some ways it reminds them of their mother's milk.";
//		 text = "The two things are not really related. Many cats like milk because in some ways it reminds them of their mother's milk.";
//		text = "The two things are not really related. Many cats like milk because in some ways it reminds them of their mother's milk. "
//				+ "It is rich in fat and protein. They like the taste. They like the consistency . "
//				+ "The issue as far as it being bad for them is the fact that cats often have difficulty digesting milk and so it may give them "
//				+ "digestive upset like diarrhea, bloating and gas. After all, cow's milk is meant for baby calves, not cats. "
//				+ "It is a fortunate quirk of nature that human digestive systems can also digest cow's milk. But humans and cats are not cows.";
//		 text = "Many cats like milk because in some ways it reminds them of their mother's milk. Le lait n'est pas forc�ment mauvais pour les chats";
//		 text = "Many cats like milk because in some ways it reminds them of their mother's milk. Le lait n'est pas forc�ment mauvais pour les chats. "
//		 + "Der Normalfall ist allerdings der, dass Salonl�wen Milch weder brauchen noch gut verdauen k�nnen.";

		Language lang = ldme.predictLanguage(text);
		Language[] langs = ldme.predictLanguages(text);

		for (Language l : langs) {
			System.out.println(l.getLang() + ", " + l.getConfidence());
		}
		System.out.println("-------------------------------------------");
		System.out.println(lang.getLang() + ", " + lang.getConfidence());

		/*
		* w przypadku dwóch języków prawdopodobieństwo eng znacząco wzrosło, pewnie dlatego że francuski i angielski są
		* z tej samej grupy języków i dodanie francuskiego tak na prawdę zwiększyło szansę na to, że może to być angielski
		*/
	}

	private void tokenization() throws IOException
    {
		String text = "";

//		text = "Since cats were venerated in ancient Egypt, they were commonly believed to have been domesticated there, "
//				+ "but there may have been instances of domestication as early as the Neolithic from around 9500 years ago (7500 BC).";
//		text = "Since cats were venerated in ancient Egypt, they were commonly believed to have been domesticated there, "
//				+ "but there may have been instances of domestication as early as the Neolithic from around 9,500 years ago (7,500 BC).";
		text = "Since cats were venerated in ancient Egypt, they were commonly believed to have been domesticated there, "
		 + "but there may have been instances of domestication as early as the Neolithic from around 9 500 years ago ( 7 500 BC).";

		// eng
		TokenizerModel tokenizerModel = new TokenizerModel(Paths.get("models/en-token.bin"));
		TokenizerME tokenizerME = new TokenizerME(tokenizerModel);
		ArrayList<String> words = new ArrayList<>(Arrays.asList(tokenizerME.tokenize(text)));
		ArrayList<Double> propabilities = new ArrayList<>();
		for (Double p : tokenizerME.getTokenProbabilities()) {
			propabilities.add(p);
		}
		// ger
		TokenizerModel tokenizerModel2 = new TokenizerModel(Paths.get("models/de-token.bin"));
		TokenizerME tokenizerME2 = new TokenizerME(tokenizerModel2);
		ArrayList<String> words2 = new ArrayList<>(Arrays.asList(tokenizerME2.tokenize(text)));
		ArrayList<Double> propabilities2 = new ArrayList<>();
		for (Double p : tokenizerME2.getTokenProbabilities()) {
			propabilities2.add(p);
		}
		// printing
		System.out.println("ENG =====================================");
		for (int i = 0; i < words.size(); i++) {
			System.out.println(words.get(i) + " : " + propabilities.get(i));
		}
		System.out.println("GER =====================================");
		for (int i = 0; i < words2.size(); i++) {
			System.out.println(words2.get(i) + " : " + propabilities2.get(i));
		}
		/*
		* (c) wyniki się różnią, przykładowo końcówka z "(7500 BC)." w każdym przypadku jest inaczej podzielona i ma inne
		* prawdopodobieństwa. To zrozumiałe, gdyż cięzko algorytowi wydobyć pojedyńczy token, gdy ta liczba jest przestawiona
		* jako "(7,500" a dużo łatwiej gdy zapiszemy ją jako "( 7 500"
		* (e) są różnice w jakości, de-token.bin radzi sobie o wiele lepiej - lepiej dzieli słowa i tokeny mają
		* wyższe prawdopodobieństwa
		* */
	}

	private void sentenceDetection() throws IOException
    {
		String text = "";
		text = "Hi. How are you? Welcome to Op?n methods for Natural Language Processing.";
//		text = "Hi. How are you?! Welcome to OpenNLP? "
//				+ "We provide multiple built-in methods for Natural Language Processing.";
//		text = "Hi. How are you? Welcome to OpenNLP.?? "
//				+ "We provide multiple . built-in methods for Natural Language Processing.";
		text = "The interrobang, also known????????? as the interabang!!!! (often represented by ?! or !?), "
				+ "is a nonstandard punctuation mark . used in various written languages. "
				+ "It is intended to combine the functions of the question mark (?), or interrogative point, "
				+ "and the exclamation ??? mark (!), or ? exclamation ! point, known in the jargon of printers and programmers as a \"bang\". ";

		SentenceModel sentenceModel = new SentenceModel(Paths.get("models/en-sent.bin"));
		SentenceDetectorME sentenceDetectorME = new SentenceDetectorME(sentenceModel);
		ArrayList<String> sentences = new ArrayList<>();
		Collections.addAll(sentences, sentenceDetectorME.sentDetect(text));
		ArrayList<Double> propabilities = new ArrayList<>();
		for ( Double p : sentenceDetectorME.getSentenceProbabilities()) {
			propabilities.add(p);
		}
		for (int i = 0; i < sentences.size(); i++) {
			System.out.println(sentences.get(i) + " : " + propabilities.get(i));
		}

		/*
		* algorytm jedynie nie radzi sobie z  znakami końca zdania tj. "!, ?, ."
		* w momencie gdy wstawimy je POJEDYŃCZO z dwoma spacjami po obydwu stronach np " . " - powoduje to
		* rozbicie zdania na dwie części
		* */
	}

	private void posTagging() throws IOException {
		String[] sentence = new String[0];
//		sentence = new String[] { "Cats", "like", "milk" };
		sentence = new String[]{"Cat", "is", "white", "like", "milk"};
//		sentence = new String[] { "Hi", "How", "are", "you", "Welcome", "to", "OpenNLP", "We", "provide", "multiple",
//				"built-in", "methods", "for", "Natural", "Language", "Processing" };
//		sentence = new String[] { "She", "put", "the", "big", "knives", "on", "the", "table" };

		POSModel posModel = new POSModel(Paths.get("models/en-pos-maxent.bin"));
		POSTaggerME posTaggerME = new POSTaggerME(posModel);
		int i = 0;
		for (String tag : posTaggerME.tag(sentence)) {
			System.out.println(sentence[i] + " : " + tag);
			i++;
		}

		/*
		* w pierwszym przypadku algorytm źle rozpoznał like jako IN co uzaje go za "jak" a nie za "lubić", w
		* drugim przypadku także like otrzymał tag IN, lecz tym razem jest to poprawny tag
		* */
	}

	private void lemmatization() throws IOException
    {
		String[] text = new String[0];
		text = new String[] { "Hi", "wegwhertwewe", "are", "you", "Welcome", "to", "OpenNLP", "We", "provide", "multiple",
				"built-in", "methods", "for", "Natural", "Language", "Processing" };
		String[] tags = new String[0];
		tags = new String[] { "NNP", "WRB", "VBP", "PRP", "VB", "TO", "VB", "PRP", "VB", "JJ", "JJ", "NNS", "IN", "JJ",
				"NN", "VBG" };

		DictionaryLemmatizer dictionaryLemmatizer = new DictionaryLemmatizer(Paths.get("models/en-lemmatizer.dict"));
		for (String s : dictionaryLemmatizer.lemmatize(text, tags)) {
			System.out.println(s);
		}


	}

	private void stemming()
    {
		System.out.println("================================================");
		String[] sentence = new String[0];
		sentence = new String[] { "Hi", "wegwhertwewe", "are", "you", "Welcome", "to", "OpenNLP", "We", "provide", "multiple",
				"built-in", "methods", "for", "Natural", "Language", "Processing" };

		PorterStemmer porterStemmer = new PorterStemmer();
		for (String s : sentence) {
			System.out.println(porterStemmer.stem(s));
		}

		/*
		* lemmatizer zamienił "are" w "be", zaś stemmer uciął "e" z końca i zostawił "ar"
		* ogólnie lemmatizer lepiej sobie radzi, ale wadą jest to, że potrzebuje on tagów
		* tagi potrzebne mu są do przykładowej zamiany "are" w "be", jest to zamiana innego typu, niż
		* ta w stemmerze, on jedynie ucina końcówki z wyrazów ("progresses" -> "progress(es)")
		*
		* w moim przypadku randomowe słowo "wegwhertwewe" skutkowało ucięciem "e" w stemmerze, a w
		* lemmatizerze zostało oznaczone jako "O" co, z tego co mi się wydaje, oznacza, że to słowo jest bazą
		* */
	}
	
	private void chunking() throws IOException
    {
		String[] sentence = new String[0];
		sentence = new String[] { "She", "put", "the", "big", "knives", "on", "the", "table" };

		String[] tags = new String[0];
		tags = new String[] { "PRP", "VBD", "DT", "JJ", "NNS", "IN", "DT", "NN" };

		ChunkerModel chunkerModel = new ChunkerModel(Paths.get("models/en-chunker.bin"));
		ChunkerME chunkerME = new ChunkerME(chunkerModel);

		int i = 0;
		for (String s : chunkerME.chunk(sentence, tags)) {
			System.out.println(sentence[i] + " " + s);
			i++;
		}

		/*
		* tagi są potrzebne gdyż chunker zajmuje się tylko lączeniem wyrazów w clustry, nie zajmuje się
		* rozpoznawaniem jakiego typu jest dany wyraz - taką informację musi otrzymać z zewenątrz
		*
		* B odziela nam chunki (dla n-tego wyrazu oznacza, że n-1 wyraz nie należy do tego samego chunku co n)
		* I i O oznacza kolejno że wyraz jest lub nie jest w chunku (analogicznie I oznacza zaprzeczenie B, czyli
		* n-1 należy do tego samego chunka co n)
		*
		* w mojej opini wynik jest poprawny
		* */

	}

	private void nameFinding() throws IOException
    {
		String text = "he idea of using computers to search for relevant pieces of information was popularized in the article "
				+ "As We May Think by Vannevar Bush in 1945. It would appear that Bush was inspired by patents "
				+ "for a 'statistical machine' - filed by Emanuel Goldberg in the 1920s and '30s - that searched for documents stored on film. "
				+ "The first description of a computer searching for information was described by Holmstrom in 1948, "
				+ "detailing an early mention of the Univac computer. Automated information retrieval systems were introduced in the 1950s: "
				+ "one even featured in the 1957 romantic comedy, Desk Set. In the 1960s, the first large information retrieval research group "
				+ "was formed by Gerard Salton at Cornell. By the 1970s several different retrieval techniques had been shown to perform "
				+ "well on small text corpora such as the Cranfield collection (several thousand documents). Large-scale retrieval systems, "
				+ "such as the Lockheed Dialog system, came into use early in the 1970s.";

//		TokenNameFinderModel tokenNameFinderModel = new TokenNameFinderModel(Paths.get("models/en-ner-person.bin"));
//		NameFinderME nameFinderME = new NameFinderME(tokenNameFinderModel);
//		Span[] spans = nameFinderME.find(text.split(" "));
//		String[] names = Span.spansToStrings(spans, text.split(" "));
//		for (int i = 0; i < spans.length; i++) {
//			System.out.println(names[i]);
//		}
		/*
		* nameFinder znajduje tylko niektóre osoby z tekstu
		* */

		TokenNameFinderModel tokenNameFinderModel = new TokenNameFinderModel(Paths.get("models/en-ner-xxx.bin"));
		NameFinderME nameFinderME = new NameFinderME(tokenNameFinderModel);
		Span[] spans = nameFinderME.find(text.split(" "));
		String[] names = Span.spansToStrings(spans, text.split(" "));
		for (int i = 0; i < spans.length; i++) {
			System.out.println(names[i]);
		}

		/*
		* XXX szuka dat
		* */

	}

}
