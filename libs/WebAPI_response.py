from .support_defs import *
from .WebAPI_error import *
import json
import numpy as np
import numbers
from flask import request, make_response, Response

ResponseCodes = enum(['OK', 'Error'])

class WebAPI_response(Response):
    def __init__(self, response_code = ResponseCodes.OK, error = WebAPI_error(), response_description = ""):
        self.ResponseCode = response_code
        self.Error = error
        self.ResponseDescription = response_description
        self.StringAttributes = dict()
        super(WebAPI_response, self).__init__()

    def ToJSON(self):
        return json.dumps(self, default=object_convertion_rules)
