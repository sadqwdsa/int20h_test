import os

import yaml
from int20h_test.main import parse_config_file_name, load_config_from_file


def patch_config(config):
    config["SERVICES"]["FACE_PLUS_PLUS"]["API_SECRET"] = os.environ.get("FACE_PLUS_PLUS_API_SECRET")
    config["SERVICES"]["FACE_PLUS_PLUS"]["API_KEY"] = os.environ.get("FACE_PLUS_PLUS_API_KEY")
    config["SERVICES"]["FLICKR"]["API_KEY"] = os.environ.get("FLICKR_API_KEY")


if __name__ == '__main__':
    config_file_name = parse_config_file_name()
    print('Patching {}...'.format(config_file_name))

    config = load_config_from_file(config_file_name)
    patch_config(config)

    with open(config_file_name, 'w') as f:
        yaml.dump(config, f)

    print('Successfully patched {}...'.format(config_file_name))
