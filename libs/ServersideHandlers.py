from serverside_APIs import AllSkyImagesDataAPI
from .ServiceDefs import *
from .WebAPI_response import *
import binascii, cv2
from flask import g
import os



class ServersideHandlers():
    @classmethod
    def MakeImageDataHelper(cls, app, webapi_client_id = ''):
        with app.app_context():
            if webapi_client_id == '':
                raise Exception('client ID not specified!')

            app.clientHelpers[webapi_client_id] = AllSkyImagesDataAPI()
            retval = WebAPI_response(response_code=ResponseCodes.OK,
                                     error=WebAPI_error(),
                                     response_description="Session created successfully")
            print("sending JSON response:")
            print('JSON: ' + retval.ToJSON())
            return retval.ToJSON()


    @classmethod
    def NextImage(cls, app, webapi_client_id, cache_abs_path):
        with app.app_context():
            clientHelper = app.clientHelpers[webapi_client_id]
            ServiceDefs.EnsureDirectoryExists(cache_abs_path)
            tmp_base_fname = 'plot-%s.jpg' % binascii.hexlify(os.urandom(5)).decode('ascii')
            tmp_fname = os.path.join(cache_abs_path, tmp_base_fname)
            example = clientHelper.read_next_image(tmp_image_fname=tmp_fname)

            img_uri = ServiceDefs.urljoin('cache', tmp_base_fname)

            response = WebAPI_response(response_code=ResponseCodes.OK,
                                       error=WebAPI_error(),
                                       response_description="new image sucessfully prepared")
            response.StringAttributes['imageURL'] = img_uri

            response.StringAttributes['imgBaseName'] = example.img_basename

            print("sending JSON response:")
            print('JSON: ' + response.ToJSON())
            return response.ToJSON()


    @classmethod
    def SpecificImage(cls, app, webapi_client_id, cache_abs_path, **kwargs):
        assert 'specific_image_basename' in kwargs.keys()
        specific_image_basename = kwargs['specific_image_basename']

        with app.app_context():
            clientHelper = app.clientHelpers[webapi_client_id]
            ServiceDefs.EnsureDirectoryExists(cache_abs_path)
            tmp_base_fname = 'plot-%s.jpg' % binascii.hexlify(os.urandom(5)).decode('ascii')
            tmp_fname = os.path.join(cache_abs_path, tmp_base_fname)
            example = clientHelper.read_sprcific_image(img_basename = specific_image_basename, tmp_image_fname=tmp_fname)

            img_uri = ServiceDefs.urljoin('cache', tmp_base_fname)

            response = WebAPI_response(response_code=ResponseCodes.OK,
                                       error=WebAPI_error(),
                                       response_description="new image sucessfully prepared")
            response.StringAttributes['imageURL'] = img_uri

            response.StringAttributes['imgBaseName'] = example.img_basename

            print("sending JSON response:")
            print('JSON: ' + response.ToJSON())
            return response.ToJSON()


    @classmethod
    def PreviousImage(cls, app, webapi_client_id, cache_abs_path):
        # DONE: Implement PreviousImage(app, webapi_client_id, cache_abs_path)
        # category=handlers issue=none estimate=2h
        # The mechanics should involve storing all the images that was already processed
        # and PreviousImage() should return them in reversed order
        with app.app_context():
            print('entered PreviousImage()')

            clientHelper = app.clientHelpers[webapi_client_id]
            ServiceDefs.EnsureDirectoryExists(cache_abs_path)
            print('got clientHelper for the client %s' % webapi_client_id)

            print('=======getting previous example======')
            print([t.img_basename for t in clientHelper.generated_examples_history])
            if len(clientHelper.generated_examples_history) >= 2:
                _ = clientHelper.generated_examples_history.pop()
                example = clientHelper.generated_examples_history[-1]
            else:
                tmp_base_fname = 'plot-%s.jpg' % binascii.hexlify(os.urandom(5)).decode('ascii')
                tmp_fname = os.path.join(cache_abs_path, tmp_base_fname)
                example = clientHelper.read_next_image(tmp_image_fname=tmp_fname)
            print('got example: %s' % example.img_basename)


            tmp_base_fname = os.path.basename(example.cached_file_name)
            print('tmp_base_fname = %s' % tmp_base_fname)

            img_uri = ServiceDefs.urljoin('cache', tmp_base_fname)

            response = WebAPI_response(response_code=ResponseCodes.OK,
                                       error=WebAPI_error(),
                                       response_description="previous image sucessfully found")
            response.StringAttributes['imageURL'] = img_uri
            response.StringAttributes['imgBaseName'] = example.img_basename

            print("sending JSON response:")
            print('JSON: ' + response.ToJSON())
            return response.ToJSON()
