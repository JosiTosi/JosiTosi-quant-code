# Quantitative Datenbeschaffung und -analyse für Forex Trading

Dieses Repository enthält Skripte zur automatisierten Beschaffung, Verarbeitung und Speicherung verschiedener Datentypen, die für quantitative Analysen im Forex-Handel relevant sind. Es ist Teil eines umfassenderen RBI (Research, Backtest, Implement) Systems.

## 📁 Projektstruktur

```
1.00-Data/
└── forex_data/
    ├── alternative_data/
    │   ├── commodity_prices/
    │   ├── credit_card_data/
    │   ├── nightlights/
    │   ├── parking_lots/
    │   ├── shipping_traffic/
    │   └── trade_balance/
    ├── economic_data/
    │   ├── cot_data/
    │   ├── employment/
    │   ├── gdp/
    │   └── interest_rates/
    ├── regime_data/
    │   ├── gold_data/
    │   ├── mobility_data/
    │   └── vix_data/
    ├── sentiment_data/
    │   ├── google_trends/
    │   ├── news_sentiment/
    │   ├── retail_sentiment/
    │   └── social_media/
    ├── volatility_data/
    │   ├── implied_volatility/
    │   ├── realized_volatility/
    │   └── volatility_surface/
    └── scripts/
        ├── alternative_data_fetcher/
        │   ├── commodity_prices/
        │   │   └── commodity_prices_fetcher.py
        │   ├── credit_card/
        │   │   └── credit_card_data_fetcher.py
        │   ├── nightlights/
        │   │   └── nightlight_analyzer.py
        │   ├── parking_lots/
        │   │   └── parking_lot_analyzer.py
        │   ├── shipping_traffic/
        │   │   └── shipping_traffic_analyzer.py
        │   └── trade_balance/
        │       └── trade_balance_fetcher.py
        ├── COT_data_fetcher/
        │   └── cot_data_fetcher.py
        ├── economic_data_fetcher/
        │   ├── employment/
        │   │   └── employment_data_fetcher.py
        │   ├── gdp/
        │   │   └── gdp_data_fetcher.py
        │   └── interest_rates/
        │       └── interest_rates_fetcher.py
        ├── regime_data_fetcher/
        │   ├── gold_data/
        │   │   └── gold_data_fetcher.py
        │   ├── mobility_data/
        │   │   └── mobility_data_fetcher.py
        │   └── vix_data/
        │       └── vix_data_fetcher.py
        ├── sentiment_data_fetcher/
        │   ├── google_trends/
        │   │   └── google_trends_fetcher.py
        │   ├── news/
        │   │   └── news_sentiment_fetcher.py
        │   ├── retail/
        │   │   └── retail_sentiment_fetcher.py
        │   └── social_media/
        │       └── social_media_sentiment_fetcher.py
        ├── volatility_data_fetcher/
        │   ├── implied_volatility/
        │   │   └── implied_volatility_fetcher.py
        │   ├── realized_volatility/
        │   │   └── realized_volatility_fetcher.py
        │   └── volatility_surface/
        │       └── volatility_surface_fetcher.py
        └── requirements.txt
```

## 📜 Skripte Übersicht

Die Skripte sind in verschiedene Kategorien unterteilt, basierend auf dem Datentyp, den sie sammeln.

### 🌐 Alternative Daten Fetcher
Diese Skripte sammeln Daten aus unkonventionellen Quellen, um einzigartige Einblicke in Markttrends zu gewinnen.

*   `commodity_prices_fetcher.py`: Sammelt und analysiert Rohstoffpreise.
*   `credit_card_data_fetcher.py`: Beschafft und analysiert Kreditkartentransaktionsdaten.
*   `nightlight_analyzer.py`: Analysiert Satellitenbilder von Nachtlichtern zur Wirtschaftsaktivität.
*   `parking_lot_analyzer.py`: Analysiert Parkplatzauslastung mittels Satellitenbildern als Wirtschaftsindikator.
*   `shipping_traffic_analyzer.py`: Sammelt und analysiert Schiffsverkehrsdaten.
*   `trade_balance_fetcher.py`: Holt und verarbeitet Handelsbilanzdaten.

### 📊 COT Daten Fetcher
*   `cot_data_fetcher.py`: Holt Commitment of Traders (COT) Daten.

### 📈 Wirtschaftsdaten Fetcher
Diese Skripte konzentrieren sich auf makroökonomische Indikatoren.

*   `employment_data_fetcher.py`: Beschafft Beschäftigungsdaten.
*   `gdp_data_fetcher.py`: Holt Bruttoinlandsprodukt (BIP) Daten.
*   `interest_rates_fetcher.py`: Sammelt Zinsdaten.

### 🎯 Regime Daten Fetcher
Diese Skripte helfen bei der Identifizierung von Marktregimen.

*   `gold_data_fetcher.py`: Sammelt und analysiert Golddaten.
*   `mobility_data_fetcher.py`: Beschafft und analysiert Mobilitätsdaten (Google & Apple).
*   `vix_data_fetcher.py`: Holt und analysiert VIX-Daten.

### 😊 Sentiment Daten Fetcher
Diese Skripte konzentrieren sich auf die Stimmung am Markt.

*   `google_trends_fetcher.py`: Sammelt Google Trends Daten zur Analyse des öffentlichen Interesses.
*   `news_sentiment_fetcher.py`: Holt Nachrichtenartikel und führt Sentiment-Analysen durch.
*   `retail_sentiment_fetcher.py`: Beschafft Retail-Sentiment-Daten.
*   `social_media_sentiment_fetcher.py`: Sammelt und analysiert Sentiment-Daten aus sozialen Medien.

### 🧮 Volatilitätsdaten Fetcher
Diese Skripte konzentrieren sich auf die Marktvolatilität.

*   `implied_volatility_fetcher.py`: Holt implizite Volatilitätsdaten.
*   `realized_volatility_fetcher.py`: Berechnet und holt realisierte Volatilitätsdaten.
*   `volatility_surface_fetcher.py`: Erstellt und analysiert Volatilitätsoberflächen.

## ⚙️ Detaillierte Skript-Erklärungen

### 🌐 Alternative Daten Fetcher

#### `commodity_prices/commodity_prices_fetcher.py`
*   **Funktionalität:** Dieses Skript lädt historische Preisdaten für verschiedene Rohstoffe von Yahoo Finance und FRED. Es berechnet wichtige Metriken wie Preisänderungen, Volatilität und Volumen.
*   **Datenquellen:** Yahoo Finance (für Futures-Symbole wie `GC=F`, `CL=F`) und FRED (für spezifische Rohstoff-Serien).
*   **Verarbeitung:** Die Daten werden in Pandas DataFrames geladen, bereinigt und analysiert. Es werden prozentuale Preisänderungen, gleitende Durchschnitte und Volatilität berechnet.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/alternative_data/commodity_prices/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/commodity_prices/commodity_prices_fetcher.py --symbols "GC=F" "CL=F" --start-date 2023-01-01 --end-date 2023-12-31
    ```
    *Benötigt:* `FRED_API_KEY` in der `.env`-Datei für FRED-Daten.

#### `credit_card/credit_card_data_fetcher.py`
*   **Funktionalität:** Sammelt Kreditkartentransaktionsdaten von FRED und dem Bureau of Labor Statistics (BLS). Es analysiert Ausgabenmuster und liefert Einblicke in die Konsumstimmung.
*   **Datenquellen:** FRED (Federal Reserve Economic Data) und BLS (Bureau of Labor Statistics).
*   **Verarbeitung:** Daten werden von den APIs abgerufen, in Pandas DataFrames umgewandelt und relevante Metriken wie aktuelle Umsätze, monatliche und jährliche Änderungen sowie Volatilität berechnet.
*   **Speicherung:** Die Ergebnisse werden als CSV-Dateien im Ordner `1.00-Data/forex_data/alternative_data/credit_card_data/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/credit_card/credit_card_data_fetcher.py --start-date 2020-01-01 --end-date 2023-12-31
    ```
    *Benötigt:* `FRED_API_KEY` und `BLS_API_KEY` in der `.env`-Datei.

#### `nightlights/nightlight_analyzer.py`
*   **Funktionalität:** Analysiert Satellitenbilder von Nachtlichtern, die als Proxy für die Wirtschaftsaktivität dienen können. Es berechnet die durchschnittliche und maximale Lichtintensität.
*   **Datenquellen:** Planet Labs API (für Satellitenbilder).
*   **Verarbeitung:** Bilder werden heruntergeladen, mit OpenCV und scikit-image verarbeitet, um Lichtintensität zu messen. Visualisierungen werden ebenfalls erstellt.
*   **Speicherung:** Analysedaten werden als CSV-Dateien und Visualisierungen als PNG-Bilder im Ordner `1.00-Data/forex_data/alternative_data/nightlights/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/nightlights/nightlight_analyzer.py --locations "34.0522,-118.2437" "40.7128,-74.0060" --start-date 2023-01-01 --end-date 2023-01-31
    ```
    *Benötigt:* `PLANET_API_KEY` in der `.env`-Datei.

#### `parking_lots/parking_lot_analyzer.py`
*   **Funktionalität:** Analysiert die Parkplatzauslastung anhand von Satellitenbildern, was als Indikator für die Konsumausgaben und Geschäftsaktivitäten dienen kann.
*   **Datenquellen:** Planet Labs API (für Satellitenbilder).
*   **Verarbeitung:** Satellitenbilder werden von der API abgerufen, in Graustufen konvertiert und ein Schwellenwert angewendet, um die Auslastung zu schätzen.
*   **Speicherung:** Die analysierten Auslastungsraten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/alternative_data/parking_lots/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/parking_lots/parking_lot_analyzer.py --locations "34.0522,-118.2437" --start-date 2023-01-01 --end-date 2023-01-07
    ```
    *Benötigt:* `PLANET_API_KEY` in der `.env`-Datei.

#### `shipping_traffic/shipping_traffic_analyzer.py`
*   **Funktionalität:** Holt und analysiert Daten zum Schiffsverkehr, was Einblicke in den globalen Handel und die Lieferketten geben kann.
*   **Datenquellen:** MarineTraffic API.
*   **Verarbeitung:** Schiffsdaten werden von der API abgerufen und Metriken wie Gesamtzahl der Schiffe, Durchschnittsgeschwindigkeit, Schiffstypen und Flaggenländer berechnet.
*   **Speicherung:** Die analysierten Schiffsverkehrsdaten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/alternative_data/shipping_traffic/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/shipping_traffic/shipping_traffic_analyzer.py --areas "34,35,-118,-117" --start-date 2023-01-01 --end-date 2023-01-07
    ```
    *Benötigt:* `MARINETRAFFIC_API_KEY` in der `.env`-Datei.

#### `trade_balance/trade_balance_fetcher.py`
*   **Funktionalität:** Beschafft Handelsbilanzdaten von FRED und der Weltbank, um Export- und Importdynamiken zu verstehen.
*   **Datenquellen:** FRED und World Bank Data API (`wbdata`).
*   **Verarbeitung:** Die Daten werden für verschiedene Länder abgerufen, zusammengeführt und Metriken wie die aktuelle Bilanz, monatliche Änderungen, Import-Export-Verhältnis und Handelsvolumen im Verhältnis zum BIP berechnet.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/alternative_data/trade_balance/` gespeichert.
*   **Verwendung:**
    ```bash
    python alternative_data_fetcher/trade_balance/trade_balance_fetcher.py --countries "USA" "DEU" --start-date 2018-01-01 --end-date 2023-12-31
    ```
    *Benötigt:* `FRED_API_KEY` in der `.env`-Datei.

### 📊 COT Daten Fetcher

#### `COT_data_fetcher/cot_data_fetcher.py`
*   **Funktionalität:** Dieses Skript lädt wöchentliche Commitment of Traders (COT) Daten von der CFTC-Website. Diese Daten zeigen die Positionen von Händlergruppen (Commercials, Non-Commercials, Non-Reportables) in Futures-Märkten und können als Stimmungsindikator dienen.
*   **Datenquellen:** Direkt von der CFTC-Website (Commodity Futures Trading Commission) als ZIP-Dateien im `fut_fin_txt_YYYY.zip` Format.
*   **Verarbeitung:** Das Skript lädt die ZIP-Dateien herunter und extrahiert die Daten. Es ist eine direkte Datenextraktion ohne komplexe Analyse im Skript selbst. Die Daten sind bereits in einem strukturierten Format.
*   **Speicherung:** Die heruntergeladenen ZIP-Dateien werden im Ordner `1.00-Data/forex_data/economic_data/cot_data/` gespeichert. Die Dateinamen sind `cot_data_YYYY.zip`.
*   **Verwendung:**
    ```bash
    python COT_data_fetcher/cot_data_fetcher.py
    ```
    Dieses Skript lädt automatisch die Daten der letzten 5 Jahre.

### 📈 Wirtschaftsdaten Fetcher

#### `economic_data_fetcher/employment/employment_data_fetcher.py`
*   **Funktionalität:** Beschafft monatliche Beschäftigungsdaten von der BLS API, die wichtige Einblicke in die Arbeitsmarktlage und die allgemeine Wirtschaft liefern.
*   **Datenquellen:** Bureau of Labor Statistics (BLS) API.
*   **Verarbeitung:** Daten werden von der BLS API abgerufen, in Pandas DataFrames umgewandelt und nach Datum sortiert.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/economic_data/employment/` gespeichert.
*   **Verwendung:**
    ```bash
    python economic_data_fetcher/employment/employment_data_fetcher.py
    ```
    *Benötigt:* `BLS_API_KEY` in der `.env`-Datei. (Bitte beachten Sie die Platzhalter `YOUR_API_KEY` im Skript, die ersetzt werden müssen.)

#### `economic_data_fetcher/gdp/gdp_data_fetcher.py`
*   **Funktionalität:** Holt Bruttoinlandsprodukt (BIP) Daten von der FRED API, die als wichtiger Indikator für das Wirtschaftswachstum dienen.
*   **Datenquellen:** FRED (Federal Reserve Economic Data) API.
*   **Verarbeitung:** Die Daten werden von der FRED API abgerufen, in Pandas DataFrames umgewandelt und statistische Zusammenfassungen wie Anzahl der Datenpunkte, Zeitraum, Durchschnittswerte erstellt.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/economic_data/gdp/` gespeichert.
*   **Verwendung:**
    ```bash
    python economic_data_fetcher/gdp/gdp_data_fetcher.py --series "GDP" "GDPC1" --start-date 2000-01-01 --end-date 2023-12-31
    ```
    *Benötigt:* `FRED_API_KEY` in der `.env`-Datei.

#### `economic_data_fetcher/interest_rates/interest_rates_fetcher.py`
*   **Funktionalität:** Sammelt Zinsdaten von der FRED API, die entscheidend für die Analyse der Geldpolitik und ihrer Auswirkungen auf den Forex-Markt sind.
*   **Datenquellen:** FRED (Federal Reserve Economic Data) API.
*   **Verarbeitung:** Die Daten werden von der FRED API abgerufen, in Pandas DataFrames umgewandelt und eine Zusammenfassung mit Metriken wie aktuellem und durchschnittlichem Zinssatz erstellt.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/economic_data/interest_rates/` gespeichert.
*   **Verwendung:**
    ```bash
    python economic_data_fetcher/interest_rates/interest_rates_fetcher.py --series "FEDFUNDS" "DGS10" --start-date 2000-01-01 --end-date 2023-12-31
    ```
    *Benötigt:* `FRED_API_KEY` in der `.env`-Datei.

### 🎯 Regime Daten Fetcher

#### `regime_data_fetcher/gold_data/gold_data_fetcher.py`
*   **Funktionalität:** Holt historische Golddaten und analysiert deren Safe-Haven-Eigenschaften.
*   **Datenquellen:** Yahoo Finance (für Gold-Futures-Symbol `GC=F` und USD Index `DX-Y.NYB`).
*   **Verarbeitung:** Goldpreise und Volumen werden geladen, gleitende Durchschnitte und Volatilität berechnet. Zusätzlich wird die Korrelation mit dem USD-Index analysiert.
*   **Speicherung:** Die verarbeiteten Golddaten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/regime_data/gold_data/` gespeichert.
*   **Verwendung:**
    ```bash
    python regime_data_fetcher/gold_data/gold_data_fetcher.py --start-date 2022-01-01 --end-date 2023-12-31 --interval 1d
    ```

#### `regime_data_fetcher/mobility_data/mobility_data_fetcher.py`
*   **Funktionalität:** Beschafft Mobilitätsdaten von Google und Apple, die als Indikatoren für die wirtschaftliche Aktivität und das Verhalten der Bevölkerung dienen.
*   **Datenquellen:** Google COVID-19 Community Mobility Reports und Apple Mobility Trends.
*   **Verarbeitung:** Die Daten werden von den jeweiligen Quellen abgerufen, gefiltert, bereinigt und zusammenfassende Metriken wie prozentuale Änderungen in verschiedenen Kategorien (Einzelhandel, Parks, Arbeitsplätze) erstellt.
*   **Speicherung:** Die verarbeiteten Mobilitätsdaten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/regime_data/mobility_data/` gespeichert.
*   **Verwendung:**
    ```bash
    python regime_data_fetcher/mobility_data/mobility_data_fetcher.py --country US --start-date 2022-01-01 --end-date 2023-12-31 --source both
    ```

#### `regime_data_fetcher/vix_data/vix_data_fetcher.py`
*   **Funktionalität:** Holt VIX-Daten (Chicago Board Options Exchange Volatility Index) und analysiert das aktuelle Marktregime (Risikobereitschaft vs. Risikoaversion).
*   **Datenquellen:** Yahoo Finance (für VIX-Symbol `^VIX`).
*   **Verarbeitung:** VIX-Daten werden geladen, gleitende Durchschnitte und Standardabweichungen berechnet, um Marktregime zu identifizieren.
*   **Speicherung:** Die verarbeiteten VIX-Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/regime_data/vix_data/` gespeichert.
*   **Verwendung:**
    ```bash
    python regime_data_fetcher/vix_data/vix_data_fetcher.py --start-date 2022-01-01 --end-date 2023-12-31 --interval 1d
    ```

### 😊 Sentiment Daten Fetcher

#### `sentiment_data_fetcher/google_trends/google_trends_fetcher.py`
*   **Funktionalität:** Sammelt Google Trends Daten für spezifische Suchbegriffe, um das öffentliche Interesse und die Stimmung gegenüber bestimmten Themen oder Währungspaaren zu messen.
*   **Datenquellen:** Google Trends API (`pytrends`).
*   **Verarbeitung:** Die Daten werden abgerufen, in DataFrames umgewandelt und zusätzliche Metriken wie gleitende Durchschnitte und Trendindikatoren berechnet.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/sentiment_data/google_trends/` gespeichert.
*   **Verwendung:**
    ```bash
    python sentiment_data_fetcher/google_trends/google_trends_fetcher.py --keywords "forex trading" "EURUSD" --geo US --start-date 2023-01-01 --end-date 2023-12-31
    ```

#### `sentiment_data_fetcher/news/news_sentiment_fetcher.py`
*   **Funktionalität:** Holt Nachrichtenartikel basierend auf Suchbegriffen und führt eine Sentiment-Analyse durch, um die allgemeine Stimmung in den Nachrichten zu quantifizieren.
*   **Datenquellen:** News API (newsapi.org).
*   **Verarbeitung:** Artikel werden abgerufen, Titel und Beschreibungen werden mit `TextBlob` auf Polarität und Subjektivität analysiert. Schlüsselwörter werden extrahiert und Sentiment-Trends identifiziert.
*   **Speicherung:** Die analysierten Nachrichten-Sentiment-Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/sentiment_data/news_sentiment/` gespeichert.
*   **Verwendung:**
    ```bash
    python sentiment_data_fetcher/news/news_sentiment_fetcher.py --query "forex" --start-date 2023-11-01 --end-date 2023-11-30 --language en
    ```
    *Benötigt:* `NEWS_API_KEY` in der `.env`-Datei.

#### `sentiment_data_fetcher/retail/retail_sentiment_fetcher.py`
*   **Funktionalität:** Beschafft Retail-Sentiment-Daten, die die Positionierung von Kleinanlegern in verschiedenen Währungspaaren widerspiegeln.
*   **Datenquellen:** Simuliert TradingView-Daten (da TradingView keine offizielle API hat, ist dies ein Beispiel).
*   **Verarbeitung:** Das Skript ruft (simulierte) Daten ab und erstellt eine Zusammenfassung der Sentiment-Metriken.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/sentiment_data/retail_sentiment/` gespeichert.
*   **Verwendung:**
    ```bash
    python sentiment_data_fetcher/retail/retail_sentiment_fetcher.py --symbols EURUSD GBPUSD --timeframes 1D 1W
    ```
    *Benötigt:* `TRADINGVIEW_API_KEY` in der `.env`-Datei (für simulierte Nutzung, kann auch ohne API-Key ausgeführt werden).

#### `sentiment_data_fetcher/social_media/social_media_sentiment_fetcher.py`
*   **Funktionalität:** Sammelt Sentiment-Daten aus sozialen Medien (Twitter und Reddit) zu spezifischen Forex-Paaren, um die öffentliche Stimmung zu erfassen.
*   **Datenquellen:** Twitter API (via `tweepy`) und Reddit API (via `praw`).
*   **Verarbeitung:** Tweets und Reddit-Posts werden abgerufen, der Text wird mit `TextBlob` auf Polarität und Subjektivität analysiert.
*   **Speicherung:** Die analysierten Social-Media-Sentiment-Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/sentiment_data/social_media/` gespeichert.
*   **Verwendung:**
    ```bash
    python sentiment_data_fetcher/social_media/social_media_sentiment_fetcher.py --symbols EURUSD GBPUSD --twitter-count 50 --reddit-limit 50
    ```
    *Benötigt:* `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` in der `.env`-Datei.

### 🧮 Volatilitätsdaten Fetcher

#### `volatility_data_fetcher/implied_volatility/implied_volatility_fetcher.py`
*   **Funktionalität:** Holt implizite Volatilitätsdaten für Optionen von Forex-Paaren, die die erwartete zukünftige Volatilität des Marktes widerspiegeln.
*   **Datenquellen:** Yahoo Finance (für Optionsketten).
*   **Verarbeitung:** Optionsdaten werden abgerufen, Call- und Put-Optionen werden verarbeitet und Metriken wie durchschnittliche, minimale und maximale implizite Volatilität berechnet.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/volatility_data/implied_volatility/` gespeichert.
*   **Verwendung:**
    ```bash
    python volatility_data_fetcher/implied_volatility/implied_volatility_fetcher.py --symbols EURUSD=X GBPUSD=X --expiry-date 2024-12-20
    ```

#### `volatility_data_fetcher/realized_volatility/realized_volatility_fetcher.py`
*   **Funktionalität:** Berechnet die realisierte Volatilität historischer Preisdaten für Forex-Paare.
*   **Datenquellen:** Yahoo Finance (für historische Kursdaten).
*   **Verarbeitung:** Historische Schlusskurse werden geladen, logarithmische Renditen berechnet und die realisierte Volatilität über verschiedene gleitende Fenster (z.B. 20, 60, 120 Tage) ermittelt.
*   **Speicherung:** Die berechneten realisierten Volatilitätsdaten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/volatility_data/realized_volatility/` gespeichert.
*   **Verwendung:**
    ```bash
    python volatility_data_fetcher/realized_volatility/realized_volatility_fetcher.py --symbols EURUSD=X USDJPY=X --start-date 2022-01-01 --end-date 2023-12-31 --windows 20 60
    ```

#### `volatility_data_fetcher/volatility_surface/volatility_surface_fetcher.py`
*   **Funktionalität:** Dieses Skript kann verwendet werden, um Daten für die Konstruktion einer Volatilitätsoberfläche zu sammeln und zu verarbeiten. Eine Volatilitätsoberfläche zeigt die implizite Volatilität von Optionen über verschiedene Ausübungspreise und Verfallszeiten hinweg.
*   **Datenquellen:** Yahoo Finance (für Optionsketten, ähnlich wie beim Implied Volatility Fetcher).
*   **Verarbeitung:** Es werden Optionsdaten (Schlagpreise, Verfallsdaten, implizite Volatilitäten) abgerufen und für die Erstellung der Volatilitätsoberfläche vorbereitet.
*   **Speicherung:** Die verarbeiteten Daten werden als CSV-Dateien im Ordner `1.00-Data/forex_data/volatility_data/volatility_surface/` gespeichert.
*   **Verwendung:**
    ```bash
    python volatility_data_fetcher/volatility_surface/volatility_surface_fetcher.py --symbol EURUSD=X --expiry-date 2024-12-20 --strike-range 1.05 1.15
    ```

## 📦 Abhängigkeiten

Die erforderlichen Python-Pakete sind in der `requirements.txt`-Datei aufgeführt. Sie können sie mit dem folgenden Befehl installieren:

```bash
pip install -r requirements.txt
```

Die `requirements.txt` enthält:
```
pandas>=1.5.0
numpy>=1.21.0
requests>=2.28.0
yfinance>=0.2.0
tweepy>=4.12.0
praw>=7.7.0
python-dotenv>=0.19.0
```

## 🔑 API-Schlüssel

Einige Skripte erfordern API-Schlüssel für den Zugriff auf externe Datenquellen. Bitte legen Sie diese in einer `.env`-Datei im Stammverzeichnis des Projekts ab (z.B. `/Users/josua/Documents/Coding/JosiTosi-quant-code/.env`).

Beispiel für eine `.env`-Datei:
```
FRED_API_KEY="IHR_FRED_API_KEY"
BLS_API_KEY="IHR_BLS_API_KEY"
PLANET_API_KEY="IHR_PLANET_API_KEY"
MARINETRAFFIC_API_KEY="IHR_MARINETRAFFIC_API_KEY"
NEWS_API_KEY="IHR_NEWS_API_KEY"
TWITTER_API_KEY="IHR_TWITTER_API_KEY"
TWITTER_API_SECRET="IHR_TWITTER_API_SECRET"
TWITTER_ACCESS_TOKEN="IHR_TWITTER_ACCESS_TOKEN"
TWITTER_ACCESS_TOKEN_SECRET="IHR_TWITTER_ACCESS_TOKEN_SECRET"
REDDIT_CLIENT_ID="IHR_REDDIT_CLIENT_ID"
REDDIT_CLIENT_SECRET="IHR_REDDIT_CLIENT_SECRET"
TRADINGVIEW_API_KEY="IHR_TRADINGVIEW_API_KEY" # Optional für simulierte Daten
```

## 📊 Datenqualität & Standards

Die Skripte sind so konzipiert, dass sie Daten in einem konsistenten Format speichern, um die weitere Verarbeitung zu erleichtern.

### Datenformat-Standards
*   **CSV-Dateien:**
    *   UTF-8 Encoding
    *   Kommagetrennt (`,`)
    *   Header-Zeile obligatorisch
    *   Datum im ISO-Format (YYYY-MM-DD)
    *   Dezimaltrennzeichen: Punkt (`.`)

### Namenskonventionen
Die Ausgabedateien folgen einer klaren Namenskonvention, z.B. `{datentyp}_{quelle}_{start_datum}_{end_datum}.csv` oder `{datentyp}_{symbol}.csv`.

### Qualitätskontrolle
Obwohl die Skripte Rohdaten abrufen, ist es wichtig, separate Qualitätssicherungs- und Bereinigungsprozesse (nicht in diesen Skripten enthalten) durchzuführen, um:
*   Fehlende Datenpunkte zu identifizieren
*   Ausreißer zu erkennen
*   Datenkonsistenz zu überprüfen
*   Doppelte Einträge zu entfernen

## 🚀 Erste Schritte

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/IhrBenutzername/IhrRepositoryname.git
    cd IhrRepositoryname/1.00-Data/forex_data/scripts
    ```
2.  **Virtuelle Umgebung einrichten (empfohlen):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate  # Windows
    ```
3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **`.env`-Datei erstellen:** Erstellen Sie eine Datei namens `.env` im Stammverzeichnis des Projekts und fügen Sie Ihre API-Schlüssel hinzu (siehe Abschnitt "API-Schlüssel" oben).
5.  **Skripte ausführen:** Navigieren Sie zum jeweiligen Skript-Ordner und führen Sie das Skript aus, z.B.:
    ```bash
    python economic_data_fetcher/gdp/gdp_data_fetcher.py --start-date 2020-01-01 --end-date 2023-12-31
    ```
    Stellen Sie sicher, dass Sie sich im `scripts`-Verzeichnis befinden oder den vollständigen Pfad zum Skript angeben. 