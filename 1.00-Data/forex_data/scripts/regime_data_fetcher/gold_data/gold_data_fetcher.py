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

class GoldDataFetcher:
    def __init__(self):
        """
        Initialisiert den Gold Data Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/regime_data/gold_data")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def fetch_gold_data(self, start_date=None, end_date=None, interval='1d'):
        """
        Holt Gold-Daten von Yahoo Finance
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            interval (str, optional): Datenintervall ('1d', '1h', etc.)
        """
        try:
            with self.console.status("[bold blue]Lade Gold-Daten..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Hole Gold-Daten
                gold = yf.Ticker("GC=F")  # Gold Futures
                hist = gold.history(start=start_date, end=end_date, interval=interval)
                
                if hist.empty:
                    self.console.print("[yellow]Keine Gold-Daten verfügbar für den angegebenen Zeitraum[/yellow]")
                    return
                
                # Berechne zusätzliche Metriken
                data = pd.DataFrame()
                data['date'] = hist.index
                data['price'] = hist['Close']
                data['volume'] = hist['Volume']
                data['ma20'] = hist['Close'].rolling(window=20).mean()
                data['ma50'] = hist['Close'].rolling(window=50).mean()
                data['volatility'] = hist['Close'].rolling(window=20).std()
                
                # Berechne Korrelation mit USD
                usd_index = yf.Ticker("DX-Y.NYB")  # US Dollar Index
                usd_hist = usd_index.history(start=start_date, end=end_date, interval=interval)
                if not usd_hist.empty:
                    data['usd_correlation'] = data['price'].rolling(window=20).corr(usd_hist['Close'])
                
                # Speichere die Daten
                output_file = self.base_path / f"gold_data_{interval}.csv"
                data.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Gold Daten Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{data['date'].min().strftime('%Y-%m-%d')} bis {data['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Datenpunkte", str(len(data)))
                table.add_row("Aktueller Preis", f"${data['price'].iloc[-1]:.2f}")
                table.add_row("Durchschnittlicher Preis", f"${data['price'].mean():.2f}")
                table.add_row("Maximaler Preis", f"${data['price'].max():.2f}")
                table.add_row("Minimaler Preis", f"${data['price'].min():.2f}")
                table.add_row("Durchschnittliches Volumen", f"{data['volume'].mean():.0f}")
                if 'usd_correlation' in data.columns:
                    table.add_row("USD Korrelation (20 Tage)", f"{data['usd_correlation'].iloc[-1]:.2f}")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Gold-Daten: {str(e)}[/red]")
    
    def analyze_safe_haven(self, data):
        """
        Analysiert die Safe-Haven-Eigenschaften von Gold
        
        Args:
            data (pd.DataFrame): Gold-Daten
        """
        current_price = data['price'].iloc[-1]
        ma20 = data['ma20'].iloc[-1]
        volatility = data['volatility'].iloc[-1]
        
        # Safe-Haven-Analyse
        if current_price > ma20 + volatility:
            status = "Starkes Safe-Haven-Verhalten"
        elif current_price < ma20 - volatility:
            status = "Schwaches Safe-Haven-Verhalten"
        else:
            status = "Neutrales Verhalten"
            
        return status

def main():
    parser = argparse.ArgumentParser(description='Gold Data Fetcher')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--interval', default='1d', help='Datenintervall (1d, 1h, etc.)')
    
    args = parser.parse_args()
    
    try:
        fetcher = GoldDataFetcher()
        fetcher.fetch_gold_data(
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 