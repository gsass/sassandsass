from flask import render_template, url_for, \
        request, redirect, flash, abort, session
from flask.ext.login import current_user
from sassandsass import app, lm, tumblr
import sassandsass.user_management as users
from sassandsass.dbtools import *
from sassandsass.linkers import create_resource_link
from sassandsass.navbar import generate_navbar
from sassandsass.xml_import import XMLExtractor as XE
from sassandsass.edit_nav import Editor
from werkzeug import secure_filename
import sqlite3


'''Add functions which are called from views to the app's jinja context.'''
app.jinja_env.globals.update(create_resource_link = create_resource_link)
app.jinja_env.globals.update(generate_navbar = generate_navbar)
app.jinja_env.globals.update(get_available_pages = get_available_pages)
app.jinja_env.globals.update(zip = zip)

@app.route('/')
def index():
    session['admin'] = app.config["DEBUG"]
    index = app.config['LANDING_PAGE']
    if page_exists(index):
        return render_template('content.html',
                                content = fetch_page_content(index))
    else:
        flash("Yo you should import %s.xml" % index)
        return redirect(url_for('importpage'))

@app.route('/<name>')
def namedpage(name):
    if page_exists(name):
        return render_template('content.html',
                                content=fetch_page_content(name))
    else:
        abort(404)

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
    return render_template('import.html')

@app.route('/edit_nav', methods = ["GET", "POST"])
def edit_nav():
    if (request.method == "POST"):
        e = Editor()
        result = e.edit_nav(request.form)
        flash(result)
    return redirect(request.referrer)

@app.route('/login')
def login():
    if not current_user.is_anonymous():
        flash("Yo you're already logged in.")
        return redirect(request.referrer or url_for('index'))
    else:
        if session.has_key('tumblr_token'):
            del session['tumblr_token']
        return tumblr.authorize(callback=url_for('authenticate',
                    next=request.args.get('next') or request.referrer or None))

@app.route('/authenticate')
@tumblr.authorized_handler
def authenticate(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    else:
        session['tumblr_token'] = (
                resp['oauth_token'],
                resp['oauth_token_secret']
                )
        user = users.do_login()
        if user:
            flash("You were logged in as %s." % user.get_id())
    return redirect(next_url)

@app.route('/logout')
def logout():
    session['tumblr_token'] = None
    flash("Logged out succesfully.")
    return redirect(url_for('index'))

@app.route('/install')
def install():
    install_steps = (
            ('check_db', "DB Initialized."),
            ('add_admin', "You added %s as the site admin, and are logged in.\
                    Let's import some content now."),
            ('import_pages', "Great!  You're set to go.\
                    Visit '/admin' to make further changes."))
    current_step =  (session.get('INSTALL_STEP') or 0)
    if current_step + 1 < len(install_steps):
        nextpage, success_msg = install_steps[current_step]
        session['success_msg'] = success_msg
        session['INSTALL_STEP'] = current_step + 1
        return redirect(url_for(nextpage, next=url_for('install')))
    else:
        session['INSTALL_STEP'] = None
        return redirect(url_for('index'))

@app.route('/check_db')
def check_db():
    nextpage = (request.args.get('next')
            or request.referrer
            or url_for('importpage'))
    try:
        #test to check if DB exists
        g.db.execute("SELECT id FROM pages")
        flash("DB already initialized."+
                " Did you mean to import pages instead?")
    except sqlite3.OperationalError:
        init_db()
        flash(session.get('success_msg'))
    return redirect(nextpage)

@app.route('/add_admin')
def add_admin():
    admins = g.db.execute("SELECT userid FROM users WHERE active")
    handle = users.get_handle()
    if admins.fetchone() is not None:
        #Do nothing if admins already exist.
        flash ('Yo an admin already exists for this site.')
    elif handle is not None:
        #Add an admin once the user has authenticated via tumblr.
        reg = register_user(handle, users.get_tokenhash())
        flash(reg)
        active = set_user_active(handle, True)
        flash(active)
        users.do_login()
        flash(session.get('success_msg') % handle)
    else:
        #Ask the user to authenticate if they haven't yet.
        return redirect(url_for('login', next=url_for('add_admin')))
    return redirect(request.args.get('next') or url_for('index'))
