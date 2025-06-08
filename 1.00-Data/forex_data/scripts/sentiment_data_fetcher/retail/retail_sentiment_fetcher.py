import pandas as pd
import requests
from datetime import datetime
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv
import json

class RetailSentimentFetcher:
    def __init__(self, api_key=None):
        """
        Initialisiert den Retail Sentiment Fetcher
        
        Args:
            api_key (str, optional): TradingView API Key. Wenn nicht angegeben, wird versucht, ihn aus der .env Datei zu laden.
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/sentiment_data/retail_sentiment")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Lade API Key
        load_dotenv()
        self.api_key = api_key or os.getenv('TRADINGVIEW_API_KEY')
        if not self.api_key:
            self.console.print("[yellow]Kein TradingView API Key gefunden. Verwende öffentliche Daten.[/yellow]")
        
    def fetch_tradingview_data(self, symbol, timeframe='1D'):
        """
        Holt Retail-Sentiment-Daten von TradingView
        
        Args:
            symbol (str): Forex-Paar Symbol
            timeframe (str): Zeitrahmen für die Daten
        """
        try:
            # TradingView API-Endpunkt (Beispiel)
            url = f"https://www.tradingview.com/markets/currencies/sentiment/{symbol}"
            
            with self.console.status(f"[bold blue]Lade Sentiment-Daten für {symbol}..."):
                response = requests.get(url)
                
                if response.status_code == 200:
                    # Hier müsste die tatsächliche Verarbeitung der TradingView-Daten implementiert werden
                    # Dies ist nur ein Beispiel, da TradingView keine offizielle API hat
                    data = {
                        'date': datetime.now(),
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'sentiment': 'NEUTRAL',  # Beispielwert
                        'long_percentage': 50,   # Beispielwert
                        'short_percentage': 50,  # Beispielwert
                        'total_traders': 1000,   # Beispielwert
                        'long_traders': 500,     # Beispielwert
                        'short_traders': 500     # Beispielwert
                    }
                    
                    df = pd.DataFrame([data])
                    output_file = self.base_path / f"tradingview_sentiment_{symbol}_{timeframe}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title=f"Retail Sentiment für {symbol}")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Zeitpunkt", data['date'].strftime('%Y-%m-%d %H:%M:%S'))
                    table.add_row("Zeitrahmen", timeframe)
                    table.add_row("Sentiment", data['sentiment'])
                    table.add_row("Long %", f"{data['long_percentage']}%")
                    table.add_row("Short %", f"{data['short_percentage']}%")
                    table.add_row("Gesamttrader", str(data['total_traders']))
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print(f"[red]Fehler beim Abrufen der TradingView-Daten für {symbol}: {response.status_code}[/red]")
                    
        except Exception as e:
            self.console.print(f"[red]Fehler beim API-Aufruf: {str(e)}[/red]")
    
    def fetch_retail_sentiment(self, symbols=None, timeframes=None):
        """
        Hauptfunktion zum Abrufen aller Retail-Sentiment-Daten
        
        Args:
            symbols (list, optional): Liste von Forex-Paaren
            timeframes (list, optional): Liste von Zeitrahmen
        """
        # Standardwerte
        if not symbols:
            symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
        if not timeframes:
            timeframes = ['1D', '1W', '1M']
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Lade Retail-Sentiment-Daten...", total=len(symbols) * len(timeframes))
            
            for symbol in symbols:
                for timeframe in timeframes:
                    self.console.print(f"\n[bold blue]Lade Daten für {symbol} ({timeframe})...[/bold blue]")
                    self.fetch_tradingview_data(symbol, timeframe)
                    progress.update(task, advance=1)

def main():
    parser = argparse.ArgumentParser(description='Retail Sentiment Fetcher')
    parser.add_argument('--api-key', help='TradingView API Key')
    parser.add_argument('--symbols', nargs='+', help='Liste von Forex-Paaren')
    parser.add_argument('--timeframes', nargs='+', help='Liste von Zeitrahmen')
    
    args = parser.parse_args()
    
    try:
        fetcher = RetailSentimentFetcher(api_key=args.api_key)
        fetcher.fetch_retail_sentiment(
            symbols=args.symbols,
            timeframes=args.timeframes
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 