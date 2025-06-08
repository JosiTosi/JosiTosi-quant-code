import pandas as pd
import requests
from datetime import datetime
import os
from pathlib import Path

class EmploymentDataFetcher:
    def __init__(self):
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/economic_data/employment")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def fetch_bls_data(self, series_id, start_year, end_year):
        """
        Holt Beschäftigungsdaten von der BLS API
        """
        headers = {
            'BLS-API-KEY': 'YOUR_API_KEY',  # Bitte API-Key einfügen
            'Content-Type': 'application/json'
        }
        
        url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/{series_id}"
        payload = {
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": "YOUR_API_KEY"  # Bitte API-Key einfügen
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if data['status'] == 'REQUEST_SUCCEEDED':
                df = pd.DataFrame(data['Results']['series'][0]['data'])
                df['date'] = pd.to_datetime(df['year'] + '-' + df['period'])
                df = df.sort_values('date')
                
                output_file = self.base_path / f"bls_{series_id}_{start_year}_{end_year}.csv"
                df.to_csv(output_file, index=False)
                print(f"Daten erfolgreich gespeichert in {output_file}")
            else:
                print(f"Fehler beim Abrufen der Daten: {data['message']}")
                
        except Exception as e:
            print(f"Fehler beim API-Aufruf: {str(e)}")
    
    def fetch_employment_data(self):
        """
        Hauptfunktion zum Abrufen aller Beschäftigungsdaten
        """
        # Beispiel für wichtige Beschäftigungsserien
        series_ids = {
            'CEU0000000001': 'Total Nonfarm Employment',
            'CEU0500000001': 'Construction',
            'CEU0800000001': 'Financial Activities'
        }
        
        current_year = datetime.now().year
        for series_id, description in series_ids.items():
            print(f"Lade Daten für {description}...")
            self.fetch_bls_data(series_id, current_year-5, current_year)

if __name__ == "__main__":
    fetcher = EmploymentDataFetcher()
    fetcher.fetch_employment_data() 