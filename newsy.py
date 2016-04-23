import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from contextlib import closing
from google_news import *
from reddit_api import *
import article_parse


def summarize_urls(urls):
    summaries = []
    titles = []
    remove_indices = []
    count = 0

    urls = urls[:5] #artificially limited TODO: remove

    for url in urls:
        count += 1
        text, title = article_parse.get_article_text(url)
        if len(text) < 50:
            remove_indices.append(count - 1)
            continue
        summary_list = article_parse.get_summary(text)

        summary = ""
        for l in summary_list:
            summary += l + "\n"

        summaries.append(summary)
        titles.append(title)

    for i in reversed(remove_indices):
        del urls[i]

    return [dict(title=titles[i], url=urls[i], text=summaries[i]) for i in range(len(summaries))]


def populate_entries():
    entries = dict()
    entries['world'] = summarize_urls(get_subreddit_links('worldnews', 5)) + summarize_urls(get_google_news_article_links('world'))
    entries['sports'] = summarize_urls(get_google_news_article_links('sports'))
    entries['health'] = summarize_urls(get_google_news_article_links('health'))
    entries['business'] = summarize_urls(get_google_news_article_links('business'))
    entries['entertainment'] = summarize_urls(get_google_news_article_links('entertainment'))

    return entries

 
entries = populate_entries()
print(str(entries))

app = Flask(__name__)

DATABASE=os.path.join(app.root_path, 'newsy.db')
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'
app.config.from_object(__name__) # TODO: move to a separate file
#app.config.from_envvar('NEWSY_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    #rv = sqlite3.connect(app.config['DATABASE'])
    #rv.row_factory = sqlite3.Row
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initializes the database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]

    # using the same list for each header for now
    return render_template('overview.html', sportsEntries=entries['sports'], businessEntries=entries['business'], \
                                            worldEntries=entries['world'], entertainmentEntries=entries['entertainment'], \
                                            healthEntries=entries['health'])





if __name__ == '__main__':
    #init_db()
    app.run(debug=True)