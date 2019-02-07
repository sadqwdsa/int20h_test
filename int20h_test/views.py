from aiohttp import web


async def index(request):
    return web.FileResponse('static/index.html')


def setup(app):
    app.router.add_get('/', index)
