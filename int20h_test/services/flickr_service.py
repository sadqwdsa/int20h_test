import asyncio
from urllib.parse import urlencode

import aiohttp

from int20h_test.model import PhotoInfo


class FlickrService:

    def __init__(
        self,
        api_key,
        search_album_id,
        search_user_id,
        search_text,
        api_url,
    ):
        self._api_key = api_key
        self._search_album_id = search_album_id
        self._search_user_id = search_user_id
        self._search_text = search_text
        self._api_url = api_url

        self._photos_info_cache = None

    @classmethod
    def create_with_config(cls, config):
        flickr_service = None

        api_key = config.get('API_KEY')
        search_album_id = config.get('SEARCH_ALBUM_ID')
        search_user_id = config.get('SEARCH_USER_ID')
        search_text = config.get('SEARCH_TEXT')
        api_url = config.get('API_URL')
        if (
            api_key
            and search_album_id
            and search_user_id
            and search_text
            and api_url
        ):
            flickr_service = FlickrService(
                api_key=api_key,
                search_album_id=search_album_id,
                search_user_id=search_user_id,
                search_text=search_text,
                api_url=api_url,
            )

            loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(
                coro=flickr_service._load_photos_info(),
                loop=loop,
            )

        return flickr_service

    async def _load_photos_info(self):
        async with aiohttp.ClientSession() as session:
            done, _ = await asyncio.wait([
                self._get_photos_by_text(
                    session,
                    self._search_text
                ),
                self._get_photos_from_photoset(
                    session,
                    self._search_album_id,
                    self._search_user_id,
                ),
            ])

        loaded_photos_info = set()

        for task in done:
            loaded_photos_info.update(task.result())

        distinct_photos_info = list(loaded_photos_info)
        distinct_photos_info.sort(key=lambda photo_info: photo_info.id)

        self._photos_info_cache = tuple(distinct_photos_info)

    def _invalidate_photos_info_cache(self):
        self._photos_info_cache = None

    #  LoL, `bisect.bisect` can not search with key
    def _bisect_with_key(self, sorterd_collection, search_value, key):
        lo = 0
        hi = len(sorterd_collection)

        while lo < hi:
            mid = (lo + hi) // 2
            if key(sorterd_collection[mid]) < search_value:
                lo = mid + 1
            else:
                hi = mid
        return lo

    async def get_photos_info(self, from_id):
        all_photos_info = self._photos_info_cache

        from_idx = self._bisect_with_key(
            sorterd_collection=all_photos_info,
            search_value=from_id,
            key=lambda photo_info: photo_info.id,
        )

        from_idx += 1  # Because not inclusive
        result_photos_info = all_photos_info[from_idx: len(all_photos_info)]

        return result_photos_info

    async def _get_photos_from_photoset(self, session, photoset_id, user_id):
        url_params = {
            'method': 'flickr.photosets.getPhotos',
            'api_key': self._api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'photoset_id': photoset_id,
            'user_id': user_id,
            'extras': 'url_m, url_h, url_z',
            'per_page': 500,
        }

        url_query = urlencode(url_params, encoding='UTF-8')
        url = f'{self._api_url}?{url_query}'

        async with session.get(url) as resp:
            json = await resp.json()

            status = json.get('stat')
            if status != 'ok':
                return None

            payload = json.get('photoset')
            if not payload:
                return None

            photos_payload = payload.get('photo')
            if photos_payload is None:
                return None

            photos_info = []
            for photo_payload in photos_payload:
                photo_info = self._deserialize_photo_info(
                    photo_payload
                )

                if photo_info is not None:
                    photos_info.append(photo_info)
                else:
                    return None

            return photos_info

    async def _get_photos_by_text(self, session, search_test):
        url_params = {
            'method': 'flickr.photos.search',
            'api_key': self._api_key,
            'format': 'json',
            'nojsoncallback': 1,
            'text': search_test,
            'extras': 'url_m, url_h, url_z',
            'per_page': 500,
        }

        url_query = urlencode(url_params, encoding='UTF-8')
        url = f'{self._api_url}?{url_query}'

        async with session.get(url) as resp:
            json = await resp.json()

            status = json.get('stat')
            if status != 'ok':
                return None

            payload = json.get('photos')
            if not payload:
                return None

            photos_payload = payload.get('photo')
            if photos_payload is None:
                return None

            photos_info = []
            for photo_payload in photos_payload:
                photo_info = self._deserialize_photo_info(
                    photo_payload
                )

                if photo_info is not None:
                    photos_info.append(photo_info)
                else:
                    return None

            return photos_info

    def _deserialize_photo_info(self, photo_payload):
        origin_url = photo_payload.get('url_h')
        photo_id = photo_payload.get('id')
        min_url = photo_payload.get('url_m')
        medium_url = photo_payload.get('url_z')

        if origin_url and photo_id:
            return PhotoInfo(
                photo_id=int(photo_id),
                origin_url=origin_url,
                min_url=min_url,
                medium_url=medium_url,
            )

        else:
            return None
