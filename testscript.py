import praw
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from topia.termextract import extract
from difflib import SequenceMatcher

from goose import Goose

from secret import reddit_user_agent, reddit_client_id, reddit_client_secret

print("\n\n")

g = Goose()

r = praw.Reddit(user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_client_secret)
submissions = r.get_subreddit('worldnews').get_hot(limit=3)

urls = [submission.url for submission in submissions]

article_texts = []
article_titles = []
for url in urls:
	try:
		article_texts.append(g.extract(url=url).cleaned_text)
	except:
		print("failed to extract from " + url)

for text in article_texts:
	#parser = HtmlParser.from_url(url, Tokenizer("english"))
	parser = PlaintextParser.from_string(text, Tokenizer("english"))
	stemmer = Stemmer("english")

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words("english")

	for sentence in summarizer(parser.document, 10): # sentence count set to 10
		print(sentence)

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


