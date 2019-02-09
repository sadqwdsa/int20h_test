import os
import sys

from aiohttp import web

sys.path.append(os.getcwd())  # noqa

from int20h_test import views, services, api
from int20h_test.utils import load_config_from_file, parse_config_file_name


def create_app(config_file):
    app = web.Application()
    config = load_config_from_file(config_file)

    services_config = config['SERVICES']
    services.setup(services_config)

    views.setup(app)
    api.setup(app)

    return app


if __name__ == '__main__':
    config_file = parse_config_file_name()
    app = create_app(config_file)

    web.run_app(app, host='0.0.0.0', port=8080)
