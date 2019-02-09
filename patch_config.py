import os

import yaml
from int20h_test.utils import parse_config_file_name, load_config_from_file


def patch_config(config):
    config["SERVICES"]["FACE_PLUS_PLUS"]["API_SECRET"] = os.environ.get("FACE_PLUS_PLUS_API_SECRET")
    config["SERVICES"]["FACE_PLUS_PLUS"]["API_KEY"] = os.environ.get("FACE_PLUS_PLUS_API_KEY")
    config["SERVICES"]["FLICKR"]["API_KEY"] = os.environ.get("FLICKR_API_KEY")


if __name__ == '__main__':
    config_default = parse_config_file_name()
    config_file = os.environ.get('PATH_TO_CONFIG_FILE')

    print(f'Patching {config_default}...')

    config = load_config_from_file(config_default)
    patch_config(config)

    with open(config_file, 'w+') as f:
        yaml.dump(config, f)

    print(f'Successfully patched {config_file}...')
