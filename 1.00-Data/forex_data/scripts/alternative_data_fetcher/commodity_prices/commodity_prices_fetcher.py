import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv
import yfinance as yf
import requests
from fredapi import Fred

class CommodityPricesFetcher:
    def __init__(self):
        """
        Initialisiert den Commodity Prices Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/commodity_prices")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade FRED API-Key
        self.fred_api_key = os.getenv('FRED_API_KEY')
        if not self.fred_api_key:
            self.console.print("[yellow]Warnung: Kein FRED_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere FRED Client
        if self.fred_api_key:
            self.fred = Fred(api_key=self.fred_api_key)
        
        # Definiere Standard-Rohstoffe
        self.default_commodities = {
            'GC=F': 'Gold',
            'SI=F': 'Silber',
            'PL=F': 'Platin',
            'PA=F': 'Palladium',
            'CL=F': 'Rohöl',
            'BZ=F': 'Brent',
            'NG=F': 'Erdgas',
            'ZC=F': 'Mais',
            'ZW=F': 'Weizen',
            'ZS=F': 'Sojabohnen',
            'KC=F': 'Kaffee',
            'CT=F': 'Baumwolle',
            'CC=F': 'Kakao',
            'SB=F': 'Zucker',
            'LBS=F': 'Holz'
        }
    
    def fetch_yahoo_prices(self, symbols, start_date=None, end_date=None):
        """
        Holt Rohstoffpreise von Yahoo Finance
        
        Args:
            symbols (list): Liste von Yahoo Finance Symbolen
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Rohstoffpreise von Yahoo Finance..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Hole Daten
                data = yf.download(
                    symbols,
                    start=start_date,
                    end=end_date,
                    group_by='ticker'
                )
                
                return data
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Yahoo Finance Daten: {str(e)}[/red]")
            return None
    
    def fetch_fred_prices(self, series_ids, start_date=None, end_date=None):
        """
        Holt Rohstoffpreise von FRED
        
        Args:
            series_ids (list): Liste von FRED Series IDs
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Rohstoffpreise von FRED..."):
                if not self.fred_api_key:
                    self.console.print("[red]Fehler: Kein FRED API-Key verfügbar[/red]")
                    return None
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Hole Daten für jede Series
                data = {}
                for series_id in series_ids:
                    series_data = self.fred.get_series(
                        series_id,
                        start_date=start_date,
                        end_date=end_date
                    )
                    data[series_id] = series_data
                
                return pd.DataFrame(data)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der FRED Daten: {str(e)}[/red]")
            return None
    
    def analyze_commodity_prices(self, data, commodity_name):
        """
        Analysiert die Rohstoffpreisdaten
        
        Args:
            data (pd.DataFrame): Preisdaten
            commodity_name (str): Name des Rohstoffs
        """
        try:
            if data is None or data.empty:
                return None
            
            # Berechne Metriken
            metrics = {
                'current_price': data['Close'].iloc[-1],
                'price_change_1d': data['Close'].pct_change().iloc[-1],
                'price_change_1w': data['Close'].pct_change(5).iloc[-1],
                'price_change_1m': data['Close'].pct_change(21).iloc[-1],
                'volatility_1m': data['Close'].pct_change().rolling(21).std().iloc[-1],
                'volume_avg': data['Volume'].mean(),
                'high_1m': data['High'].rolling(21).max().iloc[-1],
                'low_1m': data['Low'].rolling(21).min().iloc[-1]
            }
            
            return metrics
            
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Datenanalyse: {str(e)}[/red]")
            return None
    
    def process_commodities(self, symbols=None, start_date=None, end_date=None):
        """
        Verarbeitet mehrere Rohstoffe
        
        Args:
            symbols (list, optional): Liste von Yahoo Finance Symbolen
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            # Verwende Standard-Symbole, wenn keine angegeben wurden
            if not symbols:
                symbols = list(self.default_commodities.keys())
            
            # Hole Preisdaten
            price_data = self.fetch_yahoo_prices(symbols, start_date, end_date)
            
            if price_data is not None:
                results = []
                
                with Progress() as progress:
                    task = progress.add_task("[cyan]Analysiere Rohstoffe...", total=len(symbols))
                    
                    for symbol in symbols:
                        if symbol in self.default_commodities:
                            commodity_name = self.default_commodities[symbol]
                            
                            # Extrahiere Daten für diesen Rohstoff
                            if len(symbols) > 1:
                                commodity_data = price_data[symbol]
                            else:
                                commodity_data = price_data
                            
                            # Analysiere die Daten
                            metrics = self.analyze_commodity_prices(commodity_data, commodity_name)
                            
                            if metrics:
                                results.append({
                                    'symbol': symbol,
                                    'name': commodity_name,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    **metrics
                                })
                        
                        progress.update(task, advance=1)
                
                # Konvertiere zu DataFrame
                if results:
                    df = pd.DataFrame(results)
                    
                    # Speichere die Daten
                    output_file = self.base_path / f"commodity_prices_{start_date}_{end_date}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title="Rohstoffpreis-Analyse Zusammenfassung")
                    table.add_column("Rohstoff", style="cyan")
                    table.add_column("Aktueller Preis", style="green")
                    table.add_column("1T Änderung", style="green")
                    table.add_column("1M Volatilität", style="green")
                    
                    for _, row in df.iterrows():
                        table.add_row(
                            row['name'],
                            f"${row['current_price']:.2f}",
                            f"{row['price_change_1d']:.1%}",
                            f"{row['volatility_1m']:.1%}"
                        )
                    
                    table.add_row("Speicherort", str(output_file), "", "")
                    
                    self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Commodity Prices Fetcher')
    parser.add_argument('--symbols', nargs='+', help='Liste von Yahoo Finance Symbolen')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        fetcher = CommodityPricesFetcher()
        fetcher.process_commodities(
            symbols=args.symbols,
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 