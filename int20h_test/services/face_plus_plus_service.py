from urllib.parse import urlencode

import aiohttp


class Emotion:

    def __init__(self, emotion_id, name):
        self._id = emotion_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


EMOTION_IDS = (
    SADNESS_ID,
    NEUTRAL_ID,
    DISGUST_ID,
    ANGER_ID,
    SURPRISE_ID,
    FEAR_ID,
    HAPPINESS_ID,
) = list(range(7))


class FacePlusPlusService:

    def __init__(
        self,
        api_key,
        api_secret,
        api_url,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._api_url = api_url

        self._photo_emotions_cache = {}

    @classmethod
    def create_with_config(cls, config):
        fpp_service = None

        api_key = config.get('API_KEY')
        api_secret = config.get('API_SECRET')
        api_url = config.get('API_URL')

        if (
            api_key
            and api_secret
            and api_url
        ):
            fpp_service = FacePlusPlusService(
                api_key=api_key,
                api_secret=api_secret,
                api_url=api_url,
            )

        return fpp_service

    async def filter_photos_by_emotions(self, photos_info, emotions, count):
        if not emotions:
            return photos_info[0: count]

        filtered_photos = []
        emotions_set = set(emotions)

        async with aiohttp.ClientSession() as session:
            idx = 0

            while len(filtered_photos) < count:
                photo_info = photos_info[idx]
                photo_emotions = await self._get_photo_emotions_info(
                    session,
                    photo_info,
                )

                photo_emotions_set = set(photo_emotions)
                conjunction = emotions_set & photo_emotions_set

                if len(conjunction) > 0:
                    filtered_photos.append(photo_info)

                idx += 1

        return tuple(filtered_photos)

    async def _get_photo_emotions_info(self, session, photo_info):
        emotions_ids = self._photo_emotions_cache.get(photo_info)

        if emotions_ids is None:
            emotions_ids_set = set()
            url_params = {
                'api_key': self._api_key,
                'api_secret': self._api_secret,
                'return_attributes': 'emotion',
                'image_url': photo_info.medium_url
            }

            url_query = urlencode(url_params, encoding='UTF-8')
            url = f'{self._api_url}?{url_query}'

            async with session.post(url) as resp:
                json = await resp.json()
                faces = json.get('faces')

                if faces is not None:
                    for face in faces:
                        attributes = face.get('attributes')

                        if attributes:
                            emotion_probabilities = attributes.get('emotion')
                            min_emotion_percent = 10.0

                            for emotion, probability in emotion_probabilities.items():
                                if probability > min_emotion_percent:
                                    probable_emotion_id = self._get_emotion_id(
                                        emotion
                                    )

                                    emotions_ids_set.add(probable_emotion_id)

            emotions_ids = tuple(emotions_ids_set)
            self._photo_emotions_cache[photo_info] = emotions_ids

        return emotions_ids

    def _get_emotion_id(self, emotion_name):
        emotions = {
            'sadness': SADNESS_ID,
            'neutral': NEUTRAL_ID,
            'disgust': DISGUST_ID,
            'anger': ANGER_ID,
            'surprise': SURPRISE_ID,
            'fear': FEAR_ID,
            'happiness': HAPPINESS_ID,
        }

        return emotions.get(emotion_name)


