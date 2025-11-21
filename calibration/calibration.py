# https://github.com/jessica-herrmann/vesselprint | Skylar-Scott Lab

# Last updated: 11.19.25

############################################################### Import: Dependencies ######################################################################

import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from numpy import array, exp
from scipy.optimize import curve_fit

############################################################### Print Speeds ######################################################################

speed = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 
         0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 
         1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 
         3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 
         4.6, 4.7, 4.8, 4.9, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 
         11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 
         18.5, 19, 19.5, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
         33, 34, 35]

############################################################### Measured Data ######################################################################

measured_data = pd.read_csv('inputs/diameters.csv')

diameter = measured_data.loc[:, 'Length']

diameter_array = diameter.to_numpy()
diameter_array = diameter_array / 1000 # convert microns to mm

# Average the recorded measurements from a given segment
diameter_averages = np.mean(diameter_array.reshape(-1, 3), axis=1)

############################################################### Predictions ######################################################################

"""
volume = pi r^2 L
flow*time = r^2 * (speed*time) * 3.14
flow = r^2 * speed * 3.14
r = sqrt(flow/(speed*pi))
"""

# Arrays for fitting
speed_arr = speed[0:]
diam_arr = diameter_averages[0:]

# Divide measured diameters by 2 to get radius
radius_arr = diam_arr / 2

def filament_radius(speed, flow):
  return np.sqrt(np.abs(flow)/(np.abs(speed)*np.pi))

# Curve fitting
param, param_cov = curve_fit(filament_radius, speed_arr, radius_arr)
flow = param[0]
#print(flow)

param, _ = curve_fit(filament_radius, speed_arr, radius_arr) # curve_fit(function, x, y)
# print(f'parameters: {param}')
# print(f'covariance: {cov}')
flow = param[0]

print(f'Volumetric flow rate (Q): {flow} mm^3/s')

speeds_pred = speed_arr
rads_pred = [filament_radius(s, flow) for s in speeds_pred]
start = 0

fig = go.Figure(layout_title_text = 'Ink Calibration (Pink Acrylic Powder in Carbopol), Pressure-Based Printing')
# Add traces
fig.add_trace(go.Scatter(x=speeds_pred[start:], y=rads_pred[start:],
                    mode='lines',
                    name='predicted'))
fig.add_trace(go.Scatter(x=speed_arr[start:], y=radius_arr[start:],
                    mode='markers',
                    name='observed'))
fig.update_layout(title_x=0.5, font_family='Avenir', legend_font_size=18, legend_font_color='black', title_font_size=25, title_font_color='black')
fig.update_xaxes(title_text='Nozzle translation speed (mm/s)', title_font = {"size": 18}, title_font_color='black')
fig.update_yaxes(title_text='Filament radius (mm)', title_font = {"size": 18},title_font_color='black')

# Save figure
fig.write_html(f'outputs/radii_pressure.html')

# Save Q
with open('Q_pressure.txt', 'w') as f:
	f.write(f'Volumetric flow rate, Q, is {flow}.')
f.close()
