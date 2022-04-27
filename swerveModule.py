import math

import pygame

# GLOBAL VARIABLES
COLOR = (66, 139, 255)
BORDER_COLOR = (250, 250, 255)
TRANSPARENT_COLOR = (0, 0, 0)
BORDER_SIZE = 0.04  # Percent
ASPECT_RATIO = 0.35
WHITE = (0, 0, 0)
RED = (255, 0, 0)


KP_ADJUST_ROTATION = 0.1
MAX_TURN_SPEED = 15


# Object class
class SwerveModule(pygame.sprite.Sprite):
    def __init__(self, size, pos=(0, 0)):
        super().__init__()
        self.size = size
        self.pos = pos
        self.angle = 0
        self.sourceImage = pygame.Surface([size * ASPECT_RATIO, size])
        self.sourceImage.fill(BORDER_COLOR)
        self.sourceImage.set_colorkey((0, 0, 1))

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
        self.isReversed = False

    @staticmethod
    def closest_angle(target, current):
        error = target - current
        if abs(error) > 180:
            error = -math.copysign(1, error) * 360 + error
        return error

    def set_speed(self, angle, speed):

        # speed = speed / 0.3 * 250

        # math stuff
        error = self.closest_angle(angle, self.angle)
        flipped_error = self.closest_angle(angle, self.angle + 180)

        if abs(error) > abs(flipped_error):
            velocity = KP_ADJUST_ROTATION * flipped_error
            self.isReversed = True
        else:
            velocity = KP_ADJUST_ROTATION * error
            self.isReversed = False

        # Simulation stuffs
        self.angle %= 360
        if abs(velocity) > MAX_TURN_SPEED:
            velocity = math.copysign(1, velocity) * MAX_TURN_SPEED

        self.angle += velocity
        self.speed = speed

    def update(self):
        self.image = pygame.transform.rotate(self.sourceImage, self.angle+90)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        col = self.speed * 255
        self.sourceImage.fill((col, 200, 200))
        pygame.draw.circle(
            self.sourceImage,
            RED if self.isReversed else WHITE,
            (self.size / 2 *
             ASPECT_RATIO, self.size / 8),
            self.size / 8)
