"""
This file contains the code for modelling a single solar cell in a simple circuit.
Using the numpy and matplotlib libraries, it generates I-V and P-V curves at
different irradiance levels with a diode equation.

AUTHOR: Hector French
WRITTEN: 8/7/26
LAST UPDATED: 8/7/26
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq


# Global constants (set to get different curves)
I_ph = 7.3 # In amps
I_0 = 1e-12 # In amps
R_s = 4.1e-3 # In ohms
R_sh = 4.1 # In ohms
n = 1.5 # dimensionless
V_t = 25.7e-3 # in V
NUM_POINTS = 70


def f(I, V):
    """ The diode equation with everything on one side. Used with scipy.brentq to root-find values of I for a given V."""
    return I_ph - I_0 * (np.exp((V + I*R_s) / (n*V_t)) - 1) - (V + I*R_s) / R_sh - I


def plot_curve(x_s, y_s, title="Curve", x_label="", y_label="", save_fig=False, fig_name="Curve"):
    """ Plots the IV curve in matplotlib using the given numpy arrays."""
    axes = plt.axes()
    axes.plot(x_s, y_s)
    axes.set_title(title)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.grid(True)
    if save_fig:
        plt.savefig(f"figures/{fig_name}.png", dpi=200)
    plt.show()


def main():
    """ The main function."""
    # Generate an array of V values and calculate I for each one
    # TODO: change "stop" to change based on the variables!
    V_s = np.linspace(0, 1.13, NUM_POINTS)
    I_s = np.array([])
    for v in V_s:
        I_s = np.append(I_s, brentq(f, 0, I_ph, args=(v,)))
    # Plot the IV curve
    plot_curve(V_s, I_s, "Solar Cell I-V Curve", "Voltage (V)", "Current (I)", save_fig=False, fig_name="IV_curve")
    P_s = V_s * I_s
    # Plot the PV curve
    plot_curve(V_s, P_s, "Solar Cell P-V Curve", "Voltage (V)", "Power (P)", save_fig=False, fig_name="PV_curve")

main()
