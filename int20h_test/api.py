from aiohttp import web

from int20h_test import services


async def get_photos(request):

    flickr_service = services.flick_service()
    photos_info = await flickr_service.get_photos_info()

    # TODO: implement filter by emotions
    # json = await request.json()

    if photos_info is not None:
        photos_urls = [photo.origin_url for photo in photos_info]
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

