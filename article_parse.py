from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from topia.termextract import extract
from difflib import SequenceMatcher

from goose import Goose

from word_comparison import *

g = Goose()

def get_article_text(url):
	try:
		extracted = g.extract(url=url)
		return extracted.cleaned_text, extracted.title
	except Exception as e:
		print(str(e))
		print("failed to extract from " + url)

	return "", ""

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

	resultList = resultList[-10:]	

	#def similar(a, b):
	#    return SequenceMatcher(None, a, b).ratio()	

	removeList = []

	for result in resultList:
		if word_importance(result[0]) == 0:
			removeList.append(result)

	for word in removeList:
		resultList.remove(word)

	removeList = []

	for s1 in resultList:
		if s1 in removeList:
			continue

		for s2 in resultList:
			if s2 in removeList:
				continue

			if s1[0] != s2[0] and compare_words(s1[0], s2[0]) >= 0.9:
				importance1 = word_importance(s1[0])
				importance2 = word_importance(s2[0])
				if importance1 == importance2:
					if len(s1[0]) > len(s2[0]):
						removeList.append(s2)
					else:
						removeList.append(s1)
				elif importance1 > importance2:
					removeList.append(s2)
				else:
					removeList.append(s1)

	return resultList




