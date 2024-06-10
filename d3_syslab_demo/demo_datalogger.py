import syslab
from json import dump
from time import sleep, time

# Defines location and name of the measurements file
LOG_FILE = f'data/measurements/measurements_{time():.00f}.json'
print(f"Logging to file {LOG_FILE}")

# Set up a connection to the switchboards
sb3192 = syslab.SwitchBoard('319-2')
sb3193 = syslab.SwitchBoard('319-3')
sb33012 = syslab.SwitchBoard("330-12")
sb1172 = syslab.SwitchBoard('117-2')

# Convenience function to
def take_measurements():
    measurements = {
        "pcc_p": sb3192.getActivePower('Grid'),
        "pcc_q": sb3192.getReactivePower('Grid'),
        "pv319_p": sb3192.getActivePower('PV'),
        "pv319_q": sb3192.getReactivePower('PV'),
        "dumpload_p": sb3192.getActivePower('Dumpload'),
        "dumpload_q": sb3192.getReactivePower('Dumpload'),
        "gaia_p": sb33012.getActivePower('Gaia'),
        "gaia_q": sb33012.getReactivePower('Gaia'),
        "pv330_p": sb33012.getActivePower('PV_1'),
        "pv330_q": sb33012.getReactivePower('PV_1'),
        "b2b_p": sb3193.getActivePower('ABB_Sec'),
        "b2b_q": sb3193.getReactivePower('ABB_Sec'),
        "battery_p": sb1172.getActivePower('Battery'),
        "battery_q": sb1172.getReactivePower('Battery'),
    }
    return [{'unit': k, 'value': meas.value, 'time': meas.timestampMicros/1e6} for k, meas in measurements.items()]


while True:
    measurement = take_measurements()

    # Open the output file in "append" mode which adds lines to the end
    with open(LOG_FILE, 'a') as file:
        for m in measurement:
            # Convert the dictionary m to a json string and put it
            # in the file.
            dump(m, file)
            # Write a newline for each measurement to make loading easier
            file.write('\n')
    sleep(1)
