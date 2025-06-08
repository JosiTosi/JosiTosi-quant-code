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

class ParkingLotAnalyzer:
    def __init__(self):
        """
        Initialisiert den Parking Lot Analyzer
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/alternative_data/parking_lots")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade Planet Labs API-Key
        self.api_key = os.getenv('PLANET_API_KEY')
        if not self.api_key:
            self.console.print("[yellow]Warnung: Kein PLANET_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere Planet API Client
        if self.api_key:
            self.client = api.ClientV1(api_key=self.api_key)
        
    def get_satellite_images(self, location, start_date=None, end_date=None):
        """
        Holt Satellitenbilder von Planet Labs
        
        Args:
            location (dict): Koordinaten des Parkplatzes {'lat': float, 'lon': float}
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status("[bold blue]Lade Satellitenbilder..."):
                if not self.api_key:
                    self.console.print("[red]Fehler: Kein API-Key verfügbar[/red]")
                    return
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=7)
                
                # Erstelle GeoJSON für den Parkplatz
                geojson = {
                    "type": "Point",
                    "coordinates": [location['lon'], location['lat']]
                }
                
                # Erstelle Filter für die Suche
                date_filter = filters.date_range('acquired', gte=start_date, lte=end_date)
                cloud_filter = filters.range_filter('cloud_cover', lte=0.1)
                geom_filter = filters.geom_filter(geojson)
                
                # Kombiniere Filter
                combined_filter = filters.and_filter(date_filter, cloud_filter, geom_filter)
                
                # Suche nach Bildern
                search = self.client.quick_search(combined_filter, item_type='PSScene4Band')
                
                return list(search.items_iter())
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Satellitenbilder: {str(e)}[/red]")
            return []
    
    def analyze_parking_lot(self, image_path, threshold=0.5):
        """
        Analysiert die Parkplatzauslastung in einem Satellitenbild
        
        Args:
            image_path (str): Pfad zum Satellitenbild
            threshold (float): Schwellenwert für die Erkennung
        """
        try:
            # Lade und verarbeite das Bild
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Wende Schwellenwert an
            _, binary = cv2.threshold(gray, int(255 * threshold), 255, cv2.THRESH_BINARY)
            
            # Finde Konturen
            contours = measure.find_contours(binary, 0.5)
            
            # Berechne Auslastung
            total_area = image.shape[0] * image.shape[1]
            occupied_area = sum(cv2.contourArea(np.array(c)) for c in contours)
            occupancy_rate = occupied_area / total_area
            
            return occupancy_rate
            
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Bildanalyse: {str(e)}[/red]")
            return None
    
    def process_parking_lots(self, locations, start_date=None, end_date=None):
        """
        Verarbeitet mehrere Parkplätze
        
        Args:
            locations (list): Liste von Parkplatz-Koordinaten
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
        """
        try:
            results = []
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Analysiere Parkplätze...", total=len(locations))
                
                for location in locations:
                    # Hole Satellitenbilder
                    images = self.get_satellite_images(location, start_date, end_date)
                    
                    if images:
                        # Analysiere jedes Bild
                        for image in images:
                            occupancy = self.analyze_parking_lot(image['path'])
                            
                            if occupancy is not None:
                                results.append({
                                    'date': image['acquired'],
                                    'location': f"{location['lat']}, {location['lon']}",
                                    'occupancy_rate': occupancy
                                })
                    
                    progress.update(task, advance=1)
            
            # Konvertiere zu DataFrame
            if results:
                df = pd.DataFrame(results)
                
                # Speichere die Daten
                output_file = self.base_path / f"parking_lot_analysis_{start_date}_{end_date}.csv"
                df.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title="Parkplatz-Analyse Zusammenfassung")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d')} bis {df['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Analysen", str(len(df)))
                table.add_row("Durchschnittliche Auslastung", f"{df['occupancy_rate'].mean():.1%}")
                table.add_row("Maximale Auslastung", f"{df['occupancy_rate'].max():.1%}")
                table.add_row("Minimale Auslastung", f"{df['occupancy_rate'].min():.1%}")
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler bei der Verarbeitung: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description='Parking Lot Analyzer')
    parser.add_argument('--locations', nargs='+', help='Liste von Parkplatz-Koordinaten (lat,lon)')
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
        
        analyzer = ParkingLotAnalyzer()
        analyzer.process_parking_lots(
            locations=locations,
            start_date=args.start_date,
            end_date=args.end_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 