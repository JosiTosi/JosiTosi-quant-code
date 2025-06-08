# JosiTosi Quant Trading System

## 🎯 Überblick
Dieses Repository dokumentiert meine Entwicklung eines quantitativen Trading-Systems basierend auf dem RBI-Prinzip (Research, Backtest, Implement). Das System ist in verschiedene Phasen unterteilt, die den Entwicklungsprozess einer Trading-Strategie abbilden.

## 📁 Projektstruktur

```
JosiTosi-quant-code/
├── Configs/                 # Konfigurationsdateien für verschiedene Strategien
├── Data/                    # Datenverwaltung und -verarbeitung
│   ├── forex_data/         # Forex-spezifische Daten
│   │   ├── cot_data/      # COT (Commitments of Traders) Daten
│   │   └── price_data/    # Preis- und Marktdaten
│   └── market_data/       # Allgemeine Marktdaten
├── Research/               # Strategie-Research und Dokumentation
├── Backtest/              # Backtesting-Implementierungen
└── Implement/             # Live-Trading Implementierungen
```

## 🔄 RBI System

### 1. 📘 Research
- **Aktuelle Forschungsschwerpunkte:**
  - COT (Commitments of Traders) Strategien
  - Mean Reversion im Forex-Markt
  - Trend Following mit COT-Daten

- **Ressourcen:**
  - Google Scholar für akademische Paper
  - Trading-Bücher und -Podcasts
  - YouTube-Tutorials und -Analysen
  - Trading-Community Foren

### 2. 🧪 Backtest
- **Aktuelle Backtesting-Projekte:**
  - COT-basierte Strategien
  - Multi-Timeframe Analysen
  - Optimierung von Entry/Exit-Parametern

- **Verwendete Tools:**
  - `backtesting.py` für Strategie-Tests
  - `pandas` für Datenanalyse
  - `numpy` für numerische Berechnungen
  - `talib` für technische Indikatoren

### 3. 📈 Implement
- **Aktuelle Implementierungen:**
  - COT Data Fetcher für automatisiertes Daten-Scraping
  - Risk Management System
  - Position Sizing Algorithmen

- **Entwicklungsstatus:**
  - [x] COT Data Fetcher
  - [ ] Mean Reversion Strategie
  - [ ] Trend Following System

## 🚀 Aktuelle Projekte

### COT Data Fetcher
- **Status:** ✅ Implementiert
- **Funktionen:**
  - Automatisiertes Herunterladen von COT-Daten
  - Intelligentes Caching-System
  - Schöne Konsolenausgabe
- **Nächste Schritte:**
  - Integration mit Backtesting-System
  - Automatische Datenbereinigung

### Mean Reversion Strategie
- **Status:** 🔄 In Entwicklung
- **Fokus:**
  - COT-basierte Mean Reversion
  - Multi-Timeframe Analyse
  - Risk Management

## 📊 Datenmanagement

### COT Daten
- **Format:** CSV
- **Quelle:** CFTC
- **Update-Frequenz:** Wöchentlich
- **Verarbeitung:**
  - Automatische Bereinigung
  - Standardisierung der Spalten
  - Historische Daten seit 2006

## 🔧 Technische Details

### Backtesting Setup
```python
# Beispiel Backtesting-Konfiguration
bt = Backtest(data, Strategy, 
    cash=100000, 
    commission=0.002
)
```

### Implementierung
```python
# Beispiel Trading-Bot Setup
schedule.every(15).minutes.do(main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
```

## 📝 Entwicklungslog

### 2024
- **März:**
  - Implementierung des COT Data Fetchers
  - Einrichtung der RBI-Struktur
  - Erste Backtesting-Versuche

## 🔜 Nächste Schritte
1. [ ] Mean Reversion Strategie finalisieren
2. [ ] Backtesting-System optimieren
3. [ ] Risk Management implementieren
4. [ ] Live-Trading vorbereiten

## 📚 Ressourcen
- [Backtesting.py Dokumentation](https://kernc.github.io/backtesting.py/)
- [CFTC COT Reports](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
- [Trading View](https://www.tradingview.com/)

