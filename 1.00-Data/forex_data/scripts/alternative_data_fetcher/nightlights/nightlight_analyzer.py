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
from planet import api
from planet.api import filters
import cv2
from skimage import measure
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

class NightlightAnalyzer:
    def __init__(self):
        """
        Initialisiert den Nightlight Analyzer
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/nightlights")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade Planet Labs API-Key
        self.api_key = os.getenv('PLANET_API_KEY')
        if not self.api_key:
            self.console.print("[yellow]Warnung: Kein PLANET_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere Planet API Client
        if self.api_key:
            self.client = api.ClientV1(api_key=self.api_key)
    
    def get_nightlight_images(self, location, start_date=None, end_date=None):
        """
        Holt Nachtlicht-Satellitenbilder von Planet Labs
        
        Args:
            location (dict): Koordinaten des Gebiets {'lat': float, 'lon': float}
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Nachtlichtbilder..."):
                if not self.api_key:
                    self.console.print("[red]Fehler: Kein API-Key verfügbar[/red]")
                    return []
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=30)
                
                # Erstelle GeoJSON für das Gebiet
                geojson = {
                    "type": "Point",
                    "coordinates": [location['lon'], location['lat']]
                }
                
                # Erstelle Filter für die Suche
                date_filter = filters.date_range('acquired', gte=start_date, lte=end_date)
                cloud_filter = filters.range_filter('cloud_cover', lte=0.1)
                geom_filter = filters.geom_filter(geojson)
                night_filter = filters.range_filter('night', eq=True)
                
                # Kombiniere Filter
                combined_filter = filters.and_filter(date_filter, cloud_filter, geom_filter, night_filter)
                
                # Suche nach Bildern
                search = self.client.quick_search(combined_filter, item_type='PSScene4Band')
                
                return list(search.items_iter())
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Nachtlichtbilder: {str(e)}[/red]")
            return []
    
    def analyze_nightlight(self, image_path):
        """
        Analysiert die Nachtlichtintensität in einem Satellitenbild
        
        Args:
            image_path (str): Pfad zum Satellitenbild
        """
        try:
            # Lade und verarbeite das Bild
            with rasterio.open(image_path) as src:
                image = src.read()
                
                # Berechne Durchschnittsintensität
                avg_intensity = np.mean(image)
                
                # Berechne maximale Intensität
                max_intensity = np.max(image)
                
                # Berechne Intensitätsverteilung
                intensity_distribution = np.histogram(image.flatten(), bins=50)
                
                # Erstelle Visualisierung
                plt.figure(figsize=(10, 6))
                show(image)
                plt.title('Nachtlichtintensität')
                plt.colorbar(label='Intensität')
                
                # Speichere Visualisierung
                vis_path = self.base_path / f"nightlight_visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(vis_path)
                plt.close()
                
                return {
                    'avg_intensity': avg_intensity,
                    'max_intensity': max_intensity,
                    'intensity_distribution': intensity_distribution,
                    'visualization_path': str(vis_path)
                }
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Bildanalyse: {str(e)}[/red]")
            return None
    
    def process_locations(self, locations, start_date=None, end_date=None):
        """
        Verarbeitet mehrere Standorte
        
        Args:
            locations (list): Liste von Standort-Koordinaten
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            results = []
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Analysiere Standorte...", total=len(locations))
                
                for location in locations:
                    # Hole Nachtlichtbilder
                    images = self.get_nightlight_images(location, start_date, end_date)
                    
                    if images:
                        # Analysiere jedes Bild
                        for image in images:
                            analysis = self.analyze_nightlight(image['path'])
                            
                            if analysis:
                                results.append({
                                    'date': image['acquired'],
                                    'location': f"{location['lat']}, {location['lon']}",
                                    'avg_intensity': analysis['avg_intensity'],
                                    'max_intensity': analysis['max_intensity'],
                                    'visualization_path': analysis['visualization_path']
                                })
                    
                    progress.update(task, advance=1)
            
            # Konvertiere zu DataFrame
            if results:
                df = pd.DataFrame(results)
                
                # Speichere die Daten
                output_file = self.base_path / f"nightlight_analysis_{start_date}_{end_date}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Nachtlicht-Analyse Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d')} bis {df['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Analysen", str(len(df)))
                table.add_row("Durchschnittliche Intensität", f"{df['avg_intensity'].mean():.2f}")
                table.add_row("Maximale Intensität", f"{df['max_intensity'].max():.2f}")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Nightlight Analyzer')
    parser.add_argument('--locations', nargs='+', help='Liste von Standort-Koordinaten (lat,lon)')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        # Konvertiere Koordinaten
        locations = []
        if args.locations:
            for loc in args.locations:
                lat, lon = map(float, loc.split(','))
                locations.append({'lat': lat, 'lon': lon})
        
        analyzer = NightlightAnalyzer()
        analyzer.process_locations(
            locations=locations,
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 