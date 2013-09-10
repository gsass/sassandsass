from sassandsass import app
from flask import g

def generate_navbar():
    navbar={}
    pages = g.db.execute('SELECT id, children from nav order by rank desc')
    navbar = [dict(ID=row[0], page=get_page_descriptor(row[0])[0], children=get_page_descriptor(row[1])) 
             for row in pages.fetchall()]
    return navbar

def get_page_descriptor(ids):
    if not isinstance(ids, tuple):
        ids = (str(ids),)
    descriptors = g.db.execute("SELECT id, link_alias, title FROM pages WHERE id IN (?);", ids)
    links = [dict(zip(['ID','alias','title'],
                        desc))
                for desc in descriptors.fetchall()]
    return links
