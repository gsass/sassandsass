from flask import render_template, url_for, request, redirect, flash
from sassandsass import app
from sassandsass.dbtools import *
from sassandsass.linkers import create_resource_link
from sassandsass.navbar import generate_navbar
from sassandsass.xml_import import XMLExtractor as XE


'''Add functions which are called from views to the app's jinja context.'''
app.jinja_env.globals.update(create_resource_link = create_resource_link)
app.jinja_env.globals.update(generate_navbar = generate_navbar)

@app.route('/')
def landingpage():
    return render_template('content.html', name=app.config['LANDING_PAGE'])

@app.route('/<name>')
def namedpage(name):
    return render_template('content.html', name=name)

@app.route('/news/<article>')
def newspage(name):
    return render_template('news.html', article=article)

@app.route('/import')
def importpage(name):
    if (request.method == "POST"):
        importer = XE()
        files = request.form["files"]
        errors = {}
        for fname in files:
            try:
                importer.import_page(fname)
            except RuntimeError as e:
                errors[fname] = e

        if len(fname):
            return render_remplate('import.html', errors=errors)
        else:
            flash("Yo you imported these files:\n %s" % "\n".join(files) )
            return redirect(url_for('/'))
    else:
        return render_remplate('import.html')
