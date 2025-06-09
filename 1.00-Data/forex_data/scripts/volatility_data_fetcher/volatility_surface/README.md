# 📈 Volatility Surface für den Forex-Markt

Dieses Projekt generiert, speichert und visualisiert eine **Volatility Surface** für ein Forex-Währungspaar (z. B. EUR/USD). Ziel ist es, eine visuelle und datenbasierte Grundlage zur Analyse von Marktvolatilität über verschiedene Preisniveaus und Zeitpunkte hinweg zu schaffen – ein wertvolles Werkzeug für diskretionäre und quantitative Trader.

---

## 🔍 Was ist eine Volatility Surface?

Die **Volatility Surface** (deutsch: *Volatilitätsoberfläche*) ist ein 3D-Modell, das darstellt, wie sich das Handelsvolumen oder die Volatilität eines Marktes in Abhängigkeit von:

- dem Preisniveau (z. B. EUR/USD = 1.0543),
- dem Zeitpunkt (z. B. 12:00 Uhr, 13:00 Uhr, …)

verhält.  

Diese Oberfläche wird in Form einer Matrix oder Heatmap dargestellt. Jeder Punkt auf der Oberfläche zeigt, wie aktiv der Markt zu einem bestimmten Zeitpunkt auf einem bestimmten Preisniveau war.

> 💡 Je stärker die Volatilität auf bestimmten Preisniveaus konzentriert ist, desto eher kann dies auf Liquiditätszonen, Unterstützungen/Widerstände oder institutionelles Interesse hindeuten.

---

## 📊 Warum ist das beim Forex Trading hilfreich?

Im Forex-Markt, wo keine zentrale Börse existiert, fehlt es oft an tieferem Einblick in das Orderbuch. Die Volatility Surface kann helfen, dieses Informationsdefizit auszugleichen, indem sie zeigt:

- **Wo sich Preisbereiche mit hohem Handelsinteresse befinden**  
  → z. B. potenzielle *liquidity pools*, magnetische Zonen, relevante Levels

- **Wie sich Volumen über die Zeit verteilt**  
  → Erkennung von News-getriebenen Bewegungen oder asiatischen/europäischen/US-Session Peaks

- **Welche Preiszonen regelmäßig getestet werden**  
  → hilft bei der Einschätzung zukünftiger Preisreaktionen

Diese Analyse bietet einen quantitativen Vorteil gegenüber rein visuellen oder subjektiven Support/Resistance-Zeichnungen.

---

## 🧠 Projektstruktur
volatility_surface/
├── volatility_surface_fetcher.py   # Simuliert oder lädt die Daten (Preis-Zeit-Volumen-Matrix)
├── volatility_visualizer.py       # Visualisiert die Volatility Surface als 3D-Plot oder Heatmap
└── README.md                       # Projektbeschreibung


---

## ⚙️ Skripte erklärt

### `volatility_surface_fetcher.py`

- Simuliert eine Volatility Surface durch:
  - Erzeugen künstlicher Preislevel (z. B. 1.0500 bis 1.0600)
  - Erzeugen eines Zeitrasters (z. B. stündlich über 100 Schritte)
  - Zufälliges oder reales Handelsvolumen je Preis/Zeit
- Speichert die generierten Daten als `.csv` zur späteren Analyse

> Kann erweitert werden, um echte Daten von Brokern oder APIs zu laden.

---

### `volatility_visualizer.py`

- Liest die `.csv`-Datei mit der Volatility Surface
- Erstellt eine anschauliche Visualisierung (z. B. 3D-Surface oder Heatmap)
- Optional: Markiert Zonen mit hoher Aktivität / Liquidität

---

## 🛠️ Mögliche Erweiterungen

- Verwendung echter Tick-Daten oder Orderbuchdaten
- Integration in Tradingview oder Webinterface
- Automatische Erkennung von „Hot Zones“
- Kombination mit Indikatoren (FVGs, Fibonacci, COT-Daten etc.)

---

## 📬 Kontakt & Lizenz

Dieses Projekt ist aktuell privat und dient nur Forschungs- und Analysezwecken. Du kannst es gern forken oder erweitern.

---