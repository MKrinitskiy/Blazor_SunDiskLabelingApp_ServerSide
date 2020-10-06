import argparse, warnings, datetime, os
import numpy as np
from .ServiceDefs import ServiceDefs


def parse_args(args):
    parser = argparse.ArgumentParser(description='flask server for the labeling program')

    parser.add_argument('--disable-mongodb', dest='disable_mongodb', help='disabling mongodb service interaction', action='store_true')
    parser.add_argument('--port', dest='port', help='port for the flask app to listen to', default=2019, type=int)

    return preprocess_args(parser.parse_args(args))


def preprocess_args(parsed_args):
    return parsed_args