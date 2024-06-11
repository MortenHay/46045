# %%
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import timedelta
import syslab
from util import *

try:
    ## Read the measurements data file ##
    DATA_MEAS_DIR = "data\measurements"
    # Always plot latest datafile - replace [-1] with another index if you want to plot a specific file.
    MEAS_LOG_FILE = sorted(os.listdir(DATA_MEAS_DIR))[-1]
except FileNotFoundError:
    ## Read the measurements data file ##
    DATA_MEAS_DIR = "data/measurements"
    # Always plot latest datafile - replace [-1] with another index if you want to plot a specific file.
    MEAS_LOG_FILE = sorted(os.listdir(DATA_MEAS_DIR))[-1]

# Store each dictionary of the measurements json in a list
with open(os.path.join(DATA_MEAS_DIR, MEAS_LOG_FILE)) as f:
    meas_data = [json.loads(line) for line in f]

# Use setpoint logger (only necessary for part two of the exercise "collecting fresh data")
use_setpoint_log = True


## Read the setpoints data file ##
if use_setpoint_log:
    try:
        DATA_SP_DIR = "data\setpoints"
        # Always plot latest datafile
        SP_LOG_FILE = sorted(os.listdir(DATA_SP_DIR))[-1]
    except FileNotFoundError:
        DATA_SP_DIR = "data/setpoints"
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
df_pivot = df.pivot_table(values="value", columns="unit", index="time")


# Plot the data. Note, that the data will mostly not be plotted with lines.
plt.ion()  # Turn interactive mode on
plt.figure()
ax1 = plt.subplot(211)  # Make two separate figures
ax2 = plt.subplot(212)
df_pivot[[c for c in df_pivot.columns if "_p" in c]].plot(
    marker=".", ax=ax1, linewidth=3
)
df_pivot[[c for c in df_pivot.columns if "_q" in c]].plot(
    marker=".", ax=ax2, linewidth=3
)
plt.show(block=True)

# %%
## TODO Q1: Your code here
plt.figure(figsize=(10, 6))
for x in df_pivot.columns:
    if "_p" in x:
        x = x.replace("_p", "")
        plt.plot(
            df_pivot[x + "_p"], df_pivot[x + "_q"], label=x, marker=".", linewidth=3
        )
        print(x)
plt.legend()
plt.xlabel("P")
plt.ylabel("Q")
plt.title("P vs Q")
plt.show()
# %%
## TODO Q2:
# Convert time column (index) of df_pivot to datetime
# TODO Your code here
# Hint1: You can use pandas to_numeric() to prepare the index for pandas to_datetime function
# Hint2: Remember to define the unit within pandas to_datetime function

df_pivot.index = pd.to_datetime(df_pivot.index, unit="s")

# Resample the data
# TODO Your code here
df_resampled = df_pivot.resample("s").mean()

# Interpolate the measurements
# TODO Your code here
# Hint: For part two of the exercise ("collecting fresh data") the nan rows after a setpoint
# in the recorded step function should be filled with the value of the setpoint until the row of the next setpoint is reached
# You can use the df.fillna(method="ffill") function for that purpose. However, the measurements should still be interpolated!
df_resampled = df_resampled.interpolate()

# Plot the resampled data
# TODO Your code here
plt.figure(figsize=(10, 6))
plt.plot(df_resampled.index, df_resampled, marker=".", linewidth=3)
plt.legend(df_resampled.columns)
plt.show()


# %%
ncol = 3
nrow = 3
fig, axs = plt.subplots(nrows=nrow, ncols=ncol)
units = [c[:-2] for c in df_resampled.columns if "_p" in c]
for i in range(len(units)):
    ax = axs.reshape(-1)[i]
    ax.plot(
        df_resampled[units[i] + "_q"], df_resampled[units[i] + "_p"], label=units[i]
    )
    ax.title.set_text(units[i])

fig.tight_layout()

# %%
## TODO Q3: Your code here
gaia = df_resampled["gaia_p"]
gaia.plot()
gaia_range = (min(gaia), max(gaia))
gaia_ramp = (gaia.diff()).dropna()
max_ramp = max(gaia_ramp)
min_ramp = min(gaia_ramp)
steep_ramp = max(np.abs([max_ramp, min_ramp]))

## TODO Q4: Your code here
df_resampled["recon"] = 0
for x in df_resampled.columns[:-1:2]:
    if x != "pcc_p":
        df_resampled["recon"] += df_resampled[x]
# %%
## Part two: "Collecting fresh data"

# Hint 1: You can build up on the "read_and_plot_data.py" from day 2
# Hint 2: Yoy may want to store your response metric functions from day 2 in the "util.py" and import all of them with
# "from util import *"

if use_setpoint_log:

    # Loop over all steps and extract T_1, T_2 and the step size
    results = {}

    for idx in range(0, len(sp_data) - 1):
        label = f"Step_{sp_data[idx]['value']}kW"

        # Extract T_1 and T_2 from the setpoint JSON
        T_1 = sp_data[idx]["time"]
        T_2 = sp_data[idx + 1]["time"]

        # Change timestamp format
        T_1 = pd.to_datetime(pd.to_numeric(T_1), unit="s").round("1s")
        T_2 = pd.to_datetime(pd.to_numeric(T_2), unit="s").round("1s")

        # To ensure we are not considering values of the next load step
        T_2 = T_2 - timedelta(seconds=0.2)

        # define measured output y and target setpoint r
        y = df_resampled["pcc_p"]
        r = pd.Series(0, index=y.index)

        # Derive step direction from the setpoint data

        Positive_step = True
        if sp_data[idx]["value"] < sp_data[idx - 1]["value"]:
            Positive_step = False
        # Collect response metrics results
        os, T_os = overshoot(y, r, T_1, T_2, positive_step=Positive_step)
        results[label] = {
            "overshoot": os,
            "undershoot": undershoot(y, r, T_os, T_2, positive_step=Positive_step),
            "settling_time": settling_time(y, r, T_1, T_2, 2),
            "RMSE": rmse(y, r, T_1, T_2),
        }
    print(pd.DataFrame.from_dict(results))
"""     pd.DataFrame.from_dict(results).plot(kind="bar")
    plt.title("Metrics")
    plt.tight_layout()
    plt.savefig("data/test_metrics" + MEAS_LOG_FILE[-10:] + ".png")
    plt.show(block=True) """
