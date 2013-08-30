from flask import render_template, url_for
from sassandsass import app
from sassandsass.dbtools import *


@app.route('/<name>')
def namedpage(name):
    return render_template('content.html', name=name)
 
