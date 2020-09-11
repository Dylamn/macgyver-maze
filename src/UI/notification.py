import pygame.font
import time

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Notification:
    """Send text notification to the screen."""

    # The Height spacing between the text lines..
    SPACING_H = 10

    # Margin of the background.
    MARGIN_BACKGROUND_TEXT = 20

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
            'You craft the syringe.',
            'You are now able to beat the guardian.'
        ],
        "loose": [
            'You loose.',
            'Try again !'
        ],
        "win": [
            'You win.',
            ' Great job !'
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
        self.running_time = None
        self.end = None

    def render(self, screen):
        """Display the text notification if the notification display is active."""

        if self.end is not None:
            # Current time. We'll use this value to check if the notification is expired.
            self.running_time = time.time()

            if self.running_time >= self.end:  # Notification is expired, we'll erase it.
                self.erase()

        if (self.end is not None and self.__is_active) or self.__is_active:
            if self.__is_active:
                # Retrieve the size of the screen
                screen_height, screen_width = screen.get_height(), screen.get_width()

                # Get the sentences which will be displayed.
                self.line1 = self.font.render(self.sentences.get(self.__selected_sentence)[0], True, WHITE)
                self.line2 = self.font.render(self.sentences.get(self.__selected_sentence)[1], True, WHITE)

                # Retrieve the rect of each text surfaces.
                self.rect_line1 = self.line1.get_rect()
                self.rect_line2 = self.line2.get_rect()

                # Center the surfaces on the X axis.
                offset_x_line1 = (screen_width - self.rect_line1.width) / 2
                offset_x_line2 = (screen_width - self.rect_line2.width) / 2

                # Calculate position of the first text line.
                margin_top = (screen_height - (self.rect_line1.height + self.SPACING_H + self.rect_line2.height)) / 2
                offset_y_line1 = margin_top

                # Calculate the position of the second text line with the first one.
                offset_y_line2 = screen_height - margin_top - self.rect_line2.height

                background_width = self.line2.get_width() \
                    if self.line2.get_width() > self.line1.get_width() else self.line1.get_width()

                # Add a bit of margin
                background_width += self.MARGIN_BACKGROUND_TEXT
                background_height = self.rect_line1.height + self.rect_line2.height + self.MARGIN_BACKGROUND_TEXT

                background_x = int((screen.get_width() - background_width) / 2)

                background = pygame.Surface((background_width, background_height))
                background.set_alpha(128)
                background.fill((0, 0, 0))

                # Finally, draw text on the screen at the calculated coordinates.
                screen.blit(background, (background_x, offset_y_line1 - (self.MARGIN_BACKGROUND_TEXT / 2)))
                screen.blit(self.line1, (offset_x_line1, offset_y_line1))
                screen.blit(self.line2, (offset_x_line2, offset_y_line2))

    def active(self, slug_sentence: str):
        """Activate the display of the nofication."""
        self.__is_active = True
        self.__selected_sentence = slug_sentence

        return self

    def set_timer(self, duration: int):
        """Set a timer for the notification."""

        # We use the current epoch and add a number of seconds.
        self.end = time.time() + duration

    def erase(self):
        """Desactivate the display of the notification."""
        if self.end is not None:
            self.running_time = None
            self.end = None

        self.__is_active = False
        self.__selected_sentence = ""
