from os import path

from src.utils import get_screen_size, write_default_config
import pygame
import shutil
from src.app import App


def main():
    """Bootstrap the game and the pygame module."""

    # Initialize pygame
    pygame.init()

    # Default size of the screen as a tuple.
    window_size = get_screen_size()

    # Initialize the application.
    app = App(size=window_size)

    # Execute the application.
    app.execute()


def check_config_file():
    """Checks if the config file exist or not."""
    if path.exists(r'settings.ini'):
        return True
    else:
        return False


def create_config_file():
    """Create the config file which will be used by the game."""
    try:
        shutil.copy(r'settings.ini.example', r'settings.ini')
    except FileNotFoundError:
        write_default_config()


if __name__ == '__main__':
    # Check if the config file exists.
    if not check_config_file():
        # Create the config file.
        create_config_file()

    # Launch the main program.
    main()
