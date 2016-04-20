import requests
import re
from BeautifulSoup import BeautifulSoup


urls = {
		"world": "https://news.google.ca/news/section?pz=1&ned=ca&topic=w&sdm=FADEOUT&authuser=0",
		"sports": "https://news.google.ca/news/section?pz=1&ned=ca&topic=s&siidp=af036f5dbb6bd3716aa019c399ee5711594b&ict=ln&sdm=FADEOUT&authuser=0",
		"technology": "https://news.google.ca/news/section?pz=1&ned=ca&topic=tc&siidp=147b17973eac9b1fb7c4ab250af26df8f4f9&ict=ln&sdm=FADEOUT&authuser=0",
		"health": "https://news.google.ca/news/section?pz=1&ned=ca&topic=m&siidp=72fedde6129000ba76a23a3752eef46d579f&ict=ln&sdm=FADEOUT&authuser=0",
		"business": "https://news.google.ca/news/section?pz=1&ned=ca&topic=b&siidp=1ee907582e879fafa64a6a668ab2bb1d56eb&ict=ln&sdm=FADEOUT&authuser=0",
		"entertainment": "https://news.google.ca/news/section?pz=1&ned=ca&topic=e&siidp=18bc1fa6ded74ed7c1dff6a446e26b2b7305&ict=ln&sdm=FADEOUT&authuser=0",
		"science": "https://news.google.ca/news/section?pz=1&ned=ca&topic=snc&siidp=d3187357ea7719a3b82da49f2fe63ca0e003&ict=ln&sdm=FADEOUT&authuser=0"
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
		