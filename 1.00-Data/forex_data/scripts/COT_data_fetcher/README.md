
# 💱 Forex COT Data Fetcher

Ein spezialisiertes Python-Script zum automatischen Herunterladen von **Forex COT-Daten** (Commitment of Traders) von der CFTC. Fokus auf die wichtigsten Währungspaare für Trading-Analysen.

## 🎯 Was macht das Script?

- ✅ **Nur Forex-Daten** - Filtert automatisch die wichtigsten Währungspaare
- ✅ **Historische Daten** - Lädt vergangene Jahre (nicht aktuelle Woche)
- ✅ **Einfache Konfiguration** - Alle Settings oben im Script
- ✅ **Progress Bars** - Zeigt Fortschritt beim Download
- ✅ **Auto-Organisation** - Einzelne + kombinierte CSV-Dateien

## 📋 Voraussetzungen

### Python Installation
```bash
pip install requests pandas tqdm
```

### Unterstützte Forex Pairs
- **EURUSD** (Euro FX)
- **USDJPY** (Japanese Yen)  
- **GBPUSD** (British Pound)
- **USDCHF** (Swiss Franc)
- **USDCAD** (Canadian Dollar)
- **AUDUSD** (Australian Dollar)
- **NZDUSD** (New Zealand Dollar)
- **USDMXN** (Mexican Peso)
- **USDBRL** (Brazilian Real)
- **USDRUB** (Russian Ruble)

## ⚙️ Konfiguration (Script anpassen)

**Öffne das Script und ändere diese Werte ganz oben:**

```python
# ============================================================
# KONFIGURATION - HIER ANPASSEN
# ============================================================

# Zeitraum für historische Daten
START_YEAR = 2020  # Ab welchem Jahr
END_YEAR = 2023    # Bis welches Jahr (nicht aktuelles Jahr)

# Output Ordner
OUTPUT_FOLDER = "forex_cot_data"

# Forex Pairs die wir wollen (CFTC Namen)
FOREX_PAIRS = [
    'EURO FX',
    'JAPANESE YEN', 
    'BRITISH POUND',
    # ... weitere Pairs
]
```

### Beispiel-Konfigurationen

#### Nur Major Pairs (EUR, GBP, JPY, CHF)
```python
START_YEAR = 2021
END_YEAR = 2023
FOREX_PAIRS = [
    'EURO FX',
    'JAPANESE YEN', 
    'BRITISH POUND',
    'SWISS FRANC'
]
```

#### Letzten 2 Jahre, alle Pairs
```python
START_YEAR = 2022
END_YEAR = 2023
# FOREX_PAIRS bleibt unverändert für alle Pairs
```

## 🚀 Script ausführen

1. **Konfiguration anpassen** (siehe oben)
2. **Script starten:**
   ```bash
   python forex_cot_fetcher.py
   ```
3. **Bestätigung:** Drücke ENTER zum Starten
4. **Warten:** Das Script zeigt Progress Bars

### Beispiel-Output beim Ausführen:
```
💱 FOREX COT DATA FETCHER
==================================================
📅 Zeitraum: 2020 - 2023
💱 Forex Pairs: 10
📁 Output Ordner: forex_cot_data

Konfiguration OK? Drücke ENTER zum Starten...

🚀 Forex COT Data Fetcher gestartet
==================================================
📊 Lade COT Daten: 100%|████████| 4/4 [00:45<00:00, 11.2s/Jahr]
✅ 2020: 520 Forex Records gespeichert
✅ 2021: 520 Forex Records gespeichert
✅ 2022: 520 Forex Records gespeichert
✅ 2023: 520 Forex Records gespeichert

📈 FOREX PAIRS ÜBERSICHT:
------------------------------------------------------------
💱 EURUSD   |  208 Records | 2020-01-07 bis 2023-12-26
💱 USDJPY   |  208 Records | 2020-01-07 bis 2023-12-26
💱 GBPUSD   |  208 Records | 2020-01-07 bis 2023-12-26
...

🎉 FERTIG!
📊 Total Records: 2,080
📁 Kombinierte Datei: forex_cot_combined_2020_2023.csv
```

## 📁 Output-Dateien

Nach dem Ausführen findest du diese Dateien:

```
forex_cot_data/
├── forex_cot_2020.csv                    # Einzeljahr 2020
├── forex_cot_2021.csv                    # Einzeljahr 2021  
├── forex_cot_2022.csv                    # Einzeljahr 2022
├── forex_cot_2023.csv                    # Einzeljahr 2023
├── forex_cot_combined_2020_2023.csv      # ALLE Daten kombiniert
└── forex_pairs_summary.csv               # Übersicht pro Pair
```

### Welche Datei für was?

| Datei | Verwendung |
|-------|------------|
| `forex_cot_combined_XXXX_XXXX.csv` | **Hauptdatei** - Alle Daten für Analysen |
| `forex_cot_YYYY.csv` | Einzeljahre für spezifische Analysen |
| `forex_pairs_summary.csv` | Schnelle Übersicht der verfügbaren Daten |

## 📊 Wichtige Datenspalten

### Die wichtigsten COT-Spalten für Forex Trading:

**Basis-Informationen:**
- `Report_Date_as_YYYY_MM_DD` - Berichtsdatum
- `Forex_Pair` - Vereinfachtes Pair (EURUSD, GBPUSD, etc.)
- `Open_Interest_All` - Gesamtes Open Interest

**Positionen (Disaggregated Format):**
- `Dealer_Positions_Long_All` / `Dealer_Positions_Short_All` - Dealer Positionen
- `Asset_Mgr_Positions_Long_All` / `Asset_Mgr_Positions_Short_All` - Asset Manager
- `Lev_Money_Positions_Long_All` / `Lev_Money_Positions_Short_All` - Leveraged Funds
- `Other_Rept_Positions_Long_All` / `Other_Rept_Positions_Short_All` - Andere Reportable
- `NonRept_Positions_Long_All` / `NonRept_Positions_Short_All` - Small Traders

**Veränderungen (vs. Vorwoche):**
- `Change_in_Dealer_Long_All` - Änderung Dealer Long Positionen
- `Change_in_Lev_Money_Long_All` - Änderung Leveraged Funds Long
- etc.

## 🔍 Daten-Analyse Tipps

### COT-Daten für Forex Trading nutzen:

1. **Leveraged Funds** = Meist Hedge Funds/Spekulanten
2. **Dealers** = Banken/Market Maker (oft Contrarian-Signal)
3. **Asset Managers** = Langfristige Investoren
4. **Non-Reportable** = Kleine Trader (Retail-ähnlich)

### Beispiel-Analyse in Python:
```python
import pandas as pd

# Daten laden
df = pd.read_csv('forex_cot_data/forex_cot_combined_2020_2023.csv')

# EUR/USD Daten filtern
eurusd = df[df['Forex_Pair'] == 'EURUSD'].copy()

# Net Positions berechnen
eurusd['Lev_Money_Net'] = eurusd['Lev_Money_Positions_Long_All'] - eurusd['Lev_Money_Positions_Short_All']

# Extremwerte finden
print("Leveraged Funds Extrempositionen:")
print(f"Max Long: {eurusd['Lev_Money_Net'].max():,}")
print(f"Max Short: {eurusd['Lev_Money_Net'].min():,}")
```

## ⚠️ Wichtige Hinweise

### Was das Script NICHT macht:
- ❌ **Keine aktuellen Daten** - Nur historische Jahre
- ❌ **Keine Live-Updates** - Einmaliger Download
- ❌ **Keine Preisdaten** - Nur COT-Positionsdaten

### COT-Daten Zeitplan:
- **Veröffentlichung:** Jeden Freitag 15:30 EST
- **Stichtag:** Dienstag der gleichen Woche  
- **Verzögerung:** 3 Werktage

## 🔧 Troubleshooting

### Problem: "No module named 'tqdm'"
```bash
pip install tqdm
```

### Problem: "Keine Forex-Daten gefunden"
- Prüfe Internetverbindung
- Ändere Jahresbereich (manche Jahre haben weniger Daten)
- CFTC-Website könnte temporär down sein

### Problem: Script hängt sich auf
- CTRL+C zum Abbrechen
- Internet-Verbindung prüfen
- Kleineren Jahresbereich wählen

### Debug-Modus aktivieren:
```python
# Oben im Script hinzufügen:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Nächste Schritte

Nach dem Download kannst du:

1. **CSV in Excel/Google Sheets öffnen** für erste Analysen
2. **Python/Pandas** für detaillierte Berechnungen nutzen
3. **Trading-Strategien** basierend auf COT-Extremwerten entwickeln
4. **Backtesting** mit historischen Forex-Kursen kombinieren

## 💡 Pro-Tipps

- **Disaggregated Format** ist detaillierter als Legacy
- **Leveraged Funds** sind oft die besten Trend-Indikatoren  
- **Extreme Positionierungen** (>80% Percentile) sind interessant
- **Kombiniere COT mit Technischer Analyse** für bessere Signale

---

**Happy Trading! 📈💱**