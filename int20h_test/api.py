from aiohttp import web

from int20h_test import services


async def get_photos(request):
    json = await request.json()

    emotions = json.get('emotions', [])
    from_id = json.get('from_id', 0)
    count = json.get('count', 10)

    flickr_service = services.flick_service()
    photos_info = await flickr_service.get_photos_info(from_id)

    fpp_service = services.face_plus_plus_service()
    filtered_photos_info = await fpp_service.filter_photos_by_emotions(
        photos_info=photos_info,
        emotions=emotions,
        count=count,
    )

    if photos_info is not None:
        payload = {
            'status': 'OK',
            'photos_info': [{
                'id': photo_info.id,
                'origin_url': photo_info.origin_url,
                'min_url': photo_info.min_url,
            } for photo_info in filtered_photos_info],
        }

    else:
        payload = {
            'status': 'ERROR',
        }

    return web.json_response(payload)


def setup(app):
    app.router.add_get('/api/get_photos', get_photos)

