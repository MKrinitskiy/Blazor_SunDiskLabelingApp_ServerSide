from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs
from libs.WebAPI_response import *
from libs.ServersideHandlers import ServersideHandlers
from flask import g


def url_rule_image(app):
    with app.app_context():
        ServiceDefs.LogRequest('./logs/app.log', request)
        try:
            webapi_client_id = request.args['webapi_client_id']
        except Exception as ex:
            print(ex)
            ServiceDefs.ReportException('./logs/errors.log', ex)
            response = WebAPI_response(response_code=ResponseCodes.Error,
                                       error=WebAPI_error(error_code=ErrorCodes.GenericError,
                                                          error_description='webapi_client_id not presented'),
                                       response_description='could not execute the command')
            return Response(response.ToJSON(), mimetype='application/json')

        if webapi_client_id not in app.clientHelpers.keys():
            ex = Exception("presented client webapi ID not found in the list of started IDs")
            ServiceDefs.ReportException('./logs/errors.log', ex)
            response = WebAPI_response(response_code=ResponseCodes.Error,
                                       error=WebAPI_error(error_code=ErrorCodes.ClientIDnotFound,
                                                          error_description='presented client webapi ID not found in the list of started IDs'),
                                       response_description='unable to get an image for a client without a session')
            return response



        command = request.args['command']
        if command == 'get_next_image':
            return Response(ServersideHandlers.NextImage(app, webapi_client_id=webapi_client_id, cache_abs_path=os.path.abspath('./cache/')), mimetype='application/json')

        if command == 'get_previous_image':
            return Response(ServersideHandlers.PreviousImage(app, webapi_client_id=webapi_client_id, cache_abs_path=os.path.abspath('./cache/')), mimetype='application/json')

        elif command == 'get_the_image':
            try:
                arg_src_fname = request.args['src_fname']
            except Exception as ex:
                print(ex)
                ServiceDefs.ReportException('./logs/errors.log', ex)
                response = make_response('source file was not specified')
                response.headers['ErrorDesc'] = 'FileNotFound'
                return response
