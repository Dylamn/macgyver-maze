from src.app import App
from src.game import Game
from src.utils import *
import pygame


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


if __name__ == '__main__':
    main()
