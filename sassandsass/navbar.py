from sassandsass import app
from flask import g

def generate_navbar():
    navbar={}
    pages = g.db.execute('SELECT id, children from nav order by rank desc')
    navbar = [dict(page=get_page_descriptor(row[0])[0], children=get_page_descriptor(row[1])) 
             for row in pages.fetchall()]
    return navbar

def get_page_descriptor(ids):
    pages = ids.split(',')
    descriptors = g.db.execute("SELECT link_alias, title FROM pages WHERE id IN (?);", ids)

    links = [(desc[0], desc[1]) for desc in descriptors.fetchall()]
