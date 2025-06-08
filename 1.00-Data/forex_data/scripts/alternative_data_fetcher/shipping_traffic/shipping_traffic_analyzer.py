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
import json
from shapely.geometry import Point, box
import geopandas as gpd

class ShippingTrafficAnalyzer:
    def __init__(self):
        """
        Initialisiert den Shipping Traffic Analyzer
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/shipping_traffic")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade MarineTraffic API-Key
        self.api_key = os.getenv('MARINETRAFFIC_API_KEY')
        if not self.api_key:
            self.console.print("[yellow]Warnung: Kein MARINETRAFFIC_API_KEY in .env gefunden[/yellow]")
    
    def get_vessel_positions(self, area, start_date=None, end_date=None):
        """
        Holt Schiffsdaten von MarineTraffic
        
        Args:
            area (dict): Gebiet {'min_lat': float, 'max_lat': float, 'min_lon': float, 'max_lon': float}
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Schiffsdaten..."):
                if not self.api_key:
                    self.console.print("[red]Fehler: Kein API-Key verfügbar[/red]")
                    return []
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=7)
                
                # Erstelle API-URL
                url = "https://services.marinetraffic.com/api/exportvessels/v:8"
                params = {
                    'protocol': 'jsono',
                    'apikey': self.api_key,
                    'minLat': area['min_lat'],
                    'maxLat': area['max_lat'],
                    'minLon': area['min_lon'],
                    'maxLon': area['max_lon'],
                    'fromdate': start_date.strftime('%Y-%m-%d'),
                    'todate': end_date.strftime('%Y-%m-%d')
                }
                
                # Mache API-Anfrage
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Schiffsdaten: {str(e)}[/red]")
            return []
    
    def analyze_shipping_traffic(self, vessels_data):
        """
        Analysiert die Schiffsverkehrsdaten
        
        Args:
            vessels_data (list): Liste von Schiffsdaten
        """
        try:
            if not vessels_data:
                return None
            
            # Konvertiere zu DataFrame
            df = pd.DataFrame(vessels_data)
            
            # Berechne Metriken
            metrics = {
                'total_vessels': len(df),
                'avg_speed': df['SPEED'].mean(),
                'avg_draft': df['DRAFT'].mean(),
                'vessel_types': df['SHIPTYPE'].value_counts().to_dict(),
                'flag_countries': df['FLAG'].value_counts().to_dict()
            }
            
            return metrics
            
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Datenanalyse: {str(e)}[/red]")
            return None
    
    def process_shipping_areas(self, areas, start_date=None, end_date=None):
        """
        Verarbeitet mehrere Schifffahrtsgebiete
        
        Args:
            areas (list): Liste von Gebieten
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            results = []
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Analysiere Schifffahrtsgebiete...", total=len(areas))
                
                for area in areas:
                    # Hole Schiffsdaten
                    vessels_data = self.get_vessel_positions(area, start_date, end_date)
                    
                    if vessels_data:
                        # Analysiere die Daten
                        metrics = self.analyze_shipping_traffic(vessels_data)
                        
                        if metrics:
                            results.append({
                                'area': f"{area['min_lat']},{area['min_lon']} - {area['max_lat']},{area['max_lon']}",
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                **metrics
                            })
                    
                    progress.update(task, advance=1)
            
            # Konvertiere zu DataFrame
            if results:
                df = pd.DataFrame(results)
                
                # Speichere die Daten
                output_file = self.base_path / f"shipping_traffic_analysis_{start_date}_{end_date}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Schiffsverkehrs-Analyse Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{start_date} bis {end_date}")
                table.add_row("Anzahl Gebiete", str(len(df)))
                table.add_row("Durchschnittliche Schiffe pro Gebiet", f"{df['total_vessels'].mean():.1f}")
                table.add_row("Durchschnittliche Geschwindigkeit", f"{df['avg_speed'].mean():.1f} Knoten")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Shipping Traffic Analyzer')
    parser.add_argument('--areas', nargs='+', help='Liste von Gebieten (min_lat,max_lat,min_lon,max_lon)')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        # Konvertiere Gebiete
        areas = []
        if args.areas:
            for area in args.areas:
                min_lat, max_lat, min_lon, max_lon = map(float, area.split(','))
                areas.append({
                    'min_lat': min_lat,
                    'max_lat': max_lat,
                    'min_lon': min_lon,
                    'max_lon': max_lon
                })
        
        analyzer = ShippingTrafficAnalyzer()
        analyzer.process_shipping_areas(
            areas=areas,
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 