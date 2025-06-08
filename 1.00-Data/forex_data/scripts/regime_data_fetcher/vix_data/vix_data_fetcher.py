import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

class VIXDataFetcher:
    def __init__(self):
        """
        Initialisiert den VIX Data Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/regime_data/vix_data")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def fetch_vix_data(self, start_date=None, end_date=None, interval='1d'):
        """
        Holt VIX-Daten von Yahoo Finance
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            interval (str, optional): Datenintervall ('1d', '1h', etc.)
        """
        try:
            with self.console.status("[bold blue]Lade VIX-Daten..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Hole VIX-Daten
                vix = yf.Ticker("^VIX")
                hist = vix.history(start=start_date, end=end_date, interval=interval)
                
                if hist.empty:
                    self.console.print("[yellow]Keine VIX-Daten verfügbar für den angegebenen Zeitraum[/yellow]")
                    return
                
                # Berechne zusätzliche Metriken
                data = pd.DataFrame()
                data['date'] = hist.index
                data['vix'] = hist['Close']
                data['vix_ma20'] = hist['Close'].rolling(window=20).mean()
                data['vix_ma50'] = hist['Close'].rolling(window=50).mean()
                data['vix_std20'] = hist['Close'].rolling(window=20).std()
                
                # Speichere die Daten
                output_file = self.base_path / f"vix_data_{interval}.csv"
                data.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="VIX Daten Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{data['date'].min().strftime('%Y-%m-%d')} bis {data['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Datenpunkte", str(len(data)))
                table.add_row("Aktueller VIX", f"{data['vix'].iloc[-1]:.2f}")
                table.add_row("Durchschnittlicher VIX", f"{data['vix'].mean():.2f}")
                table.add_row("Maximaler VIX", f"{data['vix'].max():.2f}")
                table.add_row("Minimaler VIX", f"{data['vix'].min():.2f}")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der VIX-Daten: {str(e)}[/red]")
    
    def analyze_regime(self, data):
        """
        Analysiert das aktuelle Marktregime basierend auf VIX-Daten
        
        Args:
            data (pd.DataFrame): VIX-Daten
        """
        current_vix = data['vix'].iloc[-1]
        vix_ma20 = data['vix_ma20'].iloc[-1]
        vix_std20 = data['vix_std20'].iloc[-1]
        
        # Regime-Klassifizierung
        if current_vix > vix_ma20 + vix_std20:
            regime = "Risk-Off (Hohe Volatilität)"
        elif current_vix < vix_ma20 - vix_std20:
            regime = "Risk-On (Niedrige Volatilität)"
        else:
            regime = "Neutral"
            
        return regime

def main():
    parser = argparse.ArgumentParser(description='VIX Data Fetcher')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--interval', default='1d', help='Datenintervall (1d, 1h, etc.)')
    
    args = parser.parse_args()
    
    try:
        fetcher = VIXDataFetcher()
        fetcher.fetch_vix_data(
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 