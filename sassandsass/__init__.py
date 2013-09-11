from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)

import sassandsass.views
