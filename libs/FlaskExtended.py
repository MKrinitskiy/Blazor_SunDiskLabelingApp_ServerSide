from flask import Flask
from flask import g

# DONE: transfer clientHelpers to _AppCtxGlobals
# category=architecture issue=none estimate=3h
# If possible, move clientHelpers attribute to the _AppCtxGlobals storage of the Flask app

class FlaskExtended(Flask):
    clientHelpers = dict()
    db = None