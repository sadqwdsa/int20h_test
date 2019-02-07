import logging

import flickr_api

log = logging.getLogger(__name__)


class FlickrService:

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret

    @classmethod
    def create_with_config(cls, config):
        flickr_service = None

        api_key = config.get('API_KEY')
        api_secret = config.get('API_SECRET')

        if api_key and api_secret:
            # flickr_service = FlickrService(
            #     api_key=api_key,
            #     api_secret=api_secret,
            # )
            #
            # a = flickr_api.auth.AuthHandler()
            # perms = "read"
            # url = a.get_authorization_url(perms)
            #
            # print(url)

            # user = flickr_api.Person.findByUserName('alexandra_yefimenko')
            # photos = user.getPhotos()

            print('LAL')

        else:
            log.error('Invalid flickr config!')

        return flickr_service
