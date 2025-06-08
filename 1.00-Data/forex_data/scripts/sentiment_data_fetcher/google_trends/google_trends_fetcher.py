import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

class GoogleTrendsFetcher:
    def __init__(self):
        """
        Initialisiert den Google Trends Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/sentiment_data/google_trends")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.pytrends = TrendReq(hl='en-US', tz=360)
        
    def fetch_trends_data(self, keywords=None, start_date=None, end_date=None, geo=''):
        """
        Holt Google Trends Daten
        
        Args:
            keywords (list, optional): Liste von Suchbegriffen
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            geo (str, optional): Geografische Region (z.B. 'US', 'GB', 'DE')
        """
        try:
            with self.console.status("[bold blue]Lade Google Trends Daten..."):
                # Setze Standardwerte
                if not keywords:
                    keywords = ['forex trading', 'currency exchange', 'forex market']
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=90)
                
                # Konfiguriere die Anfrage
                self.pytrends.build_payload(
                    keywords,
                    cat=0,
                    timeframe=f'{start_date.strftime("%Y%m%d")} {end_date.strftime("%Y%m%d")}',
                    geo=geo
                )
                
                # Hole die Daten
                interest_over_time = self.pytrends.interest_over_time()
                
                if interest_over_time.empty:
                    self.console.print("[yellow]Keine Google Trends Daten verfügbar für den angegebenen Zeitraum[/yellow]")
                    return
                
                # Berechne zusätzliche Metriken
                data = pd.DataFrame()
                data['date'] = interest_over_time.index
                
                for keyword in keywords:
                    data[keyword] = interest_over_time[keyword]
                    data[f'{keyword}_ma7'] = interest_over_time[keyword].rolling(window=7).mean()
                    data[f'{keyword}_trend'] = interest_over_time[keyword].rolling(window=7).mean().diff()
                
                # Speichere die Daten
                output_file = self.base_path / f"google_trends_{geo}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
                data.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Google Trends Daten Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{data['date'].min().strftime('%Y-%m-%d')} bis {data['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Datenpunkte", str(len(data)))
                table.add_row("Region", geo if geo else "Global")
                
                for keyword in keywords:
                    current_value = data[keyword].iloc[-1]
                    avg_value = data[keyword].mean()
                    trend = data[f'{keyword}_trend'].iloc[-1]
                    trend_direction = "↑" if trend > 0 else "↓" if trend < 0 else "→"
                    
                    table.add_row(f"{keyword} (Aktuell)", f"{current_value} {trend_direction}")
                    table.add_row(f"{keyword} (Durchschnitt)", f"{avg_value:.1f}")
                
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Google Trends Daten: {str(e)}[/red]")
    
    def analyze_trends(self, data, keyword):
        """
        Analysiert die Trends für einen bestimmten Suchbegriff
        
        Args:
            data (pd.DataFrame): Google Trends Daten
            keyword (str): Suchbegriff
        """
        current_value = data[keyword].iloc[-1]
        ma7 = data[f'{keyword}_ma7'].iloc[-1]
        trend = data[f'{keyword}_trend'].iloc[-1]
        
        # Trend-Analyse
        if trend > 2:
            status = "Starker Aufwärtstrend"
        elif trend > 0:
            status = "Leichter Aufwärtstrend"
        elif trend < -2:
            status = "Starker Abwärtstrend"
        elif trend < 0:
            status = "Leichter Abwärtstrend"
        else:
            status = "Seitwärtsbewegung"
            
        return status

def main():
    parser = argparse.ArgumentParser(description='Google Trends Fetcher')
    parser.add_argument('--keywords', nargs='+', help='Liste von Suchbegriffen')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--geo', default='', help='Geografische Region (z.B. US, GB, DE)')
    
    args = parser.parse_args()
    
    try:
        fetcher = GoogleTrendsFetcher()
        fetcher.fetch_trends_data(
            keywords=args.keywords,
            start_date=args.start_date,
            end_date=args.end_date,
            geo=args.geo
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 