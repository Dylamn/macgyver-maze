from os import path
import configparser


def settings(section=None, option=None):
    """Get a value from the config file.

    If none exist, create a option with the default value of 720x480
    """

    path_to_ini = base_path(r'settings.ini')

    config = configparser.ConfigParser()

    config.read(path_to_ini)

    try:
        return config[section][option]
    except KeyError:
        default_size = '720x720'

        with open(path_to_ini, 'w') as configfile:
            write_config(config, configfile, default_size)

        return config[section][option]


def write_config(config, file, size):
    """Write options in the config file."""
    if not config.has_section('Interface'):
        config.add_section('Interface')

    config['Interface'] = {
        'size': size
    }

    config.write(file)


def asset(relpath=""):
    """Generate an asset path."""
    asset_path = base_path(f'resources/{relpath}')

    assert path.isfile(asset_path), "The path doesn't indicate a file"
    assert path.exists(asset_path), "Given file doesn't exists."

    return path.realpath(f'resources/{relpath}')


def base_path(relpath=""):
    """Get the path to the base of the project."""
    return path.realpath(f'{relpath}')


def get_screen_size():
    """Retrieve the last registered screen size in the settings file."""
    size = [int(values) for values in settings('Interface', option='size').split('x')]

    return tuple(size)
