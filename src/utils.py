from os import path
import configparser
from pathlib import Path


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
    asset_path = base_path(f'assets/{relpath}')

    assert path.isfile(asset_path), f"The path doesn't indicate a file. Given: {asset_path}"
    assert path.exists(asset_path), "Given file doesn't exists."

    return str(asset_path)


def base_path(relpath=""):
    """Get the path to the base of the project.

    :param relpath relative path to a file, dir...
    """
    project_path = Path(path.realpath(''))

    # Jump to the parent directory as long as it's not the project directory (macgyver-maze).
    while not project_path.name.endswith('macgyver-maze'):
        project_path = project_path.parent

    return project_path.joinpath(relpath)


def get_screen_size():
    """Retrieve the last registered screen size in the settings file."""
    size = [int(values) for values in settings('Interface', option='size').split('x')]

    return tuple(size)


def scale_position(pos: tuple, scale: tuple):
    """Returns the mapped position of the maze coordinates for the screen."""
    return tuple(point * scaling for point, scaling in zip(pos, scale))


def calculate_scale(screen_size: tuple):
    """Calculate the scaling for the given screen size"""
    return tuple(round(num / 15) for num in screen_size)
