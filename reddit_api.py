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

g = Goose()

r = praw.Reddit(user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_client_secret)

def get_subreddit_link_summaries(subreddit, num_links=10):
	submissions = list(r.get_subreddit(subreddit).get_hot(limit=num_links))

	urls = [submission.url for submission in submissions]
	titles = [submission.title for submission in submissions]
	selftexts = [submission.selftext for submission in submissions]

	article_texts = []
	article_titles = []

	remove_urls = []
	count = 0
	for url in urls:
		count += 1
		try:
			selftext = selftexts[count-1]
			if len(selftext) > 50:
				#article_texts.append(selftext)
				continue
			text = g.extract(url=url).cleaned_text
			if len(text) < 50: # some arbitrary number, just want to eliminate failed extractions
				remove_urls.append(count - 1)
				continue
			article_texts.append(text)
		except Exception as e:
			print(str(e))
			raise e
			print("failed to extract from " + url)

	for i in reversed(remove_urls):
		del urls[i]

	summaries = []
	for text in article_texts:
		#parser = HtmlParser.from_url(url, Tokenizer("english"))
		parser = PlaintextParser.from_string(text, Tokenizer("english"))
		stemmer = Stemmer("english")

		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words("english")

		summary = ""
		for sentence in summarizer(parser.document, 10): # sentence count set to 10
			summary += str(sentence._text.encode('ascii', 'ignore'))

		summaries.append(summary)

		"""extractor = extract.TermExtractor()
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
		"""
	return urls, titles, summaries

