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
import json

class CreditCardDataFetcher:
    def __init__(self):
        """
        Initialisiert den Credit Card Data Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/credit_card_data")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade API-Keys
        self.fred_api_key = os.getenv('FRED_API_KEY')
        self.bls_api_key = os.getenv('BLS_API_KEY')
        
        if not self.fred_api_key:
            self.console.print("[yellow]Warnung: Kein FRED_API_KEY in .env gefunden[/yellow]")
        if not self.bls_api_key:
            self.console.print("[yellow]Warnung: Kein BLS_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere FRED Client
        if self.fred_api_key:
            self.fred = Fred(api_key=self.fred_api_key)
        
        # Definiere Standard-Kategorien
        self.default_categories = {
            'RETAIL': 'Einzelhandel',
            'TRAVEL': 'Reisen',
            'DINING': 'Gastronomie',
            'ENTERTAINMENT': 'Unterhaltung',
            'GROCERY': 'Lebensmittel',
            'GAS': 'Treibstoff',
            'ONLINE': 'Online-Shopping',
            'UTILITIES': 'Versorgungsunternehmen'
        }
    
    def fetch_fred_data(self, start_date=None, end_date=None):
        """
        Holt Kreditkartendaten von FRED
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade FRED Kreditkartendaten..."):
                if not self.fred_api_key:
                    self.console.print("[red]Fehler: Kein FRED API-Key verfügbar[/red]")
                    return None
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Definiere FRED Series IDs
                series_ids = {
                    'REVOLSL': 'Kreditkartenumsatz',
                    'REVOLNS': 'Kreditkartenumsatz (nicht saisonbereinigt)',
                    'REVOLCC': 'Kreditkartenumsatz (Verbraucherkredite)'
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
    
    def fetch_bls_data(self, start_date=None, end_date=None):
        """
        Holt Kreditkartendaten vom Bureau of Labor Statistics
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade BLS Kreditkartendaten..."):
                if not self.bls_api_key:
                    self.console.print("[red]Fehler: Kein BLS API-Key verfügbar[/red]")
                    return None
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                
                # Definiere BLS Series IDs
                series_ids = {
                    'CUSR0000SA0L1E': 'Kreditkartenumsatz (CPI)',
                    'CUSR0000SA0L2': 'Kreditkartenumsatz (ohne Lebensmittel und Energie)'
                }
                
                # Erstelle API-URL
                url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
                
                # Erstelle Payload
                payload = {
                    "seriesid": list(series_ids.keys()),
                    "startyear": start_date.year,
                    "endyear": end_date.year,
                    "registrationkey": self.bls_api_key
                }
                
                # Mache API-Anfrage
                response = requests.post(url, json=payload)
                response.raise_for_status()
                
                # Verarbeite Antwort
                data = response.json()
                if data['status'] == 'REQUEST_SUCCEEDED':
                    results = {}
                    for series in data['Results']['series']:
                        series_id = series['seriesID']
                        description = series_ids[series_id]
                        values = []
                        for item in series['data']:
                            values.append({
                                'date': f"{item['year']}-{item['period']}",
                                'value': float(item['value'])
                            })
                        results[description] = pd.DataFrame(values)
                    
                    return results
                
                return None
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der BLS Daten: {str(e)}[/red]")
            return None
    
    def analyze_credit_card_data(self, fred_data, bls_data):
        """
        Analysiert die Kreditkartendaten
        
        Args:
            fred_data (pd.DataFrame): FRED Daten
            bls_data (dict): BLS Daten
        """
        try:
            metrics = {}
            
            # Analysiere FRED Daten
            if fred_data is not None and not fred_data.empty:
                metrics.update({
                    'current_revolving_credit': fred_data['Kreditkartenumsatz'].iloc[-1],
                    'revolving_credit_change_1m': fred_data['Kreditkartenumsatz'].pct_change().iloc[-1],
                    'revolving_credit_change_1y': fred_data['Kreditkartenumsatz'].pct_change(12).iloc[-1],
                    'revolving_credit_volatility': fred_data['Kreditkartenumsatz'].pct_change().std()
                })
            
            # Analysiere BLS Daten
            if bls_data is not None:
                for description, data in bls_data.items():
                    if not data.empty:
                        metrics.update({
                            f'{description}_current': data['value'].iloc[-1],
                            f'{description}_change_1m': data['value'].pct_change().iloc[-1],
                            f'{description}_change_1y': data['value'].pct_change(12).iloc[-1]
                        })
            
            return metrics
            
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Datenanalyse: {str(e)}[/red]")
            return None
    
    def process_data(self, start_date=None, end_date=None):
        """
        Verarbeitet die Kreditkartendaten
        
        Args:
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            # Hole Daten
            fred_data = self.fetch_fred_data(start_date, end_date)
            bls_data = self.fetch_bls_data(start_date, end_date)
            
            # Analysiere die Daten
            metrics = self.analyze_credit_card_data(fred_data, bls_data)
            
            if metrics:
                # Erstelle DataFrame
                df = pd.DataFrame([{
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    **metrics
                }])
                
                # Speichere die Daten
                output_file = self.base_path / f"credit_card_data_{start_date}_{end_date}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Kreditkarten-Analyse Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Aktueller Umsatz", f"${metrics['current_revolving_credit']:,.0f}")
                table.add_row("1M Änderung", f"{metrics['revolving_credit_change_1m']:.1%}")
                table.add_row("1J Änderung", f"{metrics['revolving_credit_change_1y']:.1%}")
                table.add_row("Volatilität", f"{metrics['revolving_credit_volatility']:.1%}")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Credit Card Data Fetcher')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        fetcher = CreditCardDataFetcher()
        fetcher.process_data(
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 