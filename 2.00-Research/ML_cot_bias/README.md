# COT ML Model - Market Bias Prediction

Ein Machine Learning Modell zur Analyse von Commitment of Traders (COT) Daten für die Vorhersage von Marktbias und kurzfristigen Marktbewegungen (3-5 Tage).

## Projekt Übersicht

Dieses Projekt entwickelt ein ML-System, das COT-Daten verarbeitet und Marktbias erkennt, um eine quantitative Edge gegenüber manueller COT-Interpretation zu schaffen.

## Zielsetzung

- Automatisierte Analyse von COT-Daten
- Erkennung von Marktbias für die nächsten 3-5 Tage
- Identifikation optimaler Einstiegspunkte
- Überlegenheit gegenüber manueller COT-Analyse

## Daten und Features

### COT-Grunddaten
- **Commercial/Hedger Positionen** - Smart Money Indikatoren
- **Large Speculator Positionen** - Institutionelle Trader
- **Small Speculator Positionen** - Retail Trader
- **Net-Positionen** und deren Veränderungen
- **Relative Positionsgrößen** (% der Open Interest)

### Abgeleitete Features
- **Commitment Index** - Commercial vs. Speculator Ratio
- **Positionsextremes** - Perzentile über Rolling Windows
- **Momentum** der Positionsveränderungen
- **Divergenzen** zwischen COT und Preisbewegung
- **Saisonale Adjustierungen** - Elimination vorhersagbarer Zyklen
  - X-12-ARIMA Saisonbereinigung
  - STL Decomposition für Trend-Saison-Zerlegung
  - Anomalie-Detection bei Abweichungen von saisonalen Mustern
- **Regime-Indicators** - Hidden Markov Model States
- **Cross-Market Relationships** - COT-Correlations zwischen verwandten Märkten

## Modellarchitektur

### Core Architecture: Hybrid Foundation Model + Custom Design

#### **Primary Model: Chronos Foundation Model (2024) + Custom Extensions**

**Chronos Foundation Layer:**
- Pre-trained auf massive Zeitreihen-Datasets
- Tokenisierung von COT-Werten durch Skalierung und Quantisierung
- State-of-the-Art Performance als Basis

**Custom Multi-Modal Transformer Stack:**
```
Input ti-StreLayer: Mulam COT Features
├── Chronos Foundation (pre-trained backbone)
├── Custom Attention Layers (COT-specific patterns)
├── Cross-Modal Fusion (COT + Price + Volume)
├── Temporal Convolution Network (TCN)
└── Multi-Head Output (Direction + Confidence + Timing)
```

#### **Edge-Creating Components**

**A) Regime-Aware Architecture:**
- Separate Modell-Weights für verschiedene Marktregime
- Automatische Regime-Detection mit Hidden Markov Models
- Adaptive Learning Rates basierend auf Marktvolatilität

**B) Asymmetric Loss Function:**
- Higher penalty für falsche High-Confidence Predictions
- Reward für frühe Trend-Erkennung
- Penalty für Late-Entry Signals
- Trading-optimiert statt Accuracy-optimiert

**C) Meta-Learning Layer:**
- Lernt, welche COT-Patterns in verschiedenen Marktphasen funktionieren
- Schnelle Adaptation an neue Marktstrukturen
- Few-Shot Learning für seltene Marktereignisse

### Multi-Horizon Ensemble
- **3-Tage Modell** - High Frequency Signals für schnelle Einstiege
- **7-Tage Modell** - Medium Term Bias für Hauptpositionen
- **21-Tage Modell** - Structural Changes und Regime-Shifts

### Confidence-Based Architecture
- Modell Output: Direction + Confidence Score + Timing
- Größere Positionen bei High-Confidence Signals
- Risk-Adjusted Position Sizing basierend auf Modell-Uncertainty

### Fallback Models (Baseline Comparison)
1. **XGBoost/LightGBM** - Feature Importance Baseline
2. **LSTM** - Sequential Pattern Baseline  
3. **Standard Transformer** - Attention Mechanism Baseline

## Datenquellen

### Primäre Quellen
- **CFTC Weekly Reports** - Offizielle COT Daten
- **Disaggregated COT** - Detaillierte Futures-Daten
- **Legacy COT** - Breiterer Marktüberblick

### Zusätzliche Daten
- Preisdaten der entsprechenden Instrumente
- Volatilitätsindikatoren
- Makroökonomische Faktoren (optional)

## Target Definition

### Prediction Targets
- **3-5 Tage Forward Returns** - Hauptziel
- **Directional Bias** - Long/Short/Neutral Klassifikation
- **Volatility-adjusted Returns** - Risikoadjustierte Performance

### Output Format
- Wahrscheinlichkeiten für Marktrichtung
- Confidence Levels
- Empfohlene Positionsgrößen

## Evaluation Metriken

### Performance Metriken
- **Sharpe Ratio** der Predictions (primäre Metrik)
- **Information Ratio** - Risk-adjusted Excess Returns
- **Calmar Ratio** - Return/Max Drawdown
- **Hit Rate** bei verschiedenen Confidence Levels
- **Profit Factor** - Gross Profit/Gross Loss
- **Maximum Drawdown** Metriken
- **Alpha Generation** - Excess Return über Benchmark
- **Trade Efficiency** - Avg Win/Avg Loss Ratio
- **Regime-Specific Performance** - Performance in verschiedenen Marktphasen

### Advanced Evaluation
- **Cross-Validation** über verschiedene Marktzyklen
- **Regime-Aware Backtesting** - Getrennte Evaluation pro Marktregime
- **Adversarial Testing** - Robustheit gegen Market Manipulation
- **Confidence Calibration** - Accuracy der Confidence Scores
- **Feature Attribution** - Welche COT-Features treiben Performance

### Backtesting
- Out-of-Sample Testing
- Walk-Forward Analyse
- Stress Testing in verschiedenen Marktregimen

### Technische Implementierung

### Entwicklungsumgebung
```
Python 3.9+
pandas, numpy - Datenverarbeitung
scikit-learn - ML Grundlagen
xgboost, lightgbm - Gradient Boosting (Baseline)
transformers, chronos - Foundation Models
pytorch/tensorflow - Deep Learning Framework
ta-lib - Technical Analysis Features
matplotlib, seaborn, plotly - Visualisierung
```

### Spezielle Libraries für Advanced Architecture
```
huggingface-hub - Chronos Model Access
optuna - Hyperparameter Optimization
wandb - Experiment Tracking
ray[tune] - Distributed Training
```

### Projektstruktur
```
cot-ml-model/
├── data/
│   ├── raw/          # Rohe COT Daten
│   ├── processed/    # Verarbeitete Features
│   └── external/     # Zusätzliche Datenquellen
├── src/
│   ├── data/         # Datenverarbeitung
│   ├── features/     # Feature Engineering
│   ├── models/       # ML Modelle
│   └── evaluation/   # Backtesting & Evaluation
├── notebooks/        # Jupyter Notebooks für EDA
├── configs/          # Konfigurationsdateien
└── results/          # Ergebnisse und Reports
```

## Roadmap

### Phase 1: Foundation Setup
- [ ] Chronos Foundation Model Setup und Fine-tuning
- [ ] COT Daten Download automatisieren
- [ ] Advanced Feature Engineering Pipeline
- [ ] Regime Detection Implementation
- [ ] Explorative Datenanalyse mit Multi-Modal Approach

### Phase 2: Core Model Development
- [ ] Custom Attention Layers für COT-Patterns
- [ ] Cross-Modal Fusion Architecture
- [ ] Asymmetric Loss Function Implementation
- [ ] Meta-Learning Layer Integration
- [ ] Multi-Horizon Ensemble Setup

### Phase 3: Advanced Optimization
- [ ] Confidence-Based Position Sizing
- [ ] Regime-Aware Training
- [ ] Hyperparameter Optimization mit Optuna
- [ ] Adversarial Robustness Testing
- [ ] Cross-Market Feature Integration

### Phase 3: Backtesting
- [ ] Out-of-Sample Testing
- [ ] Performance Evaluation
- [ ] Risk Management Integration

### Phase 4: Production
- [ ] Real-time Daten Pipeline
- [ ] Automated Trading Signals
- [ ] Monitoring & Alerting

## Competitive Edge und Alpha Generation

### Technische Überlegenheit
- **Foundation Model Basis:** Nutzt pre-trained Chronos für sofortige State-of-the-Art Performance
- **Custom COT Architecture:** Speziell für COT-Pattern optimierte Attention-Mechanismen
- **Multi-Modal Intelligence:** Intelligente Fusion verschiedener Datenquellen
- **Regime Adaptability:** Automatische Anpassung an verschiedene Marktphasen

### Alpha-Generating Advantages
- **Asymmetric Optimization:** Trading-optimiert statt nur Accuracy-optimiert
- **Confidence-Based Sizing:** Größere Positionen bei höherer Modell-Sicherheit
- **Early Signal Detection:** Meta-Learning für schnelle Adaptation an neue Patterns
- **Multi-Horizon Arbitrage:** Verschiedene Zeithorizonte für maximale Opportunity-Capture

### Edge über andere Algo-Trader
- **Foundation Model Integration:** Mehrjähriger Technologie-Vorsprung
- **Saisonale Anomalie-Detection:** Profit aus Abweichungen von Standard-Mustern  
- **Regime-Aware Training:** Robustheit bei Market-Regime-Changes
- **Advanced Feature Engineering:** Cross-Market COT-Relationships und komplexe Derivate

### Datenrisiken
- COT Daten sind weekly delayed
- Strukturelle Marktveränderungen
- Datenverfügbarkeit verschiedener Instrumente

### Modellrisiken
- Overfitting auf historische Patterns
- Regime Changes nicht erfasst
- Limited Lookback für seltene Events

## Getting Started

1. **Environment Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Daten Download**
   ```bash
   python src/data/download_cot_data.py
   ```

3. **Feature Engineering**
   ```bash
   python src/features/build_features.py
   ```

4. **Modell Training**
   ```bash
   python src/models/train_model.py
   ```

## Kontakt

Für Fragen und Verbesserungsvorschläge zum Projekt.

---

**Disclaimer:** Dieses Modell dient ausschließlich zu Forschungszwecken. Trading birgt erhebliche Risiken und vergangene Performance ist keine Garantie für zukünftige Ergebnisse.