import sqlite3
from flask import g
from contextlib import closing
from sassandsass import app


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('../schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def page_exists(pagename):
    page_id = g.db.execute("SELECT id FROM pages WHERE link_alias = ?", (pagename,))
    return (page_id.fetchone() is not None)

def fetch_page_content(pagename):
    cur = g.db.execute("SELECT title, blurb, imagename, content " +
            "FROM pages WHERE link_alias = ?", (pagename,))
    return dict(zip(["title","blurb", "img", "content"], cur.fetchone()))
