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
    clientHelper = app.clientHelpers[webapi_client_id]
    clientHelper.read_next_image()
    tmp_base_fname = 'plot-%s.jpg' % binascii.hexlify(os.urandom(5)).decode('ascii')
    tmp_fname = os.path.join(cache_abs_path, tmp_base_fname)
    cv2.imwrite(tmp_fname, clientHelper.currentImageBinary)
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

