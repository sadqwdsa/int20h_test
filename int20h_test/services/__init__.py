from int20h_test.services.face_plus_plus_service import FacePlusPlusService
from int20h_test.services.flickr_service import FlickrService

_flickr_service = None
_fpp_service = None


def setup(config):
    global _flickr_service
    global _fpp_service

    flickr_config = config['FLICKR']
    _flickr_service = FlickrService.create_with_config(flickr_config)

    fpp_config = config['FACE_PLUS_PLUS']
    _fpp_service = FacePlusPlusService.create_with_config(fpp_config)


def flick_service():
    assert _flickr_service is not None, 'Flickr service is not initialized!'
    return _flickr_service


def face_plus_plus_service():
    assert _fpp_service is not None, 'Face plus plus service is not initialized!'
    return _fpp_service
