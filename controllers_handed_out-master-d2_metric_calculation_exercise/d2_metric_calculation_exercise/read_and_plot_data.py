import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir = "controllers_handed_out-master-d2_metric_calculation_exercise/d2_metric_calculation_exercise/"

plt.ion()
# Creating a list of all csv files in the current working directory
csv_files = [
    f for f in os.listdir('.') if f.endswith(".csv") and "unit_characterization_" in f
]

# Create a dictionary with one csv file each key stored as dataframe
dfs_dict = {
    filename: pd.read_csv(filename, index_col=0) for filename in csv_files
}

# Plot all csv files included in the dfs_dict
for title, df in dfs_dict.items():
    plt.figure()
    ax = plt.axes()
    df.plot(ax=ax)
    plt.title(title)
    plt.show(block=True)


def overshoot(y, r, T_1, T_2, positive_step=None):
    # TODO Q2: Your code here
    result = 10.0
    t_os = 9
    return result, t_os  # Return both the overshoot and the time


def undershoot(y, r, T_os, T_2, positive_step=None):
    # TODO Q2: Your code here
    result = 10.0
    return result


def settling_time(y, r, T_1, T_2, M):
    e = r[T_1:T_2] - y[T_1:T_2]
    for t in e.index:
        t_settling = t
        if e.loc[t:].abs().max() < M:
            break
    
    result = t_settling - T_1
    return result


def rmse(y, r, T_1, T_2):
    sq_e = r[T_1:T_2] - y[T_1:T_2]
    sq_e_sum = 0
    for x in sq_e:
        sq_e_sum += x**2

    rsme = (sq_e_sum / len(sq_e))**(1/2)
    result = rsme
    return result


results = {}
for label, df in dfs_dict.items():

    # get measured output y and target setpoint r
    y = df.machine_state
    r = df.target

    # Derive step direction from target values
    # TODO Q2: Your code here
    Positive_step = True

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
