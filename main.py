from src.app import App
from src.utils import *
import pygame


def main():
    """Bootstrap the game and the pygame module."""

    # Initialize pygame
    pygame.init()

    # Default size of the screen as a tuple.
    window_size = get_screen_size()

    # Initialize the game.
    app = App(size=window_size)

    # Then execute the game loop.
    app.execute()


if __name__ == '__main__':
    main()
