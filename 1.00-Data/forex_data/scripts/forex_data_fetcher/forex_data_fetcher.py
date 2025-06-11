"""
📥 Forex Tick Data Fetcher – Parallel + Fortschrittsanzeige + File-Check + Logging
Autor: Dein Name
Version: 2.3

Lädt Tick-Daten (bid/ask) von Dukascopy für beliebige Forex-Paare.
Speichert jahrweise als CSV mit Multi-Threading und Fortschrittsanzeige.
Bereits existierende Dateien werden übersprungen. Alles wird geloggt.
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import lzma
import struct
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# === BENUTZEREINSTELLUNGEN ===
PAIRS = ["EURUSD","GBPUSD","AUDUSD","NZDUSD","USDCAD","USDCHF","USDJPY"]
START_YEAR = 2014
END_YEAR = 2024
BASE_PATH = "/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/price_data/tick"
MAX_WORKERS = 8

# === URL-Helfer ===
def get_url(symbol, dt):
    symbol = symbol.upper()
    return (
        f"https://datafeed.dukascopy.com/datafeed/{symbol}/"
        f"{dt.year}/{dt.month - 1:02d}/{dt.day:02d}/{dt.hour:02d}h_ticks.bi5"
    )

# === Tick-Datei herunterladen & extrahieren ===
def download_and_extract(pair, dt):
    url = get_url(pair, dt)
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return []
        raw = lzma.decompress(r.content)
        records = []
        for i in range(0, len(raw), 20):
            chunk = raw[i:i + 20]
            if len(chunk) < 20:
                continue
            m = struct.unpack(">IIIff", chunk)
            ms = m[0]
            bid = m[3]
            ask = m[4]
            timestamp = dt + timedelta(seconds=ms / 1000.0)
            records.append([timestamp, bid, ask])
        return records
    except Exception:
        return []

# === Hauptfunktion pro Jahr & Paar ===
def fetch_yearly_ticks_parallel(pair, year, base_path):
    file_name = f"{pair.upper()}_{year}.csv"
    folder = os.path.join(base_path, f"{pair.upper()}_tick")
    file_path = os.path.join(folder, file_name)
    log_path = os.path.join(folder, "download_log.txt")

    # === Logging
    def log(msg):
        os.makedirs(folder, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")

    # === Datei existiert schon?
    if os.path.exists(file_path):
        msg = f"[↪] Datei existiert bereits – übersprungen: {file_name}"
        print(msg)
        log(msg)
        return

    print(f"\n📦 Lade Tick-Daten für {pair}, Jahr {year} (parallel)")
    log(f"[START] Lade Tick-Daten für {pair}, Jahr {year}")

    start_dt = datetime(year, 1, 1, 0, 0)
    end_dt = datetime(year + 1, 1, 1, 0, 0)
    hours = [start_dt + timedelta(hours=i) for i in range(int((end_dt - start_dt).total_seconds() // 3600))]

    all_ticks = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_and_extract, pair, dt): dt for dt in hours}
        with tqdm(total=len(futures), desc=f"{pair} {year}", unit="h") as pbar:
            for future in as_completed(futures):
                dt = futures[future]
                try:
                    ticks = future.result()
                    if ticks:
                        all_ticks.extend(ticks)
                except Exception as e:
                    log(f"[FEHLER] bei {pair} {dt}: {e}")
                pbar.update(1)

    # === Speichern
    if all_ticks:
        df = pd.DataFrame(all_ticks, columns=["timestamp", "bid", "ask"])
        os.makedirs(folder, exist_ok=True)
        df.sort_values("timestamp", inplace=True)
        df.to_csv(file_path, index=False)
        msg = f"[✓] {pair} {year} gespeichert: {file_name}"
        print(msg)
        log(msg)
    else:
        msg = f"[!] Keine Daten für {pair} im Jahr {year}"
        print(msg)
        log(msg)

# === Einstiegspunkt ===
if __name__ == "__main__":
    try:
        for pair in PAIRS:
            for year in range(START_YEAR, END_YEAR + 1):
                fetch_yearly_ticks_parallel(pair, year, BASE_PATH)
    except KeyboardInterrupt:
        print("\n❌ Abbruch durch Benutzer – Script wurde gestoppt.")
