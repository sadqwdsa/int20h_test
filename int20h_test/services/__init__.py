from int20h_test.services.flickr_service import FlickrService

_flickr_service = None


def setup(config):
    global _flickr_service

    flickr_config = config['FLICKR']
    _flickr_service = FlickrService.create_with_config(flickr_config)


def flick_service():
    assert _flickr_service is not None, 'Flickr service is not initialized!'
    return _flickr_service
