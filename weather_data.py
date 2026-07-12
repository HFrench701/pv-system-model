"""
Following on from generating I-V and P-V curves for different irradiances in pv_model.py, this program extracts
real weather data - sunlight irradiance - for one day at a given date, at a given location.
It calculates the current generated in a PV cell using the same model, and plots it against time in a matplotlib graph.

AUTHOR: Hector French
WRITTEN: 10/7/26
LAST UPDATED: 10/7/26
"""

import requests
import numpy as np
from pv_model import plot_curves, I_ph
from scipy.io import savemat

# Location date/time setting
location = "Christchurch"
latitude = -43.532024
longitude = 172.636633
date = "2025-07-10"
timezone = "Pacific/Auckland"


def nice_date(date_str):
    """ Converts date from YYYY-MM-DD format to nice format e.g. July 10 2026."""
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year, month, day = date_str.split("-")
    return f"{months[int(month) - 1]} {day} {year}"


def get_current_vs_time_data():
    """ Fetches weather data from weather api using JSON at given location and date."""
    weather_api_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&timezone={timezone}&hourly=shortwave_radiation,temperature_2m"
    response = requests.get(weather_api_url)
    data = response.json()
    irradiances = np.array(data["hourly"]["shortwave_radiation"])
    currents = I_ph(irradiances)
    timestamps = data["hourly"]["time"]
    hours = np.array([timestamp.split('T')[1].split(':')[0] for timestamp in timestamps], dtype=int)
    hours = hours * 3600
    return currents, hours


def main():
    """ The main function."""
    currents, hours = get_current_vs_time_data()
    plot_curves([hours], [currents], None, f"Estimated PV Current - {nice_date(date)}, {location}", "Hour of Day", "Current (A)", False, "Current v. Time Graph Chch 10-7-26")
    time_series_data = np.column_stack((hours, currents))
    savemat("Data/pv_current.mat", {"pv_current_data": time_series_data})


main()
