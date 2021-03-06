import os, sys, logging, time, threading
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from contextlib import closing
from google_news import *
from reddit_api import *
import article_parse, giphy_request
import nltk
nltk.download('punkt')


entries = { 'sports': [], 'business': [], 'world': [], 'entertainment': [], 'health': [] } # start with empty dictionary
lock = threading.Lock() # lock for entries dictionary

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

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
        summary_list = article_parse.get_summary(text) # returns a list of sentences

        summary = ""
        for l in summary_list:
            summary += l + "\n"

        summaries.append(summary)
        titles.append(title)

        # get most prominent keywords
        keys = article_parse.get_keywords(text)
        keys = sorted(keys, key=lambda x: x[1])
        keys = [key[0] for key in keys]

        # get most relevant giphy (gif)
        # not always relevant, but funny when not relevant
        giphy_urls.append(giphy_request.getGiphyURLFromKeywords(keys))

        keywords.append(keys)

    # remove info from bad links
    for i in reversed(remove_indices):
        del urls[i]

    return [dict(title=titles[i], url=urls[i], text=summaries[i], keywords=keywords[i], giphy=giphy_urls[i]) for i in range(len(summaries))]


def populate_entries():
    global entries

    temp = dict()
    temp['world'] = summarize_urls(get_subreddit_links('worldnews', 10)) + summarize_urls(get_subreddit_links('news', 10)) + summarize_urls(get_google_news_article_links('world'))
    temp['sports'] = summarize_urls(get_subreddit_links('sports', 10)) + summarize_urls(get_google_news_article_links('sports'))
    temp['health'] = summarize_urls(get_google_news_article_links('health'))
    temp['business'] = summarize_urls(get_subreddit_links('business', 10)) + summarize_urls(get_subreddit_links('economics', 10)) + summarize_urls(get_google_news_article_links('business'))
    temp['entertainment'] = summarize_urls(get_google_news_article_links('entertainment'))

    lock.acquire()
    entries = temp
    lock.release()

    return entries



@app.route('/')
def show_entries():
    lock.acquire()
    isPopulated = True
    for entry in entries:
        if len(entry) == 0:
            isPopulated = False
            break

    if isPopulated:
        retval = render_template('overview.html', sportsEntries=entries['sports'], businessEntries=entries['business'], \
                                                  worldEntries=entries['world'], entertainmentEntries=entries['entertainment'], \
                                                  healthEntries=entries['health'])
        lock.release()
        return retval
    else:
        lock.release()
        return render_template('overview.html')


def refresh_task():
    global entries
    while True:
        entries = populate_entries()
        while len(entries) == 0:
            time.sleep(5)
            entries = populate_entries()
        time.sleep(60 * 60)

# run thread in background to update the links every hour
t = threading.Thread(target=refresh_task)

if __name__ == '__main__':
    t.start()
    app.run(debug=False, host='0.0.0.0', port=os.environ.get("PORT", 5000))
