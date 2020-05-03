from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs

def url_rule_root(app):
    with app.app_context():
        ServiceDefs.LogRequest('./logs/app.log', request)
        response = make_response('Nothing to do here')
        response.headers['ErrorDesc'] = 'CommandNotUnderstood'
        return response
