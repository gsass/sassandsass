from flask import render_template, url_for
from sassandsass import app
from sassandsass.dbtools import *
from sassandsass.linkers import create_resource_link
from sassandsass.navbar import generate_navbar


'''Add functions which are called from views to the app's jinja context.'''
app.jinja_env.globals.update(create_resource_link = create_resource_link)
app.jinja_env.globals.update(generate_navbar = generate_navbar)

@app.route('/<name>')
def namedpage(name):
    return render_template('content.html', name=name)
 
