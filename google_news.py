import requests
import re
from BeautifulSoup import BeautifulSoup


urls = {
		"world": "https://news.google.ca/news/section?pz=1&ned=ca&topic=w&sdm=FADEOUT&authuser=0",
		"technology": "https://news.google.ca/news/section?pz=1&ned=ca&topic=tc&siidp=147b17973eac9b1fb7c4ab250af26df8f4f9&ict=ln&sdm=FADEOUT&authuser=0",
		"health": "https://news.google.ca/news/section?pz=1&ned=ca&topic=m&siidp=72fedde6129000ba76a23a3752eef46d579f&ict=ln&sdm=FADEOUT&authuser=0"
	  }

def get_google_news_article_links(topic):
	if topic not in urls:
		return

	r = requests.get(urls[topic])
	html = r.content

	parsed_html = BeautifulSoup(html)
	elements = parsed_html.body.findAll('a', attrs={'class':re.compile('article usg*'), 'target':'_blank'})
	links = set()
	for e in elements:
		links.add(e['href'])

	return list(links)
		