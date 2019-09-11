from serverside_APIs import *
from libs import *
import binascii, cv2


def MakeImageDataHelper(app, webapi_client_id = ''):
    if webapi_client_id == '':
        raise Exception('client ID not specified!')

    app.clientHelpers[webapi_client_id] = AllSkyImagesDataAPI()
    retval = WebAPI_response(response_code=ResponseCodes.OK,
                             error=WebAPI_error(),
                             response_description="Session created successfully")
    print("sending JSON response:")
    print('JSON: ' + retval.ToJSON())
    return retval.ToJSON()





def NextImage(app, webapi_client_id, cache_abs_path):
    # DONE: store the images IDs for the PreviousImage() to work properly
    # category=general functionality issue=none estimate=2h

    clientHelper = app.clientHelpers[webapi_client_id]
    tmp_base_fname = 'plot-%s.jpg' % binascii.hexlify(os.urandom(5)).decode('ascii')
    tmp_fname = os.path.join(cache_abs_path, tmp_base_fname)
    clientHelper.read_next_image(tmp_image_fname=tmp_fname)

    img_uri = urljoin('cache', tmp_base_fname)

    response = WebAPI_response(response_code=ResponseCodes.OK,
                               error=WebAPI_error(),
                               response_description="new image sucessfully prepared")
    response.StringAttributes['imageURL'] = img_uri

    response.StringAttributes['SunDisk_RoundDataWithUnderlyingImgSize'] = ToJSON(RoundDataWithUnderlyingImgSize(RoundData(512,512,100), Size(1920, 1920)))
    response.StringAttributes['ImgSize_'] = ToJSON(Size(1920, 1920))

    print("sending JSON response:")
    print('JSON: ' + response.ToJSON())
    return response.ToJSON()



def PreviousImage(app, webapi_client_id, cache_abs_path):
    # DONE: Implement PreviousImage(app, webapi_client_id, cache_abs_path)
    # category=handlers issue=none estimate=2h
    # The mechanics should involve storing all the images that was already processed
    # and PreviousImage() should return them in reversed order

    # TODO: fix PreviousImage
    # category=handlers issue=none estimate=1h
    # PreviousImage works wrong. It returns the last example which is actually current

    print('entered PreviousImage()')

    clientHelper = app.clientHelpers[webapi_client_id]
    print('got clientHelper for the client %s' % webapi_client_id)

    tmp_fname = clientHelper.generated_examples_history.pop()
    tmp_fname = clientHelper.generated_examples_history.pop()
    print('tmp_fname = %s' % tmp_fname)

    tmp_base_fname = os.path.basename(tmp_fname)
    print('tmp_base_fname = %s' % tmp_base_fname)

    img_uri = urljoin('cache', tmp_base_fname)

    response = WebAPI_response(response_code=ResponseCodes.OK,
                               error=WebAPI_error(),
                               response_description="previous image sucessfully found")
    response.StringAttributes['imageURL'] = img_uri

    response.StringAttributes['SunDisk_RoundDataWithUnderlyingImgSize'] = ToJSON(
        RoundDataWithUnderlyingImgSize(RoundData(512, 512, 100), Size(1920, 1920)))
    response.StringAttributes['ImgSize_'] = ToJSON(Size(1920, 1920))

    print("sending JSON response:")
    print('JSON: ' + response.ToJSON())
    return response.ToJSON()