import os
import sys

from aiohttp import web

sys.path.append(os.getcwd())  # noqa

import yaml
from argparse import ArgumentParser

from int20h_test import views, services, api


def parse_config_file_name():
    parser = ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    return args.config


def load_config_from_file(config_file):
    with open(config_file) as f:
        config = yaml.load(f)

    return config


def create_app(config_file):
    app = web.Application()
    config = load_config_from_file(config_file)

    #  Setup modules
    services_config = config['SERVICES']
    services.setup(services_config)


    views.setup(app)
    api.setup(app)


    return app


if __name__ == '__main__':
    config_file = parse_config_file_name()
    app = create_app(config_file)

    web.run_app(app, host='0.0.0.0', port=8080)
