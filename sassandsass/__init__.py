from flask import Flask
import sassandsass.config


debug = True

app = Flask(__name__)
if debug:
    app.config.from_object(config.DebugConfig)
else:
    app.config.from_object(config.Config)

import sassandsass.views
