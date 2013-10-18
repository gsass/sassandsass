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
    page_id = g.db.execute("SELECT id FROM pages WHERE link_alias = ?",
            (pagename,))
    return (page_id.fetchone() is not None)

def fetch_page_content(pagename):
    cur = g.db.execute("SELECT title, blurb, imagename, content " +
            "FROM pages WHERE link_alias = ?", (pagename,))
    return dict(zip(["title","blurb", "img", "content"], cur.fetchone()))

@app.context_processor
def get_available_pages():
    cur = g.db.execute("SELECT id, title from pages "+
                        "WHERE id NOT IN (SELECT id FROM nav)")
    return dict(available_pages = cur.fetchall())

def get_user_info(**kwargs):
    if 'userid' in kwargs:
        with closing(connect_db()) as db:
            try:
                cur = db.execute("SELECT userid, active, tokenhash FROM users "+
                    "WHERE userid = :userid", kwargs)
                return cur.fetchone()
            except sqlite3.OperationalError:
                return None
    return None

def register_user(userid, tokenhash = ''):
    msg = "Adding user %s" % userid
    try:
        cur = g.db.execute("INSERT INTO users\
                            (userid, tokenhash) VALUES (?, ?)", 
                            (userid, tokenhash))
    except sqlite3.Error as error:
        return "%s...%s" % (msg, error)
    g.db.commit()
    return "%s...Success!" % msg

def set_user_active(userid, active):
    msg = "%s user %s" % (("Activating" if active else "Deactivating"),
                            userid)
    cur = g.db.execute("SELECT * FROM users WHERE userid = ?", (userid,))
    if cur.fetchone():
        try:
            g.db.execute("UPDATE users SET active = ? WHERE userid = ?", 
                                (active, userid))
        except sqlite3.Error as error:
            return "%s...%s" % (msg, error)
        g.db.commit()
        return "%s...Success!" % msg
    else:
        return "User %s doesn't exist; can't activate." % userid

def update_user_tokenhash(userid, tokenhash):
    msg = "Updating token hash for user %s" % userid
    try:
        cur = g.db.execute("UPDATE users SET tokenhash = ? WHERE userid = ?", 
                            (tokenhash, userid))
    except sqlite3.Error as error:
        return "%s...%s" % (msg, error)
    g.db.commit()
    return "%s...Success!" % msg
