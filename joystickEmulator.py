import pygame

# GLOBAL VARIABLES
JOYSTICK_COLOR = (150, 150, 150)
COLOR = (0, 0, 0)
BORDER_COLOR = (255, 255, 255)
TRANSPARENT_COLOR = (0, 0, 0)
BORDER_SIZE = 0.1  # Percent
JOYSTICK_RATIO = 0.2


# Object class
class JoystickVisual(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0)):
        super().__init__()
        self.sourceImage = pygame.Surface([size, size])
        # self.sourceImage.fill(BORDER_COLOR)
        self.sourceImage.set_colorkey(TRANSPARENT_COLOR)

        pygame.draw.circle(self.sourceImage, BORDER_COLOR, (size / 2, size / 2), size / 2)
        pygame.draw.circle(self.sourceImage, COLOR, (size / 2, size / 2), size / 2 * (1 - BORDER_SIZE))

        self.image = self.sourceImage
        self.rect = self.sourceImage.get_rect()
        self.size = size
        self.rect.center = pos
        self.input = (0, 0)

    def setPosition(self, cords):
        self.input = cords

    def update(self):
        self.image = self.sourceImage
        pygame.draw.circle(self.sourceImage, BORDER_COLOR, (self.size / 2 + self.input[0], self.size / 2 + self.input[1]), self.size * JOYSTICK_RATIO)
        pygame.draw.circle(self.sourceImage, JOYSTICK_COLOR, (self.size / 2 + self.input[0], self.size / 2 + self.input[1]), self.size * JOYSTICK_RATIO * (1 - BORDER_SIZE))
