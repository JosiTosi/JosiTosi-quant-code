import pandas as pd
import requests
from datetime import datetime
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

class InterestRatesFetcher:
    def __init__(self, api_key=None):
        """
        Initialisiert den Interest Rates Fetcher
        
        Args:
            api_key (str, optional): FRED API Key. Wenn nicht angegeben, wird versucht, ihn aus der .env Datei zu laden.
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/economic_data/interest_rates")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Lade API Key
        load_dotenv()
        self.api_key = api_key or os.getenv('FRED_API_KEY')
        if not self.api_key:
            self.console.print("[red]Kein FRED API Key gefunden![/red]")
            self.console.print("Bitte setzen Sie den API Key in der .env Datei oder übergeben Sie ihn als Parameter.")
            raise ValueError("FRED API Key fehlt")
        
    def fetch_fred_rates(self, series_id, start_date, end_date):
        """
        Holt Zinsdaten von der FRED API
        
        Args:
            series_id (str): FRED Series ID
            start_date (str): Startdatum im Format YYYY-MM-DD
            end_date (str): Enddatum im Format YYYY-MM-DD
        """
        url = f"https://api.stlouisfed.org/fred/series/observations"
        
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date
        }
        
        try:
            with self.console.status(f"[bold blue]Lade Daten für {series_id}..."):
                response = requests.get(url, params=params)
                data = response.json()
            
            if 'observations' in data:
                df = pd.DataFrame(data['observations'])
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                output_file = self.base_path / f"fred_{series_id}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title=f"Zinsdaten für {series_id}")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Anzahl Datenpunkte", str(len(df)))
                table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d')} bis {df['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Aktueller Zinssatz", f"{df['value'].iloc[-1]:.2f}%")
                table.add_row("Durchschnittlicher Zinssatz", f"{df['value'].mean():.2f}%")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
            else:
                self.console.print(f"[red]Fehler beim Abrufen der Daten: {data.get('error_message', 'Unbekannter Fehler')}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim API-Aufruf: {str(e)}[/red]")
    
    def fetch_interest_rates(self, start_date=None, end_date=None, series_ids=None):
        """
        Hauptfunktion zum Abrufen aller Zinsdaten
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            series_ids (dict, optional): Dictionary mit Series IDs und Beschreibungen
        """
        # Standardwerte
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now().replace(year=datetime.now().year-5)).strftime('%Y-%m-%d')
        if not series_ids:
            series_ids = {
                'FEDFUNDS': 'Federal Funds Effective Rate',
                'DGS10': '10-Year Treasury Constant Maturity Rate',
                'DGS2': '2-Year Treasury Constant Maturity Rate',
                'DGS30': '30-Year Treasury Constant Maturity Rate',
                'DFF': 'Federal Funds Rate',
                'EFFR': 'Effective Federal Funds Rate'
            }
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Lade Zinsdaten...", total=len(series_ids))
            
            for series_id, description in series_ids.items():
                self.console.print(f"\n[bold blue]Lade Daten für {description} ({series_id})...[/bold blue]")
                self.fetch_fred_rates(series_id, start_date, end_date)
                progress.update(task, advance=1)

def main():
    parser = argparse.ArgumentParser(description='Zinsdaten Fetcher')
    parser.add_argument('--api-key', help='FRED API Key')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--series', nargs='+', help='Liste von FRED Series IDs')
    
    args = parser.parse_args()
    
    # Erstelle Series IDs Dictionary wenn angegeben
    series_ids = None
    if args.series:
        series_ids = {series: series for series in args.series}
    
    try:
        fetcher = InterestRatesFetcher(api_key=args.api_key)
        fetcher.fetch_interest_rates(
            start_date=args.start_date,
            end_date=args.end_date,
            series_ids=series_ids
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 