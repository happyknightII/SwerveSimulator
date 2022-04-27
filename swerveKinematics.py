import numpy as np
import math


def getRotation(x, y):
    magnitude = math.hypot(x, y)
    if magnitude > 1e-6:
        sin = y / magnitude
        cos = x / magnitude
    else:
        sin = 0.0
        cos = 1.0
    value = math.atan2(sin, cos)
    return value * 180 / math.pi


class SwerveKinematics:
    def __init__(self, positions):
        self.inv_kinematics = self.get_inv_kinematics(positions)

    def get_inv_kinematics(self, positions):
        matrix = []
        for i in positions:
            matrix.append([1, 0, -i[0]])
            matrix.append([0, 1,  i[1]])

        return np.matrix(matrix)

    def calculate_module_states(self, chassis_x, chassis_y, chassis_omega):
        chassis_state = np.matrix([[chassis_x], [chassis_y], [chassis_omega]])
        module_states = np.matmul(self.inv_kinematics, chassis_state)

        useful_states = []
        for i in range(len(module_states) // 2):
            x = module_states[i * 2 + 0][0]  # x component of swerve state
            y = module_states[i * 2 + 1][0]  # y component of swerve state
            speed = math.hypot(x, y)  # magnitude of swerve spin (speed)
            angle = getRotation(x, y)  # angle scaled to degrees
            useful_states.append([speed, angle])

        return useful_states

    def scale_speeds(self, speeds):
        max_speed = 0
        for i in speeds:
            if i[0] > max_speed:
                max_speed = i[0]

        if max_speed > 1:
            for i in speeds:
                i[0] /= max_speed
