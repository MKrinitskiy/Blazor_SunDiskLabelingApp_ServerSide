from flask import request, make_response, Response

def url_rule_root(app):
    with app.app_context():
        response = make_response('Nothing to do here')
        response.headers['ErrorDesc'] = 'CommandNotUnderstood'
        return response
