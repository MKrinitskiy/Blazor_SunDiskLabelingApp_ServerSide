from flask import Flask
from flask import g


class FlaskExtended(Flask):
    clientHelpers = dict()
