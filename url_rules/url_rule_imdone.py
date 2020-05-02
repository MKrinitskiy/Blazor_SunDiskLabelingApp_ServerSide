from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs
from libs.WebAPI_response import *
from libs.ServersideHandlers import ServersideHandlers


def url_rule_imdone(app):
    with app.app_context():
        try:
            try:
                webapi_client_id = request.args['webapi_client_id']
            except Exception as ex:
                print(ex)
                ServiceDefs.ReportException('./logs/app.log', ex)
                response = make_response('client webapi ID was not specified')
                response.headers['ErrorDesc'] = 'ClientIDnotSpecified'
                return response

            del app.clientHelpers[webapi_client_id]

            response = make_response('OK')
            response.headers['ErrorDesc'] = ''
            return response
        except Exception as ex:
            print(ex)
            ServiceDefs.ReportException('./logs/app.log', ex)
            response = make_response('SetNewLatLonLimits: UnknownError')
            response.headers['ErrorDesc'] = 'UnknownError'
            return response
