"""
This script loads the capacitor voltage vs. time matlab arrays from the folder,
then finds the energy stored in the capacitor over time periods of a day, a week, etc.

AUTHOR: Hector French
WRITTEN: 14/7/26
LAST UPDATED: 14/7/26
"""

from scipy.io import loadmat
import numpy as np
from pv_model import get_iv_pv_data

C = 1440 # The capacitance in the Simulink simulation, in Farads
R = 1.5 # The resistance in the Simulink simulation, in ohms.


def load_data():
    """ Loads the voltage and time data from the matlab file."""
    vc_data = loadmat("Data/vc_output.mat")
    Vcs = vc_data["Vc"].flatten()
    times = vc_data["t"].flatten()
    return (Vcs, times)


def main():
    """ The main function."""
    Vcs, times = load_data()
    Es = 0.5 * C * Vcs ** 2
    maximum_power = np.max(Es)

    pv_current_data = loadmat('Data/pv_current.mat')
    irradiances = pv_current_data["irradiances"].flatten().tolist()
    print(irradiances)
    print(type(irradiances))
    P_maxes = np.array([])
    Ps = get_iv_pv_data(irradiances)
    for day in Ps:
        max_power = max(day)
        P_maxes = np.append(P_maxes, max_power)
    print(P_maxes)

main()


