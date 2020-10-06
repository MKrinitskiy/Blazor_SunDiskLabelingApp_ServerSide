from flask import request, make_response, Response
from libs.ServiceDefs import ServiceDefs
from libs.WebAPI_response import *
from libs.ServersideHandlers import ServersideHandlers
from flask import g
from libs.interfaces import *



def url_rule_labels(app):
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
            return Response(response.ToJSON(), mimetype='application/json')

        command = request.args['command']
        if request.method == 'POST':
            if command == 'post_current_example_labels':
                data_received = request.data
                # print("received data:")
                # print(data_received.decode('utf-8'))
                jsontext = ''.join([l.replace('\n', '').strip() for l in data_received.decode('utf-8')])
                data_dict = json.loads(jsontext)
                decoded_labels = ExampleLabels.from_json(data_dict)

                if not app.disable_mongodb:
                    app.db.insert_example_labels(data_dict)

                response = app.response_class(response="", status=200, mimetype='text/plain')
                return response
        elif request.method == 'GET':
            if command == 'get_current_example_labels':
                if not app.disable_mongodb:
                    img_basename = request.args['img_basename']
                    found_example_labels = app.db.read_example_labels(img_basename)
                    if found_example_labels is None:
                        response = WebAPI_response(response_code=ResponseCodes.OK,
                                                   error=WebAPI_error(error_code = ErrorCodes.NoError,
                                                                      error_description=''),
                                                   response_description='there are still no labels for this image')
                        # response = WebAPI_response(response_code=ResponseCodes.Error,
                        #                            error=WebAPI_error(error_code = ErrorCodes.NotImplementedError,
                        #                                               error_description='sorry, the command ' + command + ' is not implemented at serverside yet'),
                        #                            response_description='could not execute the command')
                    else:
                        response = WebAPI_response(response_code=ResponseCodes.OK,
                                                   error=WebAPI_error(),
                                                   response_description="found labels created previously")
                        response.StringAttributes['found_example_labels'] = found_example_labels

                        print("sending JSON response:")
                        print('JSON: ' + response.ToJSON())

                    return Response(response.ToJSON(), mimetype='application/json')
                else:
                    response = WebAPI_response(response_code=ResponseCodes.OK,
                                               error=WebAPI_error(error_code = ErrorCodes.NoError,
                                                                  error_description='database connection is turned off so there is no way to get the previous labels'),
                                               response_description='database connection is turned off so there is no way to get the previous labels')
                    return Response(response.ToJSON(), mimetype='application/json')
