from flask import Flask
import sassandsass.config
from sassandsass.linkers import create_resource_link

debug = True

app = Flask(__name__)
if debug:
    app.config.from_object(config.DebugConfig)
else:
    app.config.from_object(config.Config)
app.jinja_env.globals.update(create_resource_link=create_resource_link)

import sassandsass.views
