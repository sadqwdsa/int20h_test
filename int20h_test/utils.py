import yaml
from argparse import ArgumentParser


def parse_config_file_name():
    parser = ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    return args.config


def load_config_from_file(config_file):
    with open(config_file) as f:
        config = yaml.load(f)

    return config
