# Simulierte Daten 
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === Einstellungen ===
output_data_folder = "/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/vol_surface"
output_image_folder = "/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/vol_surface/vol_surface_visual"
file_name = "eurusd_volume_surface.csv"
image_name = "eurusd_volume_surface.png"

num_price_levels = 50
num_time_steps = 100

# === Simuliere Daten ===
prices = np.linspace(1.0500, 1.0600, num=num_price_levels)
times = pd.date_range("2024-01-01", periods=num_time_steps, freq="H")
volumes = np.random.poisson(lam=10, size=(num_time_steps, num_price_levels))

# === DataFrame erstellen ===
records = []
for i, time in enumerate(times):
    for j, price in enumerate(prices):
        records.append({
            "timestamp": time,
            "price": round(price, 5),
            "volume": volumes[i, j]
        })

df = pd.DataFrame(records)

# === Ordner erstellen, falls nötig ===
os.makedirs(output_data_folder, exist_ok=True)
os.makedirs(output_image_folder, exist_ok=True)

# === CSV speichern ===
csv_path = os.path.join(output_data_folder, file_name)
df.to_csv(csv_path, index=False)
print(f"[✓] Volume Surface gespeichert unter: {csv_path}")

# === Daten für Plot vorbereiten ===
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['time_num'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds() / 3600  # Stunden

pivot = df.pivot_table(index="time_num", columns="price", values="volume", fill_value=0)
X, Y = np.meshgrid(pivot.columns.values, pivot.index.values)
Z = pivot.values

# === 3D Plot erzeugen ===
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_xlabel("Price")
ax.set_ylabel("Time [h]")
ax.set_zlabel("Volume")
plt.title("EUR/USD Volume Surface")

# === Grafik als PNG speichern ===
image_path = os.path.join(output_image_folder, image_name)
plt.savefig(image_path, dpi=300)
plt.close()

print(f"[✓] Grafik gespeichert unter: {image_path}")