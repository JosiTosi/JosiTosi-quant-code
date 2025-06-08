import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
from pathlib import Path

class VolatilitySurfaceFetcher:
    def __init__(self):
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/vol_surface")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def calculate_volatility_surface(self, symbol):
        """
        Berechnet die Volatilitäts-Oberfläche aus Optionsdaten
        """
        try:
            # Yahoo Finance Ticker
            ticker = yf.Ticker(symbol)
            
            # Hole Optionsdaten
            options = ticker.options
            
            surface_data = []
            for expiry in options:
                opt_chain = ticker.option_chain(expiry)
                
                # Berechne Time to Expiry in Jahren
                expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
                tte = (expiry_date - datetime.now()).days / 365
                
                # Verarbeite Calls und Puts
                for option_type in ['calls', 'puts']:
                    chain = opt_chain.calls if option_type == 'calls' else opt_chain.puts
                    
                    for _, row in chain.iterrows():
                        # Berechne Moneyness (K/S)
                        current_price = ticker.info['regularMarketPrice']
                        moneyness = row['strike'] / current_price
                        
                        surface_data.append({
                            'date': datetime.now(),
                            'expiry': expiry,
                            'tte': tte,
                            'strike': row['strike'],
                            'moneyness': moneyness,
                            'type': option_type.upper(),
                            'implied_vol': row['impliedVolatility'],
                            'volume': row['volume'],
                            'open_interest': row['openInterest']
                        })
            
            # Erstelle DataFrame und speichere
            df = pd.DataFrame(surface_data)
            output_file = self.base_path / f"vol_surface_{symbol}.csv"
            df.to_csv(output_file, index=False)
            print(f"Volatilitäts-Oberfläche für {symbol} erfolgreich gespeichert")
            
            # Erstelle zusätzliche Visualisierungsdaten
            self.create_surface_visualization_data(df, symbol)
            
        except Exception as e:
            print(f"Fehler beim Berechnen der Volatilitäts-Oberfläche: {str(e)}")
    
    def create_surface_visualization_data(self, df, symbol):
        """
        Erstellt Daten für die Visualisierung der Volatilitäts-Oberfläche
        """
        try:
            # Gruppiere nach TTE und Moneyness
            grouped = df.groupby(['tte', 'moneyness'])['implied_vol'].mean().reset_index()
            
            # Erstelle Pivot-Tabelle für Visualisierung
            pivot = grouped.pivot(index='tte', columns='moneyness', values='implied_vol')
            
            # Speichere Visualisierungsdaten
            output_file = self.base_path / f"vol_surface_viz_{symbol}.csv"
            pivot.to_csv(output_file)
            print(f"Visualisierungsdaten für {symbol} erfolgreich gespeichert")
            
        except Exception as e:
            print(f"Fehler beim Erstellen der Visualisierungsdaten: {str(e)}")
    
    def fetch_volatility_surfaces(self):
        """
        Hauptfunktion zum Abrufen aller Volatilitäts-Oberflächen
        """
        # Wichtige Forex-Paare
        symbols = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
        
        for symbol in symbols:
            print(f"Berechne Volatilitäts-Oberfläche für {symbol}...")
            self.calculate_volatility_surface(symbol)

if __name__ == "__main__":
    fetcher = VolatilitySurfaceFetcher()
    fetcher.fetch_volatility_surfaces() 