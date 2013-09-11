from sassandsass import app
import sassandsass.config as config
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="run in debug mode")
args = parser.parse_args()

debug = ((args.debug=="True") if args.debug is not None else False)

if debug:
    app.config.from_object(config.DebugConfig)
else:
    app.config.from_object(config.Config)

app.run(debug = debug)
