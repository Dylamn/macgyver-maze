import pygame.freetype

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Notification:
    """Send text notification to the screen."""

    sentences = {
        "craft-available": 'You can craft the syringe !',
        "win": 'You win'
    }

    @property
    def is_running(self) -> bool:
        return self.image is not None

    def __init__(self, size=50):
        self.font = pygame.freetype.SysFont(None, size)
        self.image = None

    def text(self, screen, slug_sentence):
        # self.image = self.font.render(self.sentences.get(slug_sentence, None), True, WHITE)

        self.font.render_to(screen, (200, 200), self.sentences.get(slug_sentence, None), WHITE)

    def erase(self):
        self.image = None
