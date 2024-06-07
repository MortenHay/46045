import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from machine_model import RollingFollower


# Define control system parameters
# TODO Q3: Play around with the control system parameters
Kp = 0.5
Ki = 1.5
Kd = 0.002

# Define test parameters
STEP_UP_TIME = 5
STEP_DOWN_TIME = 40
MAX_T = 70
DT = 0.01
NUM_TIMESTEPS = int(MAX_T/DT + 1)
NOMINAL_SPEED = 40
DOWNREGULATION_SPEED = 80

# Define timesteps and the target signal.
ts = np.linspace(0, MAX_T, NUM_TIMESTEPS)
target_signal = NOMINAL_SPEED - (NOMINAL_SPEED - DOWNREGULATION_SPEED) * ((ts > 5).astype(float) - (ts > 30).astype(float))
responder = RollingFollower(machinestate=NOMINAL_SPEED, k=0.01, Kp=Kp, Ki=Ki, Kd=Kd, dt=DT, sigma=0.5*np.sqrt(DT))
response = [responder.update(x) for x in target_signal]
machine_state, pid_output = map(list, zip(*response))

# plt.ion()
# plt.plot(ts, response)
# plt.plot(ts, target_signal)

df = pd.DataFrame.from_dict({'time': ts, 'target': target_signal, 'machine_state': machine_state, 'pid_output': pid_output})
df.to_csv(f"updated_unit_characterization_{NOMINAL_SPEED}_to_{DOWNREGULATION_SPEED}.csv", index=False)
