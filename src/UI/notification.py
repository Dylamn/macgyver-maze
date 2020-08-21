import pygame.font

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Notification:
    """Send text notification to the screen."""

    sentences = {
        "craft-available": 'You can craft the syringue !'
    }

    @property
    def is_running(self) -> bool:
        return self.image is not None

    def __init__(self, size=50):
        self.font = pygame.font.SysFont(None, size)
        self.image = None

    def text(self, screen, slug_sentence):
        self.image = self.font.render(self.sentences.get(slug_sentence, None), True, BLACK)

        screen.blit(self.image, (200, 200))

    def erase(self):
        self.image = None
