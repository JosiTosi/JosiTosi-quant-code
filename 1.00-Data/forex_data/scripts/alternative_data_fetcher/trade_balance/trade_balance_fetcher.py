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
import requests
from fredapi import Fred
import wbdata

class TradeBalanceFetcher:
    def __init__(self):
        """
        Initialisiert den Trade Balance Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/trade_balance")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade FRED API-Key
        self.fred_api_key = os.getenv('FRED_API_KEY')
        if not self.fred_api_key:
            self.console.print("[yellow]Warnung: Kein FRED_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere FRED Client
        if self.fred_api_key:
            self.fred = Fred(api_key=self.fred_api_key)
        
        # Definiere Standard-Länder
        self.default_countries = {
            'USA': 'United States',
            'GBR': 'United Kingdom',
            'JPN': 'Japan',
            'DEU': 'Germany',
            'FRA': 'France',
            'ITA': 'Italy',
            'CAN': 'Canada',
            'AUS': 'Australia',
            'CHN': 'China',
            'IND': 'India'
        }
        
        # Definiere World Bank Indikatoren
        self.wb_indicators = {
            'NE.RSB.GNFS.ZS': 'Handelsbilanz (% des BIP)',
            'NE.EXP.GNFS.ZS': 'Exporte (% des BIP)',
            'NE.IMP.GNFS.ZS': 'Importe (% des BIP)',
            'NE.TRD.GNFS.ZS': 'Handelsvolumen (% des BIP)'
        }
    
    def fetch_fred_data(self, country_code, start_date=None, end_date=None):
        """
        Holt Handelsbilanzdaten von FRED
        
        Args:
            country_code (str): Länder-Code
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status(f"[bold blue]Lade FRED Daten für {country_code}..."):
                if not self.fred_api_key:
                    self.console.print("[red]Fehler: Kein FRED API-Key verfügbar[/red]")
                    return None
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Definiere FRED Series IDs für das Land
                series_ids = {
                    f'BOPGSTB{country_code}': 'Handelsbilanz',
                    f'BOPGIMP{country_code}': 'Importe',
                    f'BOPGEXP{country_code}': 'Exporte'
                }
                
                # Hole Daten für jede Series
                data = {}
                for series_id, description in series_ids.items():
                    try:
                        series_data = self.fred.get_series(
                            series_id,
                            start_date=start_date,
                            end_date=end_date
                        )
                        data[description] = series_data
                    except Exception as e:
                        self.console.print(f"[yellow]Warnung: Konnte {series_id} nicht abrufen: {str(e)}[/yellow]")
                
                return pd.DataFrame(data)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der FRED Daten: {str(e)}[/red]")
            return None
    
    def fetch_wb_data(self, country_code, start_date=None, end_date=None):
        """
        Holt Handelsbilanzdaten von der World Bank
        
        Args:
            country_code (str): Länder-Code
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status(f"[bold blue]Lade World Bank Daten für {country_code}..."):
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Konvertiere Datumsformat
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                # Hole Daten
                data = wbdata.get_dataframe(
                    self.wb_indicators,
                    country=country_code,
                    data_date=(start_date, end_date)
                )
                
                return data
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der World Bank Daten: {str(e)}[/red]")
            return None
    
    def analyze_trade_balance(self, fred_data, wb_data, country_name):
        """
        Analysiert die Handelsbilanzdaten
        
        Args:
            fred_data (pd.DataFrame): FRED Daten
            wb_data (pd.DataFrame): World Bank Daten
            country_name (str): Name des Landes
        """
        try:
            metrics = {}
            
            # Analysiere FRED Daten
            if fred_data is not None and not fred_data.empty:
                metrics.update({
                    'current_balance': fred_data['Handelsbilanz'].iloc[-1],
                    'balance_change_1m': fred_data['Handelsbilanz'].pct_change().iloc[-1],
                    'current_imports': fred_data['Importe'].iloc[-1],
                    'current_exports': fred_data['Exporte'].iloc[-1],
                    'import_export_ratio': fred_data['Importe'].iloc[-1] / fred_data['Exporte'].iloc[-1]
                })
            
            # Analysiere World Bank Daten
            if wb_data is not None and not wb_data.empty:
                metrics.update({
                    'trade_balance_gdp': wb_data['Handelsbilanz (% des BIP)'].iloc[-1],
                    'exports_gdp': wb_data['Exporte (% des BIP)'].iloc[-1],
                    'imports_gdp': wb_data['Importe (% des BIP)'].iloc[-1],
                    'trade_volume_gdp': wb_data['Handelsvolumen (% des BIP)'].iloc[-1]
                })
            
            return metrics
            
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Datenanalyse: {str(e)}[/red]")
            return None
    
    def process_countries(self, country_codes=None, start_date=None, end_date=None):
        """
        Verarbeitet mehrere Länder
        
        Args:
            country_codes (list, optional): Liste von Länder-Codes
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            # Verwende Standard-Länder, wenn keine angegeben wurden
            if not country_codes:
                country_codes = list(self.default_countries.keys())
            
            results = []
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Analysiere Länder...", total=len(country_codes))
                
                for country_code in country_codes:
                    if country_code in self.default_countries:
                        country_name = self.default_countries[country_code]
                        
                        # Hole Daten
                        fred_data = self.fetch_fred_data(country_code, start_date, end_date)
                        wb_data = self.fetch_wb_data(country_code, start_date, end_date)
                        
                        # Analysiere die Daten
                        metrics = self.analyze_trade_balance(fred_data, wb_data, country_name)
                        
                        if metrics:
                            results.append({
                                'country_code': country_code,
                                'country_name': country_name,
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                **metrics
                            })
                    
                    progress.update(task, advance=1)
            
            # Konvertiere zu DataFrame
            if results:
                df = pd.DataFrame(results)
                
                # Speichere die Daten
                output_file = self.base_path / f"trade_balance_{start_date}_{end_date}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Handelsbilanz-Analyse Zusammenfassung")
                table.add_column("Land", style="cyan")
                table.add_column("Handelsbilanz", style="green")
                table.add_column("Import/Export", style="green")
                table.add_column("Handelsvolumen/BIP", style="green")
                
                for _, row in df.iterrows():
                    table.add_row(
                        row['country_name'],
                        f"${row['current_balance']:,.0f}",
                        f"{row['import_export_ratio']:.2f}",
                        f"{row['trade_volume_gdp']:.1%}"
                    )
                
                table.add_row("Speicherort", str(output_file), "", "")
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Trade Balance Fetcher')
    parser.add_argument('--countries', nargs='+', help='Liste von Länder-Codes')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        fetcher = TradeBalanceFetcher()
        fetcher.process_countries(
            country_codes=args.countries,
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 