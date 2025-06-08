import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

class RealizedVolatilityFetcher:
    def __init__(self):
        """
        Initialisiert den Realized Volatility Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/realized_vol")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def calculate_realized_volatility(self, prices, window=20):
        """
        Berechnet die realisierte Volatilität
        
        Args:
            prices (pd.Series): Preisdaten
            window (int): Fenstergröße für die Berechnung
            
        Returns:
            pd.Series: Realisierte Volatilität
        """
        returns = np.log(prices / prices.shift(1))
        return returns.rolling(window=window).std() * np.sqrt(252)
    
    def fetch_historical_data(self, symbol, start_date=None, end_date=None, windows=None):
        """
        Holt historische Daten und berechnet die realisierte Volatilität
        
        Args:
            symbol (str): Forex-Paar Symbol
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            windows (list, optional): Liste von Fenstergrößen für die Volatilitätsberechnung
        """
        try:
            with self.console.status(f"[bold blue]Lade historische Daten für {symbol}..."):
                # Yahoo Finance Ticker
                ticker = yf.Ticker(symbol)
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=365)
                if not windows:
                    windows = [20, 60, 120]  # 20 Tage, 60 Tage, 120 Tage
                
                # Hole historische Daten
                hist = ticker.history(start=start_date, end=end_date, interval='1d')
                
                if hist.empty:
                    self.console.print(f"[yellow]Keine historischen Daten verfügbar für {symbol}[/yellow]")
                    return
                
                # Berechne verschiedene Volatilitätsmaße
                data = pd.DataFrame()
                data['date'] = hist.index
                data['close'] = hist['Close']
                
                for window in windows:
                    data[f'vol_{window}d'] = self.calculate_realized_volatility(hist['Close'], window=window)
                
                # Speichere die Daten
                output_file = self.base_path / f"realized_vol_{symbol}.csv"
                data.to_csv(output_file, index=False)
                
                # Erstelle eine schöne Zusammenfassung
                table = Table(title=f"Realisierte Volatilität für {symbol}")
                table.add_column("Metrik", style="cyan")
                table.add_column("Wert", style="green")
                
                table.add_row("Zeitraum", f"{data['date'].min().strftime('%Y-%m-%d')} bis {data['date'].max().strftime('%Y-%m-%d')}")
                table.add_row("Anzahl Datenpunkte", str(len(data)))
                
                for window in windows:
                    current_vol = data[f'vol_{window}d'].iloc[-1]
                    avg_vol = data[f'vol_{window}d'].mean()
                    table.add_row(f"Volatilität ({window} Tage)", f"Aktuell: {current_vol:.2%}, Durchschnitt: {avg_vol:.2%}")
                
                table.add_row("Speicherort", str(output_file))
                
                self.console.print(table)
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der historischen Daten: {str(e)}[/red]")
    
    def fetch_realized_volatility(self, symbols=None, start_date=None, end_date=None, windows=None):
        """
        Hauptfunktion zum Abrufen aller realisierten Volatilitätsdaten
        
        Args:
            symbols (list, optional): Liste von Forex-Paaren
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            windows (list, optional): Liste von Fenstergrößen für die Volatilitätsberechnung
        """
        # Standardwerte
        if not symbols:
            symbols = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Lade realisierte Volatilitätsdaten...", total=len(symbols))
            
            for symbol in symbols:
                self.console.print(f"\n[bold blue]Verarbeite {symbol}...[/bold blue]")
                self.fetch_historical_data(symbol, start_date, end_date, windows)
                progress.update(task, advance=1)

def main():
    parser = argparse.ArgumentParser(description='Realized Volatility Fetcher')
    parser.add_argument('--symbols', nargs='+', help='Liste von Forex-Paaren')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--windows', type=int, nargs='+', help='Liste von Fenstergrößen für die Volatilitätsberechnung')
    
    args = parser.parse_args()
    
    try:
        fetcher = RealizedVolatilityFetcher()
        fetcher.fetch_realized_volatility(
            symbols=args.symbols,
            start_date=args.start_date,
            end_date=args.end_date,
            windows=args.windows
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 