import os
import sys

from aiohttp import web

sys.path.append(os.getcwd())  # noqa

import yaml
from argparse import ArgumentParser

from int20h_test import views, services


def parse_config_file_name():
    parser = ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    return args.config


def load_config(config_file):
    with open(config_file) as f:
        config = yaml.load(f)

    return config


def create_app(config_file):
    app = web.Application()
    config = load_config(config_file)

    app_config = config['APP']
    # app.config.update(app_config)

    #  Setup modules
    views.setup(app)

    services_config = config['SERVICES']
    services.setup(services_config)

    return app


if __name__ == '__main__':
    config_file = parse_config_file_name()
    app = create_app(config_file)

    web.run_app(app, host='0.0.0.0', port=8080)
