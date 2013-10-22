from flask import g, session
from flask.ext.login import UserMixin, login_user, \
        make_secure_token, current_user
from sassandsass import app, lm, tumblr
from sassandsass.dbtools import get_user_info, update_user_tokenhash 
import json


@lm.user_loader
def get_user(userid):
    info = get_user_info(userid=userid)
    if info:
        user = User(*info)
        return user
    return None

@app.before_request
def check_login():
    g.logged_in = current_user.is_authenticated()

def do_login():
    user = get_user(get_handle())
    if user is not None:
        login_user(user)
    return user

def get_handle():
    user_info = tumblr.get("user/info")
    if user_info.status == 200:
        uname = user_info.data['response']['user']['name']
        return uname
    else:
        return None

def get_tokenhash():
    token = session.get('tumblr_token')
    if token:
        return make_secure_token(*token)
    else:
        return ''

@tumblr.tokengetter
def get_token(token=None):
    return session.get('tumblr_token')

class User(UserMixin):
    def __init__(self, userid, active, token_hash):
        self.userid = userid
        self.active = active
        self.token_hash = token_hash

    def is_active(self):
        return self.active

    def is_authenticated(self):
        #Checks for a token, which is required for authentication.
        token = session.get('tumblr_token')
        if token:
            #Checks that the token is valid.
            if self.token_hash == make_secure_token(*token):
                return True
            '''Otherwise, check that the token gets info for a blog,
            and is therefore a valid auth for our uname'''
            if get_handle() == self.userid:
                update_user_tokenhash(self.userid, 
                        make_secure_token(*token))
                return True
        return False

    def get_id(self):
        return self.userid
