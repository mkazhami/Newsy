import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from contextlib import closing
from google_news import *
from reddit_api import *
import article_parse
from threading import Thread
import giphy_request
import nltk
nltk.download('punkt')

def summarize_urls(urls):
    summaries = []
    keywords = []
    titles = []
    giphy_urls = []

    remove_indices = []
    count = 0

    keywords = []

    for url in urls:
        count += 1
        text, title = article_parse.get_article_text(url)
        if len(text) < 250: # want the article to have substance..
            remove_indices.append(count - 1)
            continue
        summary_list = article_parse.get_summary(text)

        summary = ""
        for l in summary_list:
            summary += l + "\n"

        summaries.append(summary)
        titles.append(title)

        keys = article_parse.get_keywords(text)
        keys = sorted(keys, key=lambda x: x[1])
        keys = [key[0] for key in keys]
        giphy_urls.append(giphy_request.getGiphyURLFromKeywords(keys))
        keywords.append(keys)


        #print keywords[-len(keywords)*int(3/4):]

    for i in reversed(remove_indices):
        del urls[i]

    return [dict(title=titles[i], url=urls[i], text=summaries[i], keywords=keywords[i], giphy=giphy_urls[i]) for i in range(len(summaries))]


def populate_entries():
    entries = dict()
    entries['world'] = summarize_urls(get_subreddit_links('worldnews', 10)) + summarize_urls(get_subreddit_links('news', 10)) + summarize_urls(get_google_news_article_links('world'))
    entries['sports'] = summarize_urls(get_subreddit_links('sports', 10)) + summarize_urls(get_google_news_article_links('sports'))
    entries['health'] = summarize_urls(get_google_news_article_links('health'))
    entries['business'] = summarize_urls(get_subreddit_links('business', 10)) + summarize_urls(get_subreddit_links('economics', 10)) + summarize_urls(get_google_news_article_links('business'))
    entries['entertainment'] = summarize_urls(get_google_news_article_links('entertainment'))

    return entries

 
#entries = populate_entries()
#print(str(entries))

app = Flask(__name__)


@app.route('/')
def show_entries():
    return render_template('overview.html', sportsEntries=entries['sports'], businessEntries=entries['business'], \
                                            worldEntries=entries['world'], entertainmentEntries=entries['entertainment'], \
                                            healthEntries=entries['health'])


def refresh_task():
    while True:
        populate_entries()
        show_entries()
        time.sleep(60 * 60)


if __name__ == '__main__':
    t = Thread(target=refresh_task)
    t.start()
    app.run(host='127.0.0.1', port=5000)
