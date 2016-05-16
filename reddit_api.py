import praw
import article_parse
#from secret import reddit_user_agent, reddit_client_id, reddit_client_secret
import os

reddit_user_agent = os.environ["reddit_user_agent"]
reddit_client_id = os.environ["reddit_client_id"]
reddit_client_secret = os.environ["reddit_client_secret"]

r = praw.Reddit(user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_client_secret)

def get_subreddit_links(subreddit, num_links=10):
	submissions = list(r.get_subreddit(subreddit).get_hot(limit=num_links))

	urls = [submission.url for submission in submissions]
	titles = [submission.title for submission in submissions]
	selftexts = [submission.selftext for submission in submissions]

	"""
	summaries = []
	article_titles = []

	remove_urls = []
	count = 0
	for url in urls:
		count += 1
		selftext = selftexts[count-1]
		if len(selftext) > 50:
			continue
		text = article_parse.get_article_text(url)
		if len(text) < 50: # some arbitrary number, just want to eliminate failed extractions
			remove_urls.append(count - 1)
			continue
		#article_titles.append(titles[count-1])
		#summaries.append(article_parse.get_summary(text))

	for i in reversed(remove_urls):
		del urls[i]
	"""
	return urls
