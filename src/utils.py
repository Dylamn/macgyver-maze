from os import path
import configparser
from pathlib import Path


def get_config():
    """Get the config file."""
    path_to_ini = base_path(r'settings.ini')

    config = configparser.ConfigParser()

    config.read(path_to_ini)

    return config


def settings(section=None, option=None):
    """Get a value from the config file.

    If none exist, create a new file with default values.
    """

    # Initialize the variable which will contain the retrieved/created value.
    value = None

    config = get_config()

    try:
        value = config[section][option]
    except KeyError:
        default_size = '720x720'

        write_config(config, section='Interface', key='size', value=default_size)

        value = config[section][option]
    finally:

        if is_float(value):
            return config[section].getfloat(option)
        else:
            return value


def write_config(config=None, section=None, key=None, value=None, file_path=r'settings.ini'):
    """Write options in the config file."""

    if config is None:
        config = get_config()

    with open(file_path, 'w') as configfile:
        if not config.has_section(section):
            config.add_section(section)

        # Retrieve all options from the section.
        options = config_section_map(config, section)
        # Change the value of the specified key
        options[key] = value

        # Rewrite the section
        config[section] = options

        # Save data in the file.
        config.write(configfile, space_around_delimiters=False)


def config_section_map(config, section):
    """Map a section of the config file to a dictionary"""
    dict_section = {}
    options = config.options(section)

    for option in options:
        try:
            dict_section[option] = config.get(section, option)

        except configparser.NoOptionError:
            print("exception on %s!" % option)
            dict_section[option] = None

    return dict_section


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


def get_screen_width():
    """Retrieve the width of the screen from the settings file."""
    return get_screen_size()[0]


def get_screen_height():
    """Retrieve the height of the screen from the settings file."""
    return get_screen_size()[1]


def scale_position(pos: tuple, scale: tuple):
    """Returns the mapped position of the maze coordinates for the screen."""
    return tuple(point * scaling for point, scaling in zip(pos, scale))


def calculate_scale(screen_size: tuple):
    """Calculate the scaling for the given screen size."""
    return tuple(round(num / 15) for num in screen_size)


def is_float(value):
    """Verify if the given value is a float/number"""
    try:
        float(value)
        return True

    except ValueError:
        return False
