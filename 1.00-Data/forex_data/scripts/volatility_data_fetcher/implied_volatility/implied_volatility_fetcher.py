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

class ImpliedVolatilityFetcher:
    def __init__(self):
        """
        Initialisiert den Implied Volatility Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/volatility_data/implied_vol")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def fetch_option_chain(self, symbol, expiry_date=None):
        """
        Holt Optionsdaten von Yahoo Finance
        
        Args:
            symbol (str): Forex-Paar Symbol
            expiry_date (str, optional): Verfallsdatum im Format YYYY-MM-DD
        """
        try:
            with self.console.status(f"[bold blue]Lade Optionsdaten für {symbol}..."):
                # Yahoo Finance Ticker
                ticker = yf.Ticker(symbol)
                
                # Hole Optionsdaten
                if expiry_date:
                    options = [expiry_date]
                else:
                    options = ticker.options
                
                if not options:
                    self.console.print(f"[yellow]Keine Optionsdaten verfügbar für {symbol}[/yellow]")
                    return
                
                data = []
                for date in options:
                    opt_chain = ticker.option_chain(date)
                    
                    # Verarbeite Calls
                    for _, row in opt_chain.calls.iterrows():
                        data.append({
                            'date': datetime.now(),
                            'expiry': date,
                            'symbol': symbol,
                            'type': 'CALL',
                            'strike': row['strike'],
                            'implied_volatility': row['impliedVolatility'],
                            'volume': row['volume'],
                            'open_interest': row['openInterest'],
                            'last_price': row['lastPrice'],
                            'bid': row['bid'],
                            'ask': row['ask']
                        })
                    
                    # Verarbeite Puts
                    for _, row in opt_chain.puts.iterrows():
                        data.append({
                            'date': datetime.now(),
                            'expiry': date,
                            'symbol': symbol,
                            'type': 'PUT',
                            'strike': row['strike'],
                            'implied_volatility': row['impliedVolatility'],
                            'volume': row['volume'],
                            'open_interest': row['openInterest'],
                            'last_price': row['lastPrice'],
                            'bid': row['bid'],
                            'ask': row['ask']
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    output_file = self.base_path / f"implied_vol_{symbol}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title=f"Implizite Volatilität für {symbol}")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Anzahl Optionen", str(len(df)))
                    table.add_row("Verfallsdaten", ", ".join(df['expiry'].unique()))
                    table.add_row("Durchschnittliche IV", f"{df['implied_volatility'].mean():.2%}")
                    table.add_row("Min IV", f"{df['implied_volatility'].min():.2%}")
                    table.add_row("Max IV", f"{df['implied_volatility'].max():.2%}")
                    table.add_row("Gesamt-Volumen", str(df['volume'].sum()))
                    table.add_row("Gesamt-Open Interest", str(df['open_interest'].sum()))
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print(f"[yellow]Keine Optionsdaten gefunden für {symbol}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Optionsdaten: {str(e)}[/red]")
    
    def fetch_implied_volatility(self, symbols=None, expiry_date=None):
        """
        Hauptfunktion zum Abrufen aller impliziten Volatilitätsdaten
        
        Args:
            symbols (list, optional): Liste von Forex-Paaren
            expiry_date (str, optional): Verfallsdatum im Format YYYY-MM-DD
        """
        # Standardwerte
        if not symbols:
            symbols = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Lade implizite Volatilitätsdaten...", total=len(symbols))
            
            for symbol in symbols:
                self.console.print(f"\n[bold blue]Verarbeite {symbol}...[/bold blue]")
                self.fetch_option_chain(symbol, expiry_date)
                progress.update(task, advance=1)

def main():
    parser = argparse.ArgumentParser(description='Implied Volatility Fetcher')
    parser.add_argument('--symbols', nargs='+', help='Liste von Forex-Paaren')
    parser.add_argument('--expiry-date', help='Verfallsdatum (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        fetcher = ImpliedVolatilityFetcher()
        fetcher.fetch_implied_volatility(
            symbols=args.symbols,
            expiry_date=args.expiry_date
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 