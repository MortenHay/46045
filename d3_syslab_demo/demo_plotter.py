import pandas as pd
import json
import matplotlib.pyplot as plt
import os
from datetime import timedelta

## Read the measurements data file ##
DATA_MEAS_DIR = 'data\measurements'
# Always plot latest datafile - replace [-1] with another index if you want to plot a specific file.
MEAS_LOG_FILE = sorted(os.listdir(DATA_MEAS_DIR))[-1]

# Store each dictionary of the measurements json in a list
with open(os.path.join(DATA_MEAS_DIR, MEAS_LOG_FILE)) as f:
    meas_data = [json.loads(line) for line in f]

# Use setpoint logger (only necessary for part two of the exercise "collecting fresh data")
use_setpoint_log = False


## Read the setpoints data file ##
if use_setpoint_log:
    DATA_SP_DIR = 'data\setpoints'
    # Always plot latest datafile
    SP_LOG_FILE = sorted(os.listdir(DATA_SP_DIR))[-1]

    # Store each dictionary of the setpoints json in a list
    with open(os.path.join(DATA_SP_DIR, SP_LOG_FILE)) as f:
        sp_data = [json.loads(line) for line in f]

    # Merge measurements and setpoints in one list
    data = meas_data + sp_data

else:
    data = meas_data


# Construct a dataframe and pivot it to obtain a dataframe with a column per unit, and a row per timestamp.
df = pd.DataFrame.from_records(data)
df_pivot = df.pivot_table(values='value', columns='unit', index='time')


# Plot the data. Note, that the data will mostly not be plotted with lines.
plt.ion()  # Turn interactive mode on
plt.figure()
ax1 = plt.subplot(211)  # Make two separate figures
ax2 = plt.subplot(212)
df_pivot[[c for c in df_pivot.columns if "_p" in c]].plot(marker='.', ax=ax1, linewidth=3)
df_pivot[[c for c in df_pivot.columns if "_q" in c]].plot(marker='.', ax=ax2, linewidth=3)
plt.show(block=True)

#%%
## TODO Q1: Your code here
plt.figure(figsize=(10, 6))
plt.plot(df_pivot.iloc[:, ::2],df_pivot.iloc[:, 1::2], marker='.', linewidth=3)
plt.legend(df_pivot.columns[::2])
plt.xlabel('P')
plt.ylabel('Q')
plt.title('P vs Q')
plt.show()

#%%
## TODO Q2:
# Convert time column (index) of df_pivot to datetime
# TODO Your code here
# Hint1: You can use pandas to_numeric() to prepare the index for pandas to_datetime function
# Hint2: Remember to define the unit within pandas to_datetime function

df_pivot.index = pd.to_datetime(df_pivot.index, unit='s')

#%%
# Resample the data
# TODO Your code here
df_resampled = df_pivot.resample('s').mean()

# Interpolate the measurements
# TODO Your code here
# Hint: For part two of the exercise ("collecting fresh data") the nan rows after a setpoint
# in the recorded step function should be filled with the value of the setpoint until the row of the next setpoint is reached
# You can use the df.fillna(method="ffill") function for that purpose. However, the measurements should still be interpolated!


#%%
# Plot the resampled data
# TODO Your code here
plt.ion()  # Turn interactive mode on
plt.figure()
ax1 = plt.subplot(211)  # Make two separate figures
ax2 = plt.subplot(212)
df_resampled[[c for c in df_resampled.columns if "_p" in c]].plot(marker='.', ax=ax1, linewidth=3)
df_resampled[[c for c in df_resampled.columns if "_q" in c]].plot(marker='.', ax=ax2, linewidth=3)
plt.show(block=True)


#%%
## TODO Q3: Your code here




## TODO Q4: Your code here



## Part two: "Collecting fresh data"

# Hint 1: You can build up on the "read_and_plot_data.py" from day 2
# Hint 2: Yoy may want to store your response metric functions from day 2 in the "util.py" and import all of them with
# "from util import *"

if use_setpoint_log:

    # Add a column to df_pivot containing the reference/target signal
    # TODO your code here

    # Loop over all steps and extract T_1, T_2 and the step size
    results = {}

    for idx in range(0, len(sp_data)-1):
        label = f"Step_{sp_data[idx]['value']}kW"

        # Extract T_1 and T_2 from the setpoint JSON
        # TODO your code here


        # Change timestamp format
        T_1 = pd.to_datetime(pd.to_numeric(T_1), unit="s").round("0.1S")
        T_2 = pd.to_datetime(pd.to_numeric(T_2), unit="s").round("0.1S")

        # To ensure we are not considering values of the next load step
        T_2 = T_2 - timedelta(seconds=0.2)


        # define measured output y and target setpoint r
        # TODO your code here

        # Derive step direction from the setpoint data
        if ...:  # TODO your code here
            Positive_step = True
        else:
            Positive_step = False

        # Collect response metrics results
        results[label] = {
            # TODO your code here
        }

    pd.DataFrame.from_dict(results).plot(kind='bar')
    plt.title("Metrics")
    plt.tight_layout()
    plt.savefig('data/test_metrics'+MEAS_LOG_FILE[-10:]+'.png')
    plt.show(block=True)


