from int20h_test.services.flickr_service import FlickrService


def setup(config):
    #  TODO: configure services f. e. set Flirk API url and API key

    flickr_config = config['FLICKR']
    flickr_service = FlickrService.create_with_config(flickr_config)

    pass
