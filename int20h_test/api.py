from aiohttp import web

from int20h_test import services


async def get_photos(request):
    json = await request.json()
    emotions = json.get('emotions', [])

    flickr_service = services.flick_service()
    photos_info = await flickr_service.get_photos_info()

    fpp_service = services.face_plus_plus_service()
    filtered_photos_info = await fpp_service.filter_photos_by_emotions(
        photos_info=photos_info[0:10],
        emotions=emotions,
    )

    if photos_info is not None:
        photos_urls = [photo.origin_url for photo in filtered_photos_info]
        payload = {
            'status': 'OK',
            'photos_urls': photos_urls,
        }

    else:
        payload = {
            'status': 'ERROR',
        }

    return web.json_response(payload)


def setup(app):
    app.router.add_get('/api/get_photos', get_photos)

