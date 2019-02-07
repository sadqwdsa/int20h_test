from aiohttp import web


async def index(request):
    return web.Response(text='Hello, world')


def setup(app):
    app.router.add_get('/', index)
