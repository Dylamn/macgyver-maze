import pygame.font

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Notification:
    """Send text notification to the screen."""

    # The Height spacing between the text lines..
    SPACING_H = 10

    # Determines if a notification is active.
    __is_active: bool = False

    # Value of the current notification.
    __selected_sentence: str = None

    # All values that a notification can display.
    sentences = {
        "craft-available": [
            'You can craft the syringe !',
            'Press C to craft.'
        ],
        "missing-items": [
            'Items for craft are missing.',
            ''
        ],
        "crafted": [
            'You craft a syringe.',
            ''
        ],
        "loose": [
            'You loose. Sorry !',
            ''
        ],
        "win": [
            'You win. Great job !',
            ''
        ],
    }

    @property
    def is_active(self) -> bool:
        return self.__is_active

    def __init__(self, size=50):
        self.font = pygame.font.SysFont(None, size)
        self.container = None  # Container for text
        self.line1 = None  # Font surface
        self.line2 = None  # Font surface
        self.rect_line1 = None  # The rect of the text.
        self.rect_line2 = None  # The rect of the text.

        # Timer
        self.start = None
        self.end = None

    def render(self, screen):
        """Display the text notification if the notification display is active."""

        # if not self.start >= self.end:
        if self.__is_active:
            self.line1 = self.font.render(self.sentences.get(self.__selected_sentence, [""])[0], True, WHITE)
            self.line2 = self.font.render(self.sentences.get(self.__selected_sentence)[1], True, WHITE)

            self.rect_line1 = self.line1.get_rect()
            self.rect_line2 = self.line2.get_rect()

            offset_x_line1 = (screen.get_width() - self.rect_line1.width) / 2
            offset_x_line2 = (screen.get_width() - self.rect_line2.width) / 2

            margin_h = (screen.get_height() - (self.rect_line1.height + self.SPACING_H + self.rect_line2.height)) / 2
            offset_y_0 = margin_h
            offset_y_1 = screen.get_height() - margin_h - self.rect_line2.height

            screen.blit(self.line1, (offset_x_line1, offset_y_0))
            screen.blit(self.line2, (offset_x_line2, offset_y_1))

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
