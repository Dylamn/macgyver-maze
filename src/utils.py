from os import path
import configparser


def settings(section=None, key=None):
    """Get a value from the settings.ini file"""
    config = configparser.ConfigParser()

    config.read(base_path(r'settings.ini'))

    return config[section][key]


def asset(relpath=""):
    """Generate an asset path."""
    asset_path = base_path(f'resources/{relpath}')

    assert path.isfile(asset_path), "The path doesn't indicate a file"
    assert path.exists(asset_path), "Given file doesn't exists."

    return path.realpath(f'../resources/{relpath}')


def base_path(relpath=""):
    """Get the path to the base of the project."""
    return path.realpath(f'../{relpath}')


def get_screen_size():
    """Retrieve the last registered screen size in the settings file."""
    size = [int(values) for values in settings('Interface', key='size').split('x')]

    return tuple(size)
