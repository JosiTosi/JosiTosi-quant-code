# 📥 Dukascopy Forex Tick Data Fetcher (Multi-Threaded)

Dieses Projekt ermöglicht es, **historische Tick-Daten** (Bid/Ask) für beliebige Forex-Paare direkt von der offiziellen **Dukascopy-Datenbank** herunterzuladen.  
Es speichert die Daten **jahrweise als CSV** und nutzt dabei **paralleles Multi-Threading**, um den Prozess deutlich zu beschleunigen.

---

## 📌 Features

- 🔁 Download von **Tick-Daten pro Stunde**
- 📦 Speicherung in **1 Datei pro Jahr**, **1 Ordner pro Währungspaar**
- 🧵 **Multi-Threaded** (konfigurierbar) → sehr schneller Download
- 📊 Fortschrittsanzeige mit `tqdm`
- 🔧 Leicht anpassbar für jede Zeitspanne und jedes Währungspaar

---

## 📁 Ergebnisstruktur

Beispielausgabe bei Konfiguration für `EURUSD` und Jahr `2023`:
./EURUSD_tick/
└── EURUSD_2023.csv

Die CSV-Dateien enthalten:

| timestamp            | bid     | ask     |
|----------------------|---------|---------|
| 2023-01-01 00:00:00  | 1.07123 | 1.07140 |
| ...                  | ...     | ...     |

---

## ⚙️ Installation

```bash
pip install requests pandas tqdm

Keine externen APIs, keine Anmeldung – alles basiert auf öffentlich zugänglichen Daten von Dukascopy.

# 🚀 Verwendung

1. Öffne forex_data_fetcher.py

Passe oben im Script diese Parameter an:
PAIRS = ["EURUSD", "GBPUSD"]   # Währungspaare
START_YEAR = 2023              # Startjahr (einschließlich)
END_YEAR = 2023                # Endjahr (einschließlich)
MAX_WORKERS = 8                # Anzahl paralleler Threads
BASE_PATH = "."                # Zielordner

2. Starte das Script
python3 forex_data_fetcher.py

3. Fortschritt wird angezeigt
📦 Lade Tick-Daten für EURUSD, Jahr 2023 (parallel)
EURUSD 2023:  35%|███████████▍       | 3083/8760 [01:32<2:39:00, 0.59h/s]

# ⏱ Performance

Komponente
Empfehlung
💻 Mac M1/M2/M3
6–12 Threads
🧠 Windows mit 8 Cores
8–16 Threads
🔌 Thermische Limits
Bei MacBook Air ggf. auf 6–8 begrenzen

# 🧠 Warum Tick-Daten?

Tick-Daten sind die feinste verfügbare Marktdatenform:
	•	Kein Aggregat wie M1, H1 oder Daily
	•	Ideal für Volumenanalyse, Footprint, Orderflow oder Backtesting
	•	Ermöglicht Erstellung einer Volatility Surface (Zeit × Preis × Aktivität)