import pygame
from joystickEmulator import JoystickVisual
from swerveKinematics import SwerveKinematics
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

kinematics = SwerveKinematics([
    [-1, 1],
    [-1, -1],
    [1, 1],
    [1, -1]
])

swerveGroup.add(leftTopModule)
swerveGroup.add(leftBottomModule)
swerveGroup.add(rightTopModule)
swerveGroup.add(rightBottomModule)

leftJoystick = JoystickVisual(200, (200, 800))
rightJoystick = JoystickVisual(200, (800, 800))

allSpriteGroup.add(leftJoystick)
allSpriteGroup.add(rightJoystick)
allSpriteGroup.add(swerveGroup)

driverController = pygame.joystick.Joystick(
    0) if pygame.joystick.get_count() > 0 else None

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
        rightJoystick.set_position(
            (turn * 30, driverController.get_axis(3) * 30))

    states = kinematics.calculate_module_states(-strafe, forward, turn)

    kinematics.scale_speeds(states)

    leftTopModule.set_speed(states[0][1], states[0][0])
    leftBottomModule.set_speed(states[1][1], states[1][0])
    rightTopModule.set_speed(states[2][1], states[2][0])
    rightBottomModule.set_speed(states[3][1], states[3][0])

    # Draw a solid blue circle in the center
    pygame.draw.rect(screen, (200, 200, 200), (300, 300, 400, 400))
    allSpriteGroup.update()
    allSpriteGroup.draw(screen)
    # Flip the display
    clock.tick(60)
    pygame.display.flip()

# Done! Time to quit.
pygame.joystick.quit()
pygame.quit()
