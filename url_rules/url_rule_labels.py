from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs
from libs.WebAPI_response import *
from libs.ServersideHandlers import ServersideHandlers



def url_rule_labels(app):
    with app.app_context():
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

        if webapi_client_id not in app.clientHelpers.keys():
            ex = Exception("presented client webapi ID not found in the list of started IDs")
            ServiceDefs.ReportException('./logs/app.log', ex)
            response = WebAPI_response(response_code=ResponseCodes.Error,
                                       error=WebAPI_error(error_code=ErrorCodes.ClientIDnotFound,
                                                          error_description='presented client webapi ID not found in the list of started IDs'),
                                       response_description='unable to get an image for a client without a session')
            return Response(response.ToJSON(), mimetype='application/json')

        command = request.args['command']
        if request.method == 'POST':
            if command == 'post_current_example_labels':
                # TODO: implement the command post_current_example_labels of the labels route
                # category=functionality issue=none estimate=6h

                data_received = request.data
                print("received data:")
                print(data_received)
                response = app.response_class(response="", status=200, mimetype='text/plain')
                return response
        elif request.method == 'GET':
            if command == 'get_current_example_labels':
                # TODO: implement the command get_current_example_labels of the labels route
                # category=functionality issue=none estimate=6h
                # return Response(NextImage(app,
                #                           webapi_client_id=webapi_client_id, cache_abs_path=os.path.abspath('./cache/')),
                #                 mimetype='application/json')
                response = WebAPI_response(response_code=ResponseCodes.Error,
                                           error=WebAPI_error(error_code = ErrorCodes.NotImplementedError,
                                                              error_description='sorry, the command ' + command + ' is not implemented at serverside'),
                                           response_description='could not execute the command')
                return Response(response.ToJSON(), mimetype='application/json')
