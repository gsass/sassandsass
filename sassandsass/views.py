from flask import render_template, url_for, request, redirect, flash
from sassandsass import app
from sassandsass.dbtools import *
from sassandsass.linkers import create_resource_link
from sassandsass.navbar import generate_navbar
from sassandsass.xml_import import XMLExtractor as XE
from werkzeug import secure_filename
import sqlite3


'''Add functions which are called from views to the app's jinja context.'''
app.jinja_env.globals.update(create_resource_link = create_resource_link)
app.jinja_env.globals.update(generate_navbar = generate_navbar)

@app.route('/')
def index():
    return render_template('content.html', name=app.config['LANDING_PAGE'])

@app.route('/<name>')
def namedpage(name):
    if page_exists(name):
        return render_template('content.html', content=fetch_page_content(name))
    else:
        return redirect(url_for('404'))

@app.route('/news')
def newspage(name):
    return render_template('news.html', article=article)

@app.route('/import', methods = ["GET", "POST"])
def importpage():
    if (request.method == "POST"):
        importer = XE()
        files = request.files.getlist("xml")
        errors = {}
        for resource in files:
            try:
                importer.import_page( '\n'.join(resource.readlines()),
                                    secure_filename(resource.filename),
                                    )
            except (sqlite3.Error, IOError) as e:
                errors[secure_filename(resource.filename)] = e

        if len(errors):
            return render_template('import.html', errors=errors)
        elif not len(files):
            flash("Yo you didn't select any files to import.")
        else:
            flash("Yo you imported these files:\n %s" %
                    "\n".join([f.filename for f in files]) )
        return redirect(url_for('index'))
    else:
        return render_template('import.html')
