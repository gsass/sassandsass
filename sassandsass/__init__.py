from flask import Flask
from flask.ext.login import LoginManager
from flask_oauth import OAuth

#Set up our App
app = Flask(__name__)

#Set up the Login Manager for the app
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#Set up authentication via tumblr
auth = OAuth()
tumblr = auth.remote_app('tumblr',
        base_url = 'http://api.tumblr.com/v2/',
        request_token_url = 'http://www.tumblr.com/oauth/request_token',
        access_token_url = 'http://www.tumblr.com/oauth/access_token',
        authorize_url = 'http://www.tumblr.com/oauth/authorize',
        consumer_key = '5GAdCxJZbjUvPqa24rWGZCSUSAoow2MtZrEj1uBipKiZhNAZ4W',
        consumer_secret = 'jf0rnwdWfopxlkbAcN4q7iaJxOYovKqZ867ehmSe42cLDfG2jS')

#Import app views - TODO: possible import for debugging views?
import sassandsass.views
import sassandsass.dbtools
import sassandsass.linkers

