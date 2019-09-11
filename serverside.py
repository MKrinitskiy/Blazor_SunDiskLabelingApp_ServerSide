import os, sys
python_path = sys.executable
if sys.platform == 'win32':
    os.environ['PROJ_LIB'] = os.path.join(os.path.split(python_path)[0], 'Library', 'share')
elif ((sys.platform == 'linux') | (sys.platform == 'darwin')):
    os.environ['PROJ_LIB'] = os.path.join(sys.executable.replace('bin/python', ''), 'share', 'proj')

sys.path.append('./libs')

from flask import request, make_response, Response
from flask_cors import CORS
from handlers_serverside import *
import binascii, logging
import cv2

app = FlaskExtended(__name__, static_folder='cache')
CORS(app)
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
file_handler = logging.FileHandler('./logs/app.log')

tmp_imag_dir = os.path.join(os.getcwd(), 'tmp')
src_data_dir = os.path.join(os.getcwd(), 'src_data')

@app.route('/')
def main():
    response = make_response('Nothing to do here')
    response.headers['ErrorDesc'] = 'CommandNotUnderstood'
    return response



@app.route('/exec', methods=['GET'])
def exec():
    command = request.args['command']
    if command == 'start':
        try:
            webapi_client_id = request.args['webapi_client_id']
        except Exception as ex:
            print(ex)
            ReportException('./logs/app.log', ex)
            response = WebAPI_response(response_code=ResponseCodes.Error,
                                       error=WebAPI_error(error_code=ErrorCodes.GenericError,
                                                          error_description='webapi_client_id not presented'),
                                       response_description='could not execute the command')
            return response

        return Response(MakeImageDataHelper(app, webapi_client_id=webapi_client_id), mimetype='application/json')


@app.route('/images', methods=['GET'])
def image():
    try:
        webapi_client_id = request.args['webapi_client_id']
    except Exception as ex:
        print(ex)
        ReportException('./logs/app.log', ex)
        response = WebAPI_response(response_code=ResponseCodes.Error,
                                   error=WebAPI_error(error_code=ErrorCodes.GenericError,
                                                      error_description='webapi_client_id not presented'),
                                   response_description='could not execute the command')
        return response

    if webapi_client_id not in app.clientHelpers.keys():
        ex = Exception("presented client webapi ID not found in the list of started IDs")
        ReportException('./logs/app.log', ex)
        response = WebAPI_response(response_code=ResponseCodes.Error,
                                   error=WebAPI_error(error_code=ErrorCodes.ClientIDnotFound,
                                                      error_description='presented client webapi ID not found in the list of started IDs'),
                                   response_description='unable to get an image for a client without a session')
        return response



    command = request.args['command']
    if command == 'get_next_image':
        return Response(NextImage(app,
                                  webapi_client_id=webapi_client_id, cache_abs_path=os.path.abspath('./cache/')),
                        mimetype='application/json')

    if command == 'get_previous_image':
        return Response(PreviousImage(app,
                                      webapi_client_id=webapi_client_id, cache_abs_path=os.path.abspath('./cache/')),
                        mimetype='application/json')

    elif command == 'get_the_image':
        try:
            arg_src_fname = request.args['src_fname']
        except Exception as ex:
            print(ex)
            ReportException('./logs/app.log', ex)
            response = make_response('source file was not specified')
            response.headers['ErrorDesc'] = 'FileNotFound'
            return response








@app.route('/imdone', methods=['GET'])
def imdone():
    try:
        try:
            webapi_client_id = request.args['webapi_client_id']
        except Exception as ex:
            print(ex)
            ReportException('./logs/app.log', ex)
            response = make_response('client webapi ID was not specified')
            response.headers['ErrorDesc'] = 'ClientIDnotSpecified'
            return response

        del app.bmhelpers[webapi_client_id]

        response = make_response('OK')
        response.headers['ErrorDesc'] = ''
        return response
    except Exception as ex:
        print(ex)
        ReportException('./logs/app.log', ex)
        response = make_response('SetNewLatLonLimits: UnknownError')
        response.headers['ErrorDesc'] = 'UnknownError'
        return response


app.run(host='127.0.0.1',port=2019)