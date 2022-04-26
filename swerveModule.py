import math

import pygame

# GLOBAL VARIABLES
COLOR = (66, 139, 255)
BORDER_COLOR = (250, 250, 255)
TRANSPARENT_COLOR = (0, 0, 0)
BORDER_SIZE = 0.04  # Percent
ASPECT_RATIO = 0.35

KP_ADJUST_ROTATION = 0.1
MAX_TURN_SPEED = 1


# Object class
class SwerveModule(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0)):
        super().__init__()
        self.angle = 0
        self.sourceImage = pygame.Surface([size * ASPECT_RATIO, size])
        self.sourceImage.fill(BORDER_COLOR)
        self.sourceImage.set_colorkey(TRANSPARENT_COLOR)

        pygame.draw.rect(self.sourceImage,
                         COLOR,
                         pygame.Rect(size * BORDER_SIZE,
                                     size * BORDER_SIZE,
                                     size * (ASPECT_RATIO - 2 * BORDER_SIZE),
                                     size * (1 - 2 * BORDER_SIZE)))
        self.image = self.sourceImage
        self.rect = self.sourceImage.get_rect()
        self.position = pos
        self.rect.center = pos

    @staticmethod
    def closest_angle(target, current):
        error = target - current
        if abs(error) > 180:
            error = -math.copysign(1, error) * 360 + error
        return error

    def rotate(self, angle):
        # math stuff
        error = self.closest_angle(angle, self.angle)
        flipped_error = self.closest_angle(angle, self.angle + 180)

        if abs(error) > abs(flipped_error):
            velocity = KP_ADJUST_ROTATION * error
        else:
            velocity = KP_ADJUST_ROTATION * flipped_error

        # Simulation stuffs
        self.angle %= 360
        if abs(velocity) > MAX_TURN_SPEED:
            velocity = math.copysign(1, error) * MAX_TURN_SPEED

        self.angle += velocity

    def update(self):
        self.image = pygame.transform.rotate(self.sourceImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
