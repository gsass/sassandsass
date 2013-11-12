from flask import render_template, url_for, \
        request, redirect, flash, abort, session, g, get_template_attribute
from flask.ext.login import login_required, logout_user
from sassandsass import app, lm, tumblr
from sassandsass.dbtools import *
from sassandsass.xml_import import XMLExtractor as XE
from sassandsass.edit_nav import Editor
from sassandsass.images import get_available_images
from werkzeug import secure_filename
import sassandsass.user_management as users
import sqlite3


@app.route('/')
def index():
    index = app.config['LANDING_PAGE']
    if page_exists(index):
        return render_template('content.html',
                name=index,
                content = fetch_page_content(index))
    else:
        flash("Yo you should import %s.xml" % index)
        return redirect(url_for('importpage'))

@app.route('/<name>')
def namedpage(name):
    if page_exists(name):
        return render_template('content.html',
                name=name,
                content=fetch_page_content(name))
    else:
        abort(404)

@app.route('/news')
def newspage():
    blog = tumblr.get("blog/sassandsass.tumblr.com/posts/text",
            data = dict(api_key=app.config["CONSUMER_KEY"]))
    posts = blog.data["response"]["posts"]
    return render_template('news.html', posts=posts)

@app.route('/import', methods = ["GET", "POST"])
@login_required
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
            except Exception as e:
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

@app.route('/get_editor', methods=["POST"])
def get_edit_form():
    page = request.form.get("page")
    edit_data = {"section": request.form.get("section"),
                "images": get_available_images()}
    form = get_template_attribute('edit_content.html', 
            request.form.get("type"))
    return form(page, fetch_page_content(page), edit_data)

@app.route('/edit_page', methods = ["POST"])
@login_required
def edit_page():
    msg = update_page_content(request.form)
    flash(msg)
    return redirect(request.referrer)

@app.route('/edit_image', methods = ["POST"])
@login_required
def edit_page_image():
    msg = update_page_image(request.form, request.files)
    flash(msg)
    return redirect(request.referrer)

@app.route('/edit_nav', methods = ["POST"])
@login_required
def edit_nav():
    e = Editor()
    result = e.edit_nav(request.form)
    flash(result)
    return redirect(request.referrer)

@app.route('/login')
def login():
    if g.logged_in:
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
@login_required
def logout():
    session['tumblr_token'] = None
    logout_user()
    return redirect(url_for('index'))

@app.route('/install')
def install():
    install_steps = (
            ('check_db', "DB Initialized."),
            ('add_admin', "You added %s as the site admin, and are logged in.\
                    Let's import some content now."),
            ('import', "Great!  You're set to go.\
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
