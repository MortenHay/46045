# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.ion()
# Creating a list of all csv files in the current working directory
csv_files = [
    f for f in os.listdir(".") if f.endswith(".csv") and "unit_characterization_" in f
]

# Create a dictionary with one csv file each key stored as dataframe
dfs_dict = {filename: pd.read_csv(filename, index_col=0) for filename in csv_files}

# Plot all csv files included in the dfs_dict
for title, df in dfs_dict.items():
    plt.figure()
    ax = plt.axes()
    df.plot(ax=ax)
    plt.title(title)
    plt.show(block=True)


def overshoot(y, r, T_1, T_2, positive_step=True):
    result, t_max = 0, 0
    if positive_step:
        result = (y - r).loc[T_1:T_2].max()
    else:
        result = (r - y).loc[T_1:T_2].max()

    return max(result, 0), t_max


def undershoot(y, r, T_os, T_2, positive_step=None):
    result, t_max = 0, 0
    if positive_step:
        result = -((r - y.loc[T_2]).loc[T_os:T_2].min())
    else:
        result = -((r - y).loc[T_os:T_2].min())

    return max(result, 0)


def settling_time(y, r, T_1, T_2, M):
    # TODO Q2: Your code here
    result = 10.0
    return result


def rmse(y, r, T_1, T_2):
    # TODO Q2: Your code here
    result = 10.0
    return result


results = {}
for label, df in dfs_dict.items():

    # get measured output y and target setpoint r
    y = df.machine_state
    r = df.target

    # Derive step direction from target values
    # TODO Q2: Your code here
    Positive_step = r[r.idxmax()] > r.iloc[0]

    os, T_os = overshoot(y, r, 5, 30, positive_step=Positive_step)
    results[label] = {
        "overshoot": os,
        "undershoot": undershoot(y, r, T_os, 30, positive_step=Positive_step),
        "settling_time": settling_time(y, r, 5, 30, 2),
        "RMSE": rmse(y, r, 5, 30),
    }

metricdf = pd.DataFrame.from_dict(results).plot(kind="bar")
plt.title("Metrics")
plt.tight_layout()
plt.show(block=True)

# %%
