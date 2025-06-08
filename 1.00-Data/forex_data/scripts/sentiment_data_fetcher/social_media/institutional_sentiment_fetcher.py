import pandas as pd
import requests
from datetime import datetime
import os
from pathlib import Path

class InstitutionalSentimentFetcher:
    def __init__(self):
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/sentiment_data/institutional")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def fetch_cot_data(self, year):
        """
        Holt COT-Daten von der CFTC
        """
        url = f"https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                output_file = self.base_path / f"cot_data_{year}.zip"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"COT-Daten für {year} erfolgreich heruntergeladen")
            else:
                print(f"Fehler beim Herunterladen der COT-Daten für {year}: {response.status_code}")
                
        except Exception as e:
            print(f"Fehler beim API-Aufruf: {str(e)}")
    
    def fetch_cftc_data(self):
        """
        Holt CFTC-Positionsdaten
        """
        current_year = datetime.now().year
        for year in range(current_year-5, current_year+1):
            print(f"Lade COT-Daten für {year}...")
            self.fetch_cot_data(year)
    
    def fetch_commitments_of_traders(self):
        """
        Hauptfunktion zum Abrufen aller institutionellen Sentiment-Daten
        """
        self.fetch_cftc_data()

if __name__ == "__main__":
    fetcher = InstitutionalSentimentFetcher()
    fetcher.fetch_commitments_of_traders() 