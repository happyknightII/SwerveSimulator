# Simple pygame program

# Import and initialize the pygame library
import math

import pygame
from joystickEmulator import JoystickVisual
from swerveModule import SwerveModule

pygame.init()
pygame.joystick.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])

# Run until the user asks to quit
clock = pygame.time.Clock()
running = True


allSpriteGroup = pygame.sprite.Group()
swerveGroup = pygame.sprite.Group()

leftTopModule = SwerveModule(100, (350, 350))
leftBottomModule = SwerveModule(100, (350, 350 + 300))
rightTopModule = SwerveModule(100, (350 + 300, 350))
rightBottomModule = SwerveModule(100, (350 + 300, 350 + 300))

swerveGroup.add(leftTopModule)
swerveGroup.add(leftBottomModule)
swerveGroup.add(rightTopModule)
swerveGroup.add(rightBottomModule)

leftJoystick = JoystickVisual(200, (200, 800))
rightJoystick = JoystickVisual(200, (800, 800))

allSpriteGroup.add(leftJoystick)
allSpriteGroup.add(rightJoystick)
allSpriteGroup.add(swerveGroup)

driverController = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None


def turn_in_place():
    leftTopModule.rotate(135)
    leftBottomModule.rotate(45)
    rightTopModule.rotate(45)
    rightBottomModule.rotate(135)


while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))
    forward = 0
    strafe = 0
    turn = 0

    if driverController and driverController.get_init():
        forward = driverController.get_axis(1)
        strafe = driverController.get_axis(0)
        turn = driverController.get_axis(2)
        leftJoystick.set_position((strafe * 30, forward * 30))
        rightJoystick.set_position((turn * 30, driverController.get_axis(3) * 30))

    globalAngle = math.degrees(math.atan(forward / strafe)) if strafe == 0 else 0
    magnitude = math.sqrt(forward ** 2 + strafe ** 2)

    # swerve calculations
    if magnitude > 0:
        leftTopModule.rotate(globalAngle)
        leftBottomModule.rotate(globalAngle)
        rightTopModule.rotate(globalAngle)
        rightBottomModule.rotate(globalAngle)
    else:
        turn_in_place()

    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    pygame.draw.rect(screen, (200, 200, 200), (300, 300, 400, 400))
    allSpriteGroup.update()
    allSpriteGroup.draw(screen)
    # Flip the display
    clock.tick(60)
    pygame.display.flip()

# Done! Time to quit.
pygame.joystick.quit()
pygame.quit()
