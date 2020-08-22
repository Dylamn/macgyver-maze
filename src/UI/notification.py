import pygame.font
import time

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Notification:
    """Send text notification to the screen."""

    # Determines if a notification is active.
    __is_active: bool = False

    # Value of the current notification.
    __selected_sentence: str = None

    # All values that a notification can display.
    sentences = {
        "craft-available": 'You can craft the syringe !',
        "missing-items": 'Items for craft are missing.',
        "crafted": 'You craft a syringe.',
        "loose": 'You loose. Sorry !',
        "win": 'You win. Great job !',
    }

    @property
    def is_active(self) -> bool:
        return self.__is_active

    def __init__(self, size=50):
        self.font = pygame.font.SysFont(None, size)
        self.text = None  # Font surface
        self.rect = None  # The rect of the text.

        # Timer
        self.start = None
        self.end = None

    def render(self, screen):
        """Display the text notification if the notification display is active."""

        # if not self.start >= self.end:
        if self.__is_active:
            self.text = self.font.render(self.sentences.get(self.__selected_sentence, "Default"), True, WHITE)
            self.rect = self.text.get_rect()

            screen.blit(self.text, (0, 0))

    def active(self, slug_sentence: str):
        """Activate the display of the nofication."""
        self.__is_active = True
        self.__selected_sentence = slug_sentence

        # Use timer for notification
        # self.start = time.time()
        # self.end = self.start + 3

    def erase(self):
        """Desactivate the display of the notification."""
        self.__is_active = False
        self.__selected_sentence = ""
