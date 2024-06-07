from dataclasses import dataclass
import numpy as np

@dataclass
class RollingFollower:
    machinestate: float = 1.0
    k: float = 0.1
    sigma: float = 0.005

    integral: float = 0.0
    error: float = 0.0
    error_prev: float = 0.0
    output: float = 0.0

    Kp: float = 0.1
    Ki: float = 0.1
    Kd: float = 0.1
    dt: float = 0.01

    def update(self, x_new):
        self.error = x_new - self.machinestate
        self.integral += self.error*self.dt
        derivative = (self.error - self.error_prev)/self.dt
        self.output = self.Kp * self.error + self.Ki * self.integral + self.Kd * derivative
        # Update
        self.error_prev = self.error
        self.machinestate += self.k * (1 + 0.7 * np.sin(self.machinestate/10)) * self.output + self.sigma * np.random.normal()

        return self.machinestate, self.output