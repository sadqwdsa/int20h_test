import os
import sys

sys.path.append(os.getcwd())  # noqa

import yaml
from argparse import ArgumentParser
from flask import Flask

from int20h_test import views


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
    app = Flask(__name__)
    config = load_config(config_file)

    app_config = config['APP']
    app.config.update(app_config)

    #  TODO: setup modules here
    views.setup(app, None)

    return app


if __name__ == '__main__':
    config_file = parse_config_file_name()
    app = create_app(config_file)

    app.run(host='0.0.0.0', port=8080)
