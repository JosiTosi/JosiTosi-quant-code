# 💱 Forex Data Repository

Zentrale Sammlung aller Forex-relevanten Daten für Trading, Analyse und Backtesting. Diese Repository enthält verschiedene Datenquellen und -formate für umfassende Währungsmarkt-Analysen.

## 📂 Repository-Struktur

```
forex_data/
├── 📁 price_data/              # Historische Kursdaten
│   ├── daily/                  # Tägliche OHLCV Daten
│   ├── hourly/                 # Stündliche Daten  
│   ├── minute/                 # Minuten-Charts (1M, 5M, 15M)
│   └── tick/                   # Tick-by-Tick Daten
├── 📁 cot_data/               # COT (Commitment of Traders) Daten
│   ├── raw/                    # Rohe COT-Downloads
│   ├── processed/              # Bereinigte COT-Daten
│   └── indicators/             # Berechnete COT-Indikatoren
├── 📁 economic_data/          # Wirtschaftsdaten
│   ├── interest_rates/         # Zinssätze der Zentralbanken
│   ├── inflation/              # Inflationsdaten
│   ├── gdp/                    # BIP-Daten
│   └── employment/             # Arbeitsmarktdaten
├── 📁 sentiment_data/         # Sentiment-Indikatoren
│   ├── retail_sentiment/       # Retail-Trader Sentiment
│   ├── institutional/          # Institutionelle Positionierung
│   └── social_media/           # Social Media Sentiment
├── 📁 volatility_data/        # Volatilitätsdaten
│   ├── implied_vol/            # Implizite Volatilität
│   ├── realized_vol/           # Realisierte Volatilität
│   └── vol_surface/            # Volatilitätsoberflächen
├── 📁 correlation_data/       # Korrelationsmatrizen
├── 📁 scripts/                # Daten-Scripts und Tools
├── 📁 configs/                # Konfigurationsdateien
└── 📁 documentation/          # Dokumentation und Guides
```

## 🎯 Datentypen-Übersicht

### 📈 Price Data (Kursdaten)
**Dateiformate:** CSV, JSON, Parquet
**Zeiträume:** 2000 - heute
**Frequenzen:** Tick, 1Min, 5Min, 15Min, 1H, 4H, Daily, Weekly

**Wichtigste Pairs:**
- **Majors:** EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD
- **Minors:** EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY, etc.
- **Exotics:** USD/TRY, USD/ZAR, USD/MXN, etc.

**Spalten:**
- `timestamp` - Zeitstempel
- `open` - Eröffnungskurs
- `high` - Höchstkurs
- `low` - Tiefstkurs  
- `close` - Schlusskurs
- `volume` - Handelsvolumen (wenn verfügbar)
- `spread` - Bid/Ask Spread

### 📊 COT Data (Commitment of Traders)
**Quelle:** CFTC (Commodity Futures Trading Commission)
**Update:** Wöchentlich (Freitags)
**Zeitraum:** 2006 - heute

**Kategorien:**
- **Legacy Format** - Traditionelle Aufteilung
- **Disaggregated Format** - Detaillierte Trader-Kategorien
- **Traders in Financial Futures (TiFF)** - Finanzfutures-fokussiert

**Key Metrics:**
- Open Interest (Gesamtpositionen)
- Long/Short Positionen nach Trader-Typ
- Net Positions (Long - Short)
- Wöchentliche Veränderungen

### 📰 Economic Data (Wirtschaftsdaten)
**Quellen:** Zentralbanken, Statistikämter, Bloomberg, Reuters
**Update:** Ereignisbasiert

**Kategorien:**
- **Zinssätze:** Fed Funds Rate, ECB Rate, BoE Rate, etc.
- **Inflation:** CPI, PPI, Core Inflation
- **Arbeitsmarkt:** NFP, Unemployment Rate, Job Openings
- **Wachstum:** GDP, Industrial Production
- **Retail:** Retail Sales, Consumer Confidence

### 😊 Sentiment Data
**Quellen:** Broker, IG Client Sentiment, AAII, Fear & Greed Index
**Update:** Täglich/Stündlich

**Metriken:**
- Long/Short Ratio der Retail-Trader
- Institutionelle Positionierung
- Social Media Buzz
- VIX und Currency Volatility Index

## 🛠️ Verfügbare Scripts

### Data Collection Scripts
```bash
scripts/
├── fetch_price_data.py         # Kursdaten von verschiedenen APIs
├── fetch_cot_data.py          # COT-Daten von CFTC
├── fetch_economic_data.py     # Wirtschaftsdaten-Sammler
├── fetch_sentiment_data.py    # Sentiment-Daten Aggregator
└── data_updater.py           # Automatische Updates
```

### Analysis Scripts  
```bash
scripts/analysis/
├── correlation_analysis.py    # Korrelationsberechnungen
├── cot_indicators.py         # COT-Indikatoren berechnen
├── volatility_analysis.py   # Volatilitäts-Metriken
└── backtest_framework.py    # Backtesting-Tools
```

### Utility Scripts
```bash
scripts/utils/
├── data_cleaner.py          # Datenbereinigung
├── format_converter.py     # Format-Konvertierungen
├── data_validator.py       # Qualitätskontrolle
└── merge_datasets.py      # Datensätze kombinieren
```

## 📅 Daten-Update Schedule

| Datentyp | Frequenz | Update-Zeit | Script |
|----------|----------|-------------|---------|
| **Price Data** | Real-time/1Min | Kontinuierlich | `fetch_price_data.py` |
| **COT Data** | Wöchentlich | Freitag 15:30 EST | `fetch_cot_data.py` |
| **Economic Data** | Ereignisbasiert | Nach Veröffentlichung | `fetch_economic_data.py` |
| **Sentiment Data** | Täglich | 00:00 UTC | `fetch_sentiment_data.py` |

## 🚀 Quick Start Guide

### 1. Repository Setup
```bash
# Repository klonen/erstellen
mkdir forex_data
cd forex_data

# Ordnerstruktur erstellen
mkdir -p price_data/{daily,hourly,minute,tick}
mkdir -p cot_data/{raw,processed,indicators}
mkdir -p economic_data/{interest_rates,inflation,gdp,employment}
mkdir -p sentiment_data/{retail_sentiment,institutional,social_media}
mkdir -p volatility_data/{implied_vol,realized_vol,vol_surface}
mkdir -p correlation_data scripts configs documentation
```

### 2. Erste Daten sammeln
```bash
# COT-Daten für EUR/USD (letzten 2 Jahre)
python scripts/fetch_cot_data.py --pairs EURUSD --years 2022,2023

# Tägliche Kursdaten für Major Pairs
python scripts/fetch_price_data.py --timeframe daily --pairs majors --start 2020-01-01

# Aktuelle Sentiment-Daten
python scripts/fetch_sentiment_data.py --source ig_client_sentiment
```

### 3. Daten analysieren
```bash
# Korrelationen berechnen
python scripts/analysis/correlation_analysis.py --timeframe daily --period 252

# COT-Indikatoren generieren  
python scripts/analysis/cot_indicators.py --pair EURUSD --indicators net_position,extremes
```

## 📊 Datenqualität & Standards

### Datenformat-Standards
**CSV-Dateien:**
- UTF-8 Encoding
- Comma-separated (`,`)
- Header-Zeile obligatorisch
- Datum im ISO-Format (YYYY-MM-DD)
- Dezimaltrennzeichen: Punkt (`.`)

**Naming Convention:**
```
{instrument}_{timeframe}_{start_date}_{end_date}.csv

Beispiele:
EURUSD_daily_2020-01-01_2023-12-31.csv
GBPUSD_1h_2023-01-01_2023-12-31.csv
cot_forex_combined_2020_2023.csv
```

### Qualitätskontrolle
- **Completeness Check:** Fehlende Zeitstempel identifizieren
- **Outlier Detection:** Unplausible Kursbewegungen markieren
- **Consistency Check:** Spread-Plausibilität, OHLC-Logik
- **Duplicate Removal:** Doppelte Einträge entfernen

## 🔧 Konfiguration

### configs/data_sources.json
```json
{
  "price_data": {
    "primary": "oanda_api",
    "secondary": "mt5_gateway", 
    "backup": "yahoo_finance"
  },
  "cot_data": {
    "source": "cftc_official",
    "format": "disaggregated"
  },
  "economic_data": {
    "sources": ["fred_api", "ecb_api", "boe_api"]
  }
}
```

### configs/trading_pairs.json
```json
{
  "majors": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD"],
  "minors": ["EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "EURAUD", "GBPAUD"],
  "exotics": ["USDTRY", "USDZAR", "USDMXN", "USDBRL", "USDSGD"]
}
```

## 📈 Verwendungsbeispiele

### Python Data Loading
```python
import pandas as pd
import os

# EUR/USD Tagesdaten laden
eurusd_daily = pd.read_csv('price_data/daily/EURUSD_daily_2020_2023.csv')
eurusd_daily['timestamp'] = pd.to_datetime(eurusd_daily['timestamp'])

# COT-Daten laden
cot_data = pd.read_csv('cot_data/processed/forex_cot_combined_2020_2023.csv')

# Korrelationsmatrix laden
correlations = pd.read_csv('correlation_data/daily_correlations_2023.csv', index_col=0)
```

### R Data Loading
```r
library(readr)
library(dplyr)

# Kursdaten laden
eurusd <- read_csv("price_data/daily/EURUSD_daily_2020_2023.csv")
eurusd$timestamp <- as.Date(eurusd$timestamp)

# COT-Daten laden  
cot_data <- read_csv("cot_data/processed/forex_cot_combined_2020_2023.csv")
```

## 🔍 Datenabfrage-Tipps

### Häufige Analysen
1. **Trend-Identifikation:** 50/200 MA Crossovers in Daily Data
2. **Volatility Breakouts:** ATR-basierte Signale
3. **COT Extremes:** 90th Percentile Net Positions
4. **Economic Events:** NFP Impact auf USD-Pairs
5. **Sentiment Contrarian:** Retail Long % > 80%

### Performance-Optimierung
- **Parquet-Format** für große Datensätze verwenden
- **Chunking** bei Multi-Year Analysen
- **Index** auf Timestamp-Spalten setzen
- **Memory-effiziente** Datentypen verwenden

## 📚 Dokumentation

### Wichtige Guides
- [`documentation/data_dictionary.md`](documentation/data_dictionary.md) - Alle Spalten erklärt
- [`documentation/api_reference.md`](documentation/api_reference.md) - Script-APIs
- [`documentation/troubleshooting.md`](documentation/troubleshooting.md) - Häufige Probleme
- [`documentation/best_practices.md`](documentation/best_practices.md) - Empfohlene Workflows

### External Resources
- [CFTC COT Reports](https://www.cftc.gov/dea/newcot/) - Offizielle COT-Daten
- [FRED Economic Data](https://fred.stlouisfed.org/) - US Wirtschaftsdaten
- [ECB Statistical Data](https://www.ecb.europa.eu/stats/) - Eurozone Daten
- [OANDA Historical Data](https://www.oanda.com/fx-for-business/historical-rates) - Forex Kurse

## 🤝 Contribution Guidelines

### Neue Datenquellen hinzufügen
1. Script in `scripts/` erstellen
2. Konfiguration in `configs/` erweitern
3. Dokumentation aktualisieren
4. Qualitätskontrolle implementieren

### Datenformat-Standards einhalten
- Einheitliche Zeitstempel
- Konsistente Spalten-Namen
- Plausibilitätsprüfungen
- Metadaten dokumentieren

## ⚠️ Wichtige Hinweise

### Rechtliche Aspekte
- **Lizenz-Compliance:** Datenquellen-Lizenzen beachten
- **Redistribution:** Nicht alle Daten dürfen weitergegeben werden
- **Commercial Use:** Manche APIs haben kommerzielle Beschränkungen

### Datenschutz
- **Keine personenbezogenen Daten** in Repository
- **API-Keys** in separaten, nicht-versionierten Config-Dateien
- **Backup-Strategy** für kritische Daten

### Maintenance
- **Regelmäßige Updates** der Scripts bei API-Änderungen  
- **Datenqualität** monatlich überprüfen
- **Storage-Management** bei großen Datensätzen

---

**📊 Happy Trading!**

*Letzte Aktualisierung: Dezember 2024*