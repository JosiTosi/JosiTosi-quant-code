# volume_surface_visualizer.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import Slider, Button
from pathlib import Path

# === Einstellungen ===
input_folder = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/vol_surface")
file_name = "eurusd_volume_surface.csv"

# === Daten laden ===
csv_path = input_folder / file_name
print(f"Versuche zu laden: {csv_path}")
df = pd.read_csv(csv_path)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# === Zeit in Zahlen umwandeln für 3D-Plots ===
df["time_num"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds() / 3600  # in Stunden

# === Gitter für 3D-Plot ===
pivot_table = df.pivot_table(index="time_num", columns="price", values="volume", fill_value=0)
X, Y = np.meshgrid(pivot_table.columns.values, pivot_table.index.values)
Z = pivot_table.values

# === 3D Plot erstellen ===
fig = plt.figure(figsize=(12, 10)) # Größe angepasst für Slider
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap="viridis")

ax.set_xlabel("Price")
ax.set_ylabel("Time [hours]")
ax.set_zlabel("Volume")
plt.title("Volume Surface - EUR/USD")
plt.colorbar(surf, shrink=0.5, aspect=10)

# Füge Slider für die Rotation hinzu
ax_elev = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_azim = plt.axes([0.25, 0.05, 0.65, 0.03])

elev_slider = Slider(ax_elev, 'Elevation', 0, 180, valinit=30)
azim_slider = Slider(ax_azim, 'Azimuth', 0, 360, valinit=45)

def update(val):
    ax.view_init(elev_slider.val, azim_slider.val)
    fig.canvas.draw_idle()

elev_slider.on_changed(update)
azim_slider.on_changed(update)

# Füge Reset-Button hinzu
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_ax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

def reset(event):
    elev_slider.reset()
    azim_slider.reset()

button.on_clicked(reset)

plt.tight_layout()
plt.show()