from sassandsass import app
import sassandsass.config as config
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="run in debug mode", action="store_true")
args = parser.parse_args()

if args.debug:
    app.config.from_object(config.DebugConfig)
else:
    app.config.from_object(config.Config)

app.run()
