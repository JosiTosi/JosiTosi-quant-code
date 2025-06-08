import pandas as pd
import requests
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

class MobilityDataFetcher:
    def __init__(self):
        """
        Initialisiert den Mobility Data Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/regime_data/mobility_data")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
    def fetch_google_mobility(self, country_code='US', start_date=None, end_date=None):
        """
        Holt Google Mobility Daten
        
        Args:
            country_code (str): Länder-Code (z.B. 'US', 'GB', 'DE')
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Google Mobility Daten..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=90)
                
                # Google Mobility Report URL
                url = "https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs"
                file_url = f"{url}/{start_date.strftime('%Y-%m-%d')}_{country_code}_Region_Mobility_Report.csv"
                
                # Lade die Daten
                response = requests.get(file_url)
                if response.status_code == 200:
                    data = pd.read_csv(pd.StringIO(response.text))
                    
                    # Filtere nach Datum
                    data['date'] = pd.to_datetime(data['date'])
                    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
                    
                    # Speichere die Daten
                    output_file = self.base_path / f"google_mobility_{country_code}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
                    data.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title="Google Mobility Daten Zusammenfassung")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Zeitraum", f"{data['date'].min().strftime('%Y-%m-%d')} bis {data['date'].max().strftime('%Y-%m-%d')}")
                    table.add_row("Anzahl Datenpunkte", str(len(data)))
                    table.add_row("Region", country_code)
                    
                    # Füge aktuelle Mobilitätswerte hinzu
                    latest_data = data.iloc[-1]
                    for col in data.columns:
                        if 'percent_change' in col:
                            value = latest_data[col]
                            table.add_row(col.replace('_percent_change', '').title(), f"{value:+.1f}%")
                    
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print("[yellow]Keine Google Mobility Daten verfügbar[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Google Mobility Daten: {str(e)}[/red]")
    
    def fetch_apple_mobility(self, country_code='US', start_date=None, end_date=None):
        """
        Holt Apple Mobility Daten
        
        Args:
            country_code (str): Länder-Code (z.B. 'US', 'GB', 'DE')
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Apple Mobility Daten..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=90)
                
                # Apple Mobility Trends URL
                url = "https://covid19.apple.com/mobility"
                response = requests.get(url)
                
                if response.status_code == 200:
                    # Extrahiere die Daten aus der JSON-Antwort
                    data = response.json()
                    
                    # Konvertiere zu DataFrame
                    df = pd.DataFrame(data)
                    
                    # Filtere nach Land und Datum
                    df['date'] = pd.to_datetime(df['date'])
                    df = df[(df['country'] == country_code) & 
                           (df['date'] >= start_date) & 
                           (df['date'] <= end_date)]
                    
                    # Speichere die Daten
                    output_file = self.base_path / f"apple_mobility_{country_code}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title="Apple Mobility Daten Zusammenfassung")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d')} bis {df['date'].max().strftime('%Y-%m-%d')}")
                    table.add_row("Anzahl Datenpunkte", str(len(df)))
                    table.add_row("Region", country_code)
                    
                    # Füge aktuelle Mobilitätswerte hinzu
                    latest_data = df.iloc[-1]
                    for col in ['driving', 'transit', 'walking']:
                        if col in latest_data:
                            value = latest_data[col]
                            table.add_row(col.title(), f"{value:+.1f}%")
                    
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print("[yellow]Keine Apple Mobility Daten verfügbar[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Apple Mobility Daten: {str(e)}[/red]")
    
    def analyze_mobility_trends(self, data, metric):
        """
        Analysiert die Mobilitätstrends
        
        Args:
            data (pd.DataFrame): Mobilitätsdaten
            metric (str): Zu analysierende Metrik
        """
        current_value = data[metric].iloc[-1]
        ma7 = data[metric].rolling(window=7).mean().iloc[-1]
        trend = data[metric].diff().iloc[-1]
        
        # Trend-Analyse
        if trend > 5:
            status = "Starker Anstieg der Mobilität"
        elif trend > 0:
            status = "Leichter Anstieg der Mobilität"
        elif trend < -5:
            status = "Starker Rückgang der Mobilität"
        elif trend < 0:
            status = "Leichter Rückgang der Mobilität"
        else:
            status = "Stabile Mobilität"
            
        return status

def main():
    parser = argparse.ArgumentParser(description='Mobility Data Fetcher')
    parser.add_argument('--country', default='US', help='Länder-Code (z.B. US, GB, DE)')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--source', choices=['google', 'apple', 'both'], default='both', 
                      help='Datenquelle (google, apple, oder both)')
    
    args = parser.parse_args()
    
    try:
        fetcher = MobilityDataFetcher()
        
        if args.source in ['google', 'both']:
            fetcher.fetch_google_mobility(
                country_code=args.country,
                start_date=args.start_date,
                end_date=args.end_date
            )
            
        if args.source in ['apple', 'both']:
            fetcher.fetch_apple_mobility(
                country_code=args.country,
                start_date=args.start_date,
                end_date=args.end_date
            )
            
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 