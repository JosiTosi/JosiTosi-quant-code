# 🚀 Forex ML Trading: Alternative Datenquellen & Prognosemodelle

Ein Machine Learning Projekt zur Forex-Preisprognose basierend auf alternativen Datenquellen, Sentiment-Analyse, makroökonomischen Indikatoren und fundamentalen Daten.

## 📋 Inhaltsverzeichnis

- [Projektübersicht](#projektübersicht)
- [Datenquellen-Kategorien](#datenquellen-kategorien)
- [ML-Modelle nach Datentyp](#ml-modelle-nach-datentyp)
- [Technologie-Stack](#technologie-stack)
- [Installation & Setup](#installation--setup)
- [Projektstruktur](#projektstruktur)
- [Roadmap](#roadmap)

## 🎯 Projektübersicht

Dieses Projekt nutzt **ausschließlich kostenlose Datenquellen** zur Vorhersage von Forex-Preisbewegungen durch die Kombination von:

- **Sentiment-Analyse** (Social Media, News, Trends)
- **Regime-(Marktphasen, Risk-On/OffErkennung** )
- **Makroökonomische Indikatoren** (BIP, Inflation, Zinsen)
- **FuDaten*fe, Handel, Wirtscnda* (Rohstofmentale haftsaktivität)

### 🎯 Zielwährungspaare

| Kategorie | Währungspaare | Schwerpunkt |
|-----------|---------------|-------------|
| **Majors** | EUR/USD, GBP/USD, USD/JPY, USD/CHF | Sentiment & Makro |
| **AUD/USD, USD/CAD, NZDCommodities** | /USD | Rohstoffpreise & Handel |
| **Risk Pairs** | AUD/JPY, USD/CNY, USD/ZAR | Risk-On/Off Regime |

---

## 📊 Datenquellen-Kategorien

### 1. 💬 **Sentiment-Daten**

**Zwund Risikoneieck**: Marktstimmung gung erfassen

| Datenquelle | API/Tool | Forex-Einfluss |
|-------------|----------|----------------|
| ends | `pytrends` | EUR/USD,Google Tr GBP/USD, USD/JPY |
| Reddit Sentiment | `praw` (Reddit API) | AUD/JPY, USD/CHF |
| Twitter/X Mentions | `snscrape` | Alle Major-Paare |
| News Sentiment | `newsapi` | GBP/USD (Brexit), USD/JPY |

**Indikatoren**:
- Risk-On/Risk-Off Score
- Währungs-spezifische Sentiment-Scores
- Volatilitäts-Erwartungen

### 2. 🌍 **Regime-Daten**

**Zweck**: Marktphasen und strukturelle Änderungen identifizieren

| Datenquelle | API/Tool | Anwendung |
|-------------|----------|-----------|
| VIX (Volatilität) | `yfinance` | Risk-Off Regime |
| Gold/Safe Haven | `yfinance` | USD/CHF, USD/JPY |
| Zinsdifferenzen | FRED API | EUR/USD, GBP/USD |
| Mobilitätsdaten | Google/Apple APIs | Post-Lockdown Recovery |

**Regime-Typen**:
- **Risk-On**: Wachstumsoptimismus → AUD, NZD stark
- **Risk-Off**: Flucht in Safe Havens → USD, CHF, JPY stark
- **Inflation Regime**: Rohstoffwährungen profitieren
- **Rezession**: Flucht in Staatsanleihen

### 3. 📈 **Makroökonomische Daten**

**Zweck**: Langfristige Wirtschaftstrends und Zentralbankpolitik

| Datenquelle | API/Tool | Forex-Relevanz |
|-------------|----------|----------------|
| FRED (Fed St. Louis) | `fredapi` | USD-Pairs (alle) |
| Weltbank Open Data | `wbdata` | Emerging Markets |
| OECD Daten | OECD API | EUR/USD, GBP/USD |
| BIS Daten | Web Scraping | Globale Liquidität |

**Key Indikatoren**:
- BIP-Wachstum (YoY)
- Inflationsraten (CPI, PCE)
- Leitzinsen & Zinserwartungen
- Arbeitslosenquoten
- Handelsbilanzen

### 4. 🏭 **Fundamentale/Alternative Daten**

**Zweck**: Reale Wirtschaftsaktivität messen

| Datenquelle | Tool/API | Währungseinfluss |
|-------------|----------|------------------|
| Satellitenbilder (Parkplätze) | Planet Labs | USD (Konsum) |
| Containerschiff-Traffic | MarineTraffic | AUD/USD, USD/CNH |
| Stromverbrauch/Nachtlicht | NASA VIIRS | USD/CNY, USD/INR |
| Rohstoffpreise | `yfinance`, Quandl | USD/CAD, AUD/USD |
| Kreditkartendaten | Öffentliche Aggregate | EUR/USD, USD/JPY |

**Indikatoren**:
- Export/Import-Aktivität
- Industrieproduktion (Proxy)
- Konsumverhalten
- Rohstoffnachfrage

---

## 🤖 ML-Modelle nach Datentyp

### 1. **Sentiment-Analyse** → NLP & Classification

**Empfohlene Modelle**:
- **VADER Sentiment**: Für Social Media Text
- **FinBERT**: Für Finanz-News (Hugging Face)
- **Logistic Regression**: Sentiment → Preis-Richtung
- **LSTM**: Zeitreihen-Sentiment → Preis

### 2. **Regime-Erkennung** → Clustering & Classification

**Empfohlene Modelle**:
- **Hidden Markov Models (HMM)**: Marktregime-Detection
- **Gaussian Mixture Models**: Volatilitäts-Cluster
- **K-Means Clustering**: Risk-On/Off Klassifizierung
- **Random Forest**: Multi-Feature Regime Prediction

### 3. **Makroökonomische Prognose** → Time Series & Regression

**Empfohlene Modelle**:
- **ARIMA/SARIMA**: Zinsraten, Inflation
- **VAR (Vector Autoregression)**: Multi-Country Analysis
- **XGBoost/LightGBM**: Feature-rich Regression
- **Prophet**: Trend + Seasonality (Facebook)

### 4. **Fundamentale Daten** → Regression & Deep Learning

**Empfohlene Modelle**:
- **Linear/Ridge Regression**: Rohstoff → FX Correlation
- **CNN**: Satellitenbild-Analyse
- **LSTM/GRU**: Multivariate Zeitreihen
- **Ensemble Methods**: Kombination aller Features

### 5. **Multi-Modal Fusion** → Ensemble Learning

**Kombinationsansätze**:
- **Stacking**: Meta-Learner kombiniert Vorhersagen
- **Weighted Averaging**: Gewichtung nach Modell-Performance
- **Bayesian Model Averaging**: Unsicherheits-Quantifizierung
- **Neural Network Ensemble**: Deep Learning Fusion

---

## 💻 Technologie-Stack

### **Data Collection**
- `pytrends` - Google Trends
- `praw` - Reddit API
- `snscrape` - Twitter Scraping
- `fredapi` - FRED Economic Data
- `yfinance` - Financial Data
- `requests` - Web APIs
- `beautifulsoup4` - Web Scraping

### **Data Processing**
- `pandas` - Data Manipulation
- `numpy` - Numerical Computing
- `scipy` - Statistical Functions
- `scikit-learn` - Machine Learning

### **ML & Deep Learning**
- `xgboost` - Gradient Boosting
- `lightgbm` - Microsoft Gradient Boosting
- `statsmodels` - Time Series Analysis
- `hmmlearn` - Hidden Markov Models
- `tensorflow` - Neural Networks
- `pytorch` - Neural Networks (Alternative)
- `transformers` - Hugging Face NLP Models

### **Visualization & Analysis**
- `plotly` - Interactive Charts
- `matplotlib` - Static Plots
- `seaborn` - Statistical Visualization
- `ta` - Technical Analysis
- `pyfolio` - Portfolio Analysis

---

## 🛠️ Installation & Setup

### 1. **Repository klonen**
```bash
git clone https://github.com/username/forex-ml-trading.git
cd forex-ml-trading
```

### 2. **Virtual Environment erstellen**
```bash
python -m venv forex_env
source forex_env/bin/activate  # Linux/Mac
# forex_env\Scripts\activate   # Windows
```

### 3. **Dependencies installieren**
```bash
pip install -r requirements.txt
```

### 4. **Konfiguration**
```bash
cp config/config_template.yaml config/config.yaml
# API-Keys eintragen (Reddit, News, etc.)
```

### 5. **Erstes Datensammeln**
```bash
python scripts/collect_data.py --source sentiment --pair EURUSD
```

---

## 📁 Projektstruktur

```
forex-ml-trading/
│
├── 📊 data/
│   ├── raw/                 # Rohdaten
│   ├── processed/           # Bereinigte Daten
│   └── features/            # Feature Engineering
│
├── 📝 scripts/
│   ├── collect_data.py      # Datensammlung
│   ├── preprocess.py        # Datenbereinigung
│   ├── feature_engineering.py
│   └── train_models.py      # Modell-Training
│
├── 🤖 models/
│   ├── sentiment/           # Sentiment-Modelle
│   ├── regime/              # Regime-Detection
│   ├── macro/               # Makro-Prognose
│   └── ensemble/            # Ensemble-Modelle
│
├── 📈 analysis/
│   ├── backtesting/         # Backtest-Ergebnisse
│   ├── visualization/       # Charts & Plots
│   └── reports/             # Analyse-Reports
│
├── 🔧 config/
│   ├── config.yaml          # Konfiguration
│   └── model_configs/       # Modell-Parameter
│
├── 📚 notebooks/
│   ├── exploratory/         # EDA Notebooks
│   ├── modeling/            # Modell-Entwicklung
│   └── backtesting/         # Backtest-Notebooks
│
└── 📋 requirements.txt
```

---



## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` Datei für Details.

---
