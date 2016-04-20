import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from contextlib import closing
import reddit_api, google_news
import article_parse

app = Flask(__name__)

DATABASE=os.path.join(app.root_path, 'newsy.db')
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'
app.config.from_object(__name__) # TODO: move to a separate file
#app.config.from_envvar('NEWSY_SETTINGS', silent=True)

entries = []

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
    
    populate_entries()

    # using the same list for each header for now
    return render_template('overview.html', sportsEntries=entries, businessEntries=entries, \
                                            politicsEntries=entries, entertainmentEntries=entries, \
                                            healthEntries=entries)

def add_entry():
    #g.db.execute('insert into entries (title, text) values (?, ?)',
    #           [request.form['title'], request.form['text']])
    #g.db.commit()
    #flash('New entry was successfully posted')
    #return redirect(url_for('show_entries'))
    flash("New entry added")


def populate_entries():
    urls = reddit_api.get_subreddit_links('worldnews', 5)
    urls += google_news.get_google_news_article_links('world')

    urls = urls[:20] # limit the number of links for testing
    # TODO: remove

    summaries = []

    remove_indices = []
    count = 0
    for url in urls:
        count += 1
        text = article_parse.get_article_text(url)
        if len(text) < 50:
            remove_indices.append(count - 1)
            continue
        summary_list = article_parse.get_summary(text)

        summary = ""
        for l in summary_list:
            summary += l + "\n"

        summaries.append(summary)

    for i in reversed(remove_indices):
        del urls[i]

    entries = [dict(title=urls[i], text=summaries[i]) for i in range(len(urls))]


if __name__ == '__main__':
    init_db()
    app.run(debug=True)