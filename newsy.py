import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from contextlib import closing


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
        # test values
        db.execute('insert into entries (title, text) values (?, ?)', \
                    ["basketball", "lebron"])
        db.execute('insert into entries (title, text) values (?, ?)', \
                    ["basketball", "kobe"])
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
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
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



if __name__ == '__main__':
    init_db()
    app.run(debug=True)