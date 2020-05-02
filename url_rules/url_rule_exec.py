from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs
from libs.WebAPI_response import *
from libs.ServersideHandlers import ServersideHandlers


def url_rule_exec(app):
    with app.app_context():
        command = request.args['command']
        if command == 'start':
            try:
                webapi_client_id = request.args['webapi_client_id']
            except Exception as ex:
                print(ex)
                ServiceDefs.ReportException('./logs/app.log', ex)
                response = WebAPI_response(response_code=ResponseCodes.Error,
                                           error=WebAPI_error(error_code=ErrorCodes.GenericError,
                                                              error_description='webapi_client_id not presented'),
                                           response_description='could not execute the command')

                return Response(response.ToJSON(), mimetype='application/json')

            return Response(ServersideHandlers.MakeImageDataHelper(app, webapi_client_id=webapi_client_id), mimetype='application/json')
