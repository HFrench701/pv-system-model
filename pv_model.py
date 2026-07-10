"""
This file contains the code for modelling a single solar cell in a simple circuit.
Using the numpy and matplotlib libraries, it generates I-V and P-V curves at
different irradiance levels using the diode equation.

AUTHOR: Hector French
WRITTEN: 8/7/26
LAST UPDATED: 9/7/26
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from math import log, e

# STC = standard test conditions.

# Constants
G_STC = 1000 # Irradiance in STC, in W/m^2.
NUM_POINTS = 70

# Constants calculated for a fixed solar cell size (156mm x 156mmm).
# Could implement a panel size variable + calculations of these constants in script later on.
I_ph_STC = 7.3 # Photocurrent in STC, in amps.
I_0 = 1e-12 # Saturation current, in amps.
R_s = 4.1e-3 # Series resistance, in ohms.
R_sh = 4.1 # Shunt resistance, in ohms.
n = 1.5 # Diode ideality factor.
V_t = 25.7e-3 # Thermal voltage, in volts.
V_oc_margin = 0.01 # Margin slightly below the open-circuit voltage, to ensure the entire curve is plotted.


def V_oc(G):
    """ Calculates the open-circuit voltage of the cell for a given irradiance."""
    return n * V_t * log(I_ph(G) / I_0 + 1, e)


def I_ph(G):
    """ Calculates the photocurrent of the cell for a given irradiance."""
    return I_ph_STC * (G / G_STC)


def f(I, V, G):
    """ The diode equation with everything on one side. Used with scipy.brentq to root-find values of I for a given V."""
    return I_ph(G) - I_0 * (np.exp((V + I*R_s) / (n*V_t)) - 1) - (V + I*R_s) / R_sh - I


def plot_curves(curve_xs, curve_ys, curve_labels=None, title="Curve", x_label="", y_label="", save_fig=False, fig_name="Graph"):
    """ Plots curve(s) in a single matplotlib graph using the given numpy arrays. curve_xs and curve_ys are parallel arrays of each curve's x and y values."""
    axes = plt.axes()
    # Loop through each curve and plot x against each y.
    for i in range(len(curve_xs)):
        # Give labels to each curve if they are given.
        if curve_labels is not None:
            axes.plot(curve_xs[i], curve_ys[i], label=curve_labels[i])
        else:
            axes.plot(curve_xs[i], curve_ys[i])
    axes.set_title(title)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.grid(True)
    # Enable the legend if labels are given.
    if curve_labels is not None:
        axes.legend()
    # Save the figure in the directory if instructed.
    if save_fig:
        plt.savefig(f"figures/{fig_name}.png", dpi=200)
    plt.show()


def get_iv_pv_data(G_s):
    """ Given a set of irradiances, calculate V, I and P values."""
    curve_xs = []  # An array of each curve's array of x values.
    curve_I_ys = []  # An array of each IV curve's y values.
    curve_P_ys = []  # An array of each PV curve's y values.

    # Loop through each irradiance to plot the corresponding curve.
    for g in G_s:
        # Generate an array of V values
        V_s = np.linspace(0, V_oc(g) - V_oc_margin, NUM_POINTS)
        I_s = np.array([])
        # Calculate the corresponding I
        for v in V_s:
            I_s = np.append(I_s, brentq(f, 0, I_ph(g), args=(v, g,)))
        # Calculate the corresponding P
        P_s = V_s * I_s

        curve_xs.append(V_s)
        curve_I_ys.append(I_s)
        curve_P_ys.append(P_s)
    return curve_xs, curve_I_ys, curve_P_ys


def main():
    """ The main function."""
    # Hard-coded for now; to test.
    G_s = [200, 400, 600, 800, 1000]

    # Assign each curve a label based on irradiance.
    curve_labels = []
    for g in G_s:
        curve_labels.append(f"{g} W/m^2")

    # Calculate IV and PV curve points
    curve_xs, curve_I_ys, curve_P_ys = get_iv_pv_data(G_s)

    # Plot the IV curve
    plot_curves(curve_xs, curve_I_ys, curve_labels, "Solar Cell I-V Curve", "Voltage (V)", "Current (I)", save_fig=True, fig_name="IV_curves")
    # Plot the PV curve
    plot_curves(curve_xs, curve_P_ys, curve_labels, "Solar Cell P-V Curve", "Voltage (V)", "Power (P)", save_fig=True, fig_name="PV_curves")

main()
