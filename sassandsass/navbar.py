from sassandsass import app
from flask import g

@app.context_processor
def generate_navbar():
    navbar={}
    pages = g.db.execute('SELECT id, children from nav order by rank asc')
    navbar = [dict(ID=row[0],
                page=get_page_descriptor(row[0])[0],
                children=get_page_descriptor(row[1])
                ) 
             for row in pages.fetchall()]
    return dict(navbar=navbar)

def get_page_descriptor(ids):
    if ids:
        if isinstance(ids, (str, unicode)):
            ids = [int(ID) for ID in ids.split(',')]
            #numinserts = len(ids)
            #qstring = "(%s)" % ','.join(["?"]*numinserts)
        else:
            ids=(ids,)
            #qstring = "(?)"
    descriptors = [g.db.execute("SELECT id, link_alias, title FROM pages "+
                                "WHERE id = ?", (ID,)).fetchone()
                                for ID in ids]
    links = [dict(zip(['ID','alias','title'],desc)) 
            for desc in descriptors]
    return links
