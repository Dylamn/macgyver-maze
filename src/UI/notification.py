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

    # A part of the text which is dynamic.
    # This part will replace by the @ character in the sentences.
    __dynamic_part: str = None

    # All values that a notification can display.
    sentences = {
        "volume": [
            'Volume : @'
        ],
        "craft-available": [
            'You can craft the syringe !',
            'Press C to craft.'
        ],
        "missing-items": [
            'Items for craft are missing.',
        ],
        "crafted": [
            'You crafted the syringe.',
            'You can now beat the guardian !'
        ],
        "loose": [
            'You loose.',
            'Try again !'
        ],
        "win": [
            'You win.',
            'Great job !'
        ],
    }

    @property
    def is_active(self) -> bool:
        """Get the boolean which determines if a notification is active or not."""
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        """Setter for __is_active attribute."""
        self.__is_active = value

    def __init__(self, size=50):
        self.font = pygame.font.SysFont(None, size)
        self.container = None  # Container for text
        # Font surface
        self.line1 = None
        self.line2 = None
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

        if (self.end is not None and self.is_active) or self.is_active:
            # Retrieve the size of the screen
            screen_height, screen_width = screen.get_height(), screen.get_width()

            # Get the sentences which will be displayed.
            sentence_1 = self.sentences.get(self.__selected_sentence)[0]
            if sentence_1.find('@'):
                sentence_1 = sentence_1.replace('@', self.__dynamic_part)

            self.line1 = self.font.render(sentence_1, True, WHITE)

            # Retrieve the rect of each text surfaces.
            self.rect_line1 = self.line1.get_rect()

            # Calculate position of the first text line.
            margin_top = (screen_height - (self.rect_line1.height * 2 + self.SPACING_H)) / 2
            offset_x_line1 = (screen_width - self.rect_line1.width) / 2
            offset_y_line1 = margin_top

            # Initialize vars position of line 2
            offset_x_line2 = None
            offset_y_line2 = None

            background_width = self.line1.get_width()

            # Add a bit of margin
            background_width += self.MARGIN_BACKGROUND_TEXT
            background_height = self.rect_line1.height + self.MARGIN_BACKGROUND_TEXT

            # The notification has a second line.
            if len(self.sentences.get(self.__selected_sentence)) == 2:
                self.line2 = self.font.render(self.sentences.get(self.__selected_sentence)[1], True, WHITE)
                self.rect_line2 = self.line2.get_rect()
                offset_x_line2 = (screen_width - self.rect_line2.width) / 2
                # Calculate the position of the second text line with the first one.
                offset_y_line2 = screen_height - margin_top - self.rect_line2.height

                # The background width must have the width of the longest line.
                background_width = max(self.line1.get_width(), self.line2.get_width())
                # Add the height of the line2 to the background height.
                background_height += self.rect_line2.height

            background_x = int((screen.get_width() - background_width) / 2)

            # Create the background surface and change the alpha.
            background = pygame.Surface((background_width, background_height))
            background.set_alpha(128)
            background.fill((0, 0, 0))

            # Finally, draw text on the screen at the calculated coordinates.
            screen.blit(background, (background_x, offset_y_line1 - (self.MARGIN_BACKGROUND_TEXT / 2)))
            screen.blit(self.line1, (offset_x_line1, offset_y_line1))

            if self.line2 is not None:
                screen.blit(self.line2, (offset_x_line2, offset_y_line2))

    def active(self, slug_sentence: str, dynamic_part=None):
        """Activate the display of the nofication."""

        if self.is_active:
            # Erase the current notification
            self.erase()

        self.is_active = True
        self.__selected_sentence = slug_sentence
        self.__dynamic_part = str(dynamic_part)

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

        self.is_active = False

        self.reset_text()

    def reset_text(self):
        """Reset variables used for text"""
        self.line1 = None
        self.line2 = None

        self.rect_line1 = None
        self.rect_line2 = None

        self.__selected_sentence = ""
        self.__dynamic_part = ""

