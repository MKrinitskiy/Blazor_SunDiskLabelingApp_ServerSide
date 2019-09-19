from .support_defs import *
import json

ErrorCodes = enum(['NoError', 'GenericError', 'UnknownError', 'FileNotFoundError', 'ClientIDnotFound', 'NotImplementedError'])

class WebAPI_error(object):
    def __init__(self, error_code = ErrorCodes.NoError, error_description = ""):
        self.ErrorCode = error_code
        self.ErrorDescription = error_description
        super(WebAPI_error, self).__init__()

    def ToJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)