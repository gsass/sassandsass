from flask import session
from flask.ext.login import UserMixin, login_user, make_secure_token
from sassandsass import lm, tumblr
from sassandsass.dbtools import get_user_info, update_user_tokenhash 
import json


@lm.user_loader
def get_user(userid):
    info = get_user_info(ID=userid)
    if info:
        user = User(*info)
        return user
    return None

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
        return user_info.data

def get_tokenhash():
    token = session.get('tumblr_token')
    if token:
        return make_secure_token(*token)
    else:
        return ''

class User(UserMixin):
    def __init__(userid, active, token_hash):
        self.ID = userid
        self.active = active
        self.token_hash = token_hash

    def is_active():
        return self.active

    def is_authenticated():
        #Checks for a token, which is required for authentication.
        token = session.get('tumblr_token')
        if token:
            #Checks that the token is valid.
            if self.token_hash == make_secure_token(*token):
                return True
            '''Otherwise, check that the token gets info for a blog,
            and is therefore a valid auth for our uname'''
            if get_handle() == self.ID:
                update_user_tokenhash(self.ID, 
                        make_secure_token(*token))
                return True
        return False

    def get_id():
        return self.ID

@tumblr.tokengetter
def get_token(token=None):
        return session.get('tumblr_token')
