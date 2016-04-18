from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from topia.termextract import extract
from difflib import SequenceMatcher

from goose import Goose

g = Goose()

def get_article_text(url):
	try:
		return g.extract(url=url).cleaned_text
	except Exception as e:
		print(str(e))
		raise e
		print("failed to extract from " + url)

	return ""

def get_summary(text, max_sentences=5):
	parser = PlaintextParser.from_string(text, Tokenizer("english"))
	stemmer = Stemmer("english")

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words("english")

	summary = []
	for sentence in summarizer(parser.document, max_sentences): # sentence count set to 10
		summary.append(str(sentence._text.encode('ascii', 'ignore')))

	return summary

def get_keywords(text):
	extractor = extract.TermExtractor()
	result = sorted(extractor(text), key=lambda x: x[1])
	resultList = []
	for line in result:
		if len(line[0]) > 4:
			resultList.append(line)	

	resultList = resultList[len(resultList) - 10:]	

	def similar(a, b):
	    return SequenceMatcher(None, a, b).ratio()	


	for s1 in resultList:
		for s2 in resultList:
			if s1[0] != s2[0] and similar(s1[0], s2[0]) > 0.7:
				resultList.remove(s2)

	for result in resultList:
		print(result)




