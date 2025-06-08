import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time
import zipfile
import io
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.table import Table
from rich import print as rprint
import pyfiglet
from rich.text import Text
import random

# ============================================================
# KONFIGURATION - HIER ANPASSEN
# ============================================================

# Zeitraum für historische Daten
START_YEAR = 2006  # Ab welchem Jahr
END_YEAR = 2024    # Bis welches Jahr (nicht aktuelles Jahr)

# Output Ordner
OUTPUT_FOLDER = "/Users/josua/Documents/Coding/JosiTosi-quant-code/Data/forex_data/cot_data/raw/1W_Data_raw"

# Forex Pairs die wir wollen (CFTC Namen)
FOREX_PAIRS = [
    'EURO FX',
    'JAPANESE YEN', 
    'BRITISH POUND',
    'SWISS FRANC',
    'CANADIAN DOLLAR',
    'AUSTRALIAN DOLLAR',
    'NEW ZEALAND DOLLAR',
    'MEXICAN PESO',
    'BRAZILIAN REAL',
    'RUSSIAN RUBLE'
]

# ============================================================
# SCRIPT - NICHT ÄNDERN
# ============================================================

class ForexCOTFetcher:
    def __init__(self, output_folder=OUTPUT_FOLDER):
        self.output_folder = output_folder
        self.base_url = "https://www.cftc.gov/files/dea/history/"
        self.console = Console()
        
        # Create output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            self.console.print(f"[green]📁 Output-Ordner erstellt: {self.output_folder}[/green]")
    
    def standardize_columns(self, df):
        """Standardize column names across different years"""
        if df is None or df.empty:
            return df
            
        # Mapping für Spaltennamen
        column_mapping = {
            # Markt und Datum
            'Market_and_Exchange_Names': 'Market_and_Exchange_Names',
            'Market and Exchange Names': 'Market_and_Exchange_Names',
            'Market': 'Market_and_Exchange_Names',
            'Exchange': 'Market_and_Exchange_Names',
            
            'Report_Date_as_YYYY_MM_DD': 'Report_Date_as_YYYY_MM_DD',
            'Report Date as YYYY-MM-DD': 'Report_Date_as_YYYY_MM_DD',
            'Report Date': 'Report_Date_as_YYYY_MM_DD',
            'Date': 'Report_Date_as_YYYY_MM_DD',
            
            # Open Interest
            'Open_Interest_All': 'Open_Interest_All',
            'Open Interest All': 'Open_Interest_All',
            'Open Interest': 'Open_Interest_All',
            
            # Dealer Positions
            'Dealer_Positions_Long_All': 'Dealer_Positions_Long_All',
            'Dealer Positions Long All': 'Dealer_Positions_Long_All',
            'Dealer_Positions_Short_All': 'Dealer_Positions_Short_All',
            'Dealer Positions Short All': 'Dealer_Positions_Short_All',
            
            # Asset Manager Positions
            'Asset_Mgr_Positions_Long_All': 'Asset_Mgr_Positions_Long_All',
            'Asset Mgr Positions Long All': 'Asset_Mgr_Positions_Long_All',
            'Asset_Mgr_Positions_Short_All': 'Asset_Mgr_Positions_Short_All',
            'Asset Mgr Positions Short All': 'Asset_Mgr_Positions_Short_All',
            
            # Leveraged Money Positions
            'Lev_Money_Positions_Long_All': 'Lev_Money_Positions_Long_All',
            'Lev Money Positions Long All': 'Lev_Money_Positions_Long_All',
            'Lev_Money_Positions_Short_All': 'Lev_Money_Positions_Short_All',
            'Lev Money Positions Short All': 'Lev_Money_Positions_Short_All'
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Keep only standardized columns that exist in the dataframe
        standard_columns = [
            'Market_and_Exchange_Names',
            'Report_Date_as_YYYY_MM_DD',
            'Open_Interest_All',
            'Dealer_Positions_Long_All',
            'Dealer_Positions_Short_All',
            'Asset_Mgr_Positions_Long_All',
            'Asset_Mgr_Positions_Short_All',
            'Lev_Money_Positions_Long_All',
            'Lev_Money_Positions_Short_All'
        ]
        
        # Keep only columns that exist in the dataframe
        existing_columns = [col for col in standard_columns if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    def fetch_year_data(self, year):
        """Fetch COT data for a specific year"""
        
        # Neue URL-Struktur für historische Daten
        url = f"{self.base_url}deacot{year}.zip"
        
        try:
            self.console.print(f"[yellow]📥 Lade Jahr {year}...[/yellow]")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                # Suche nach der richtigen Datei im ZIP
                csv_files = [f for f in zip_file.namelist() if f.endswith('.txt')]
                
                if not csv_files:
                    self.console.print(f"[red]❌ Keine Daten für {year} gefunden[/red]")
                    return None
                
                # Wähle die erste passende Datei
                target_file = csv_files[0]
                
                # Read the CSV file
                with zip_file.open(target_file) as csv_file:
                    df = pd.read_csv(csv_file)
                    
                    # Standardize columns
                    df = self.standardize_columns(df)
                    
                    # Zeige verfügbare Spalten für Debugging
                    self.console.print(f"\n[blue]Verfügbare Spalten für {year}:[/blue]")
                    self.console.print(df.columns.tolist())
                
                return df
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.console.print(f"[yellow]⚠️  Keine Daten für Jahr {year} verfügbar[/yellow]")
            else:
                self.console.print(f"[red]❌ HTTP Fehler bei Jahr {year}: {e}[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]❌ Fehler bei Jahr {year}: {e}[/red]")
            return None
    
    def filter_forex_data(self, df):
        """Filter data for Forex pairs only"""
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Filter for Forex pairs
        forex_mask = df['Market_and_Exchange_Names'].str.contains('|'.join(FOREX_PAIRS), case=False, na=False)
        forex_df = df[forex_mask].copy()
        
        if not forex_df.empty:
            # Add simplified pair name
            forex_df['Forex_Pair'] = forex_df['Market_and_Exchange_Names'].apply(self.simplify_pair_name)
            
            # Sort by date
            if 'Report_Date_as_YYYY_MM_DD' in forex_df.columns:
                forex_df = forex_df.sort_values('Report_Date_as_YYYY_MM_DD')
        
        return forex_df
    
    def simplify_pair_name(self, market_name):
        """Convert CFTC market name to simple forex pair"""
        mapping = {
            'EURO FX': 'EURUSD',
            'JAPANESE YEN': 'USDJPY',
            'BRITISH POUND': 'GBPUSD',
            'SWISS FRANC': 'USDCHF',
            'CANADIAN DOLLAR': 'USDCAD',
            'AUSTRALIAN DOLLAR': 'AUDUSD',
            'NEW ZEALAND DOLLAR': 'NZDUSD',
            'MEXICAN PESO': 'USDMXN',
            'BRAZILIAN REAL': 'USDBRL',
            'RUSSIAN RUBLE': 'USDRUB'
        }
        
        for cftc_name, pair in mapping.items():
            if cftc_name in market_name.upper():
                return pair
        
        return market_name
    
    def create_status_table(self, downloaded_years, years_to_download):
        """Create a status table for the download process"""
        table = Table(title="📊 Download Status")
        table.add_column("Status", style="cyan")
        table.add_column("Jahre", style="magenta")
        
        if downloaded_years:
            table.add_row("✅ Bereits heruntergeladen", ", ".join(map(str, sorted(downloaded_years))))
        if years_to_download:
            table.add_row("⏳ Noch zu laden", ", ".join(map(str, sorted(years_to_download))))
            
        return table
    
    def fetch_historical_forex_data(self, start_year=START_YEAR, end_year=END_YEAR):
        """Fetch historical Forex COT data for specified range"""
        
        # Cool ASCII Art Banner
        banner = pyfiglet.figlet_format("Josi's COT Fetcher", font="slant")
        self.console.print(Panel(Text(banner, style="bold magenta"), border_style="magenta"))
        
        # Status Panel
        status_panel = Panel(
            f"[bold cyan]📅 Zeitraum:[/bold cyan] {start_year} bis {end_year}\n"
            f"[bold green]💱 Forex Pairs:[/bold green] {len(FOREX_PAIRS)} Paare\n"
            f"[bold yellow]📁 Output:[/bold yellow] {self.output_folder}",
            title="⚙️ Konfiguration",
            border_style="blue"
        )
        self.console.print(status_panel)
        
        years = list(range(start_year, end_year + 1))
        downloaded_years = []
        
        # Check which years are already downloaded
        for year in years:
            year_filename = f"forex_cot_{year}.csv"
            year_filepath = os.path.join(self.output_folder, year_filename)
            if os.path.exists(year_filepath):
                downloaded_years.append(year)
        
        # Filter out already downloaded years
        years_to_download = [year for year in years if year not in downloaded_years]
        
        # Show status table
        self.console.print(self.create_status_table(downloaded_years, years_to_download))
        
        if not years_to_download:
            self.console.print(Panel("[green]✅ Alle Jahre sind bereits heruntergeladen![/green]", border_style="green"))
            return
        
        self.console.print(f"\n[yellow]📥 Lade {len(years_to_download)} fehlende Jahre...[/yellow]")
        
        # Progress bar for years
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Lade COT Daten...", total=len(years_to_download))
            
            for year in years_to_download:
                df = self.fetch_year_data(year)
                
                if df is not None:
                    forex_df = self.filter_forex_data(df)
                    
                    if not forex_df.empty:
                        # Save individual year file
                        year_filename = f"forex_cot_{year}.csv"
                        year_filepath = os.path.join(self.output_folder, year_filename)
                        forex_df.to_csv(year_filepath, index=False)
                        
                        self.console.print(f"[green]✅ {year}: {len(forex_df)} Forex Records gespeichert[/green]")
                    else:
                        self.console.print(f"[yellow]⚠️  {year}: Keine Forex-Daten gefunden[/yellow]")
                
                progress.update(task, advance=1)
                # Be nice to the server
                time.sleep(1)
        
        # Final success message
        success_panel = Panel(
            "[green]🎉 FERTIG![/green]\n"
            f"[blue]📁 Alle Dateien gespeichert in: {OUTPUT_FOLDER}/[/blue]",
            border_style="green"
        )
        self.console.print(success_panel)

def main():
    """Main function - Execute the Forex COT data fetching"""
    
    console = Console()
    
    # Cool ASCII Art Banner
    banner = pyfiglet.figlet_format("Josi's COT Fetcher", font="slant")
    console.print(Panel(Text(banner, style="bold magenta"), border_style="magenta"))
    
    # Show current configuration
    config_panel = Panel(
        f"[cyan]📅 Zeitraum:[/cyan] {START_YEAR} - {END_YEAR}\n"
        f"[green]💱 Forex Pairs:[/green] {len(FOREX_PAIRS)}\n"
        f"[yellow]📁 Output Ordner:[/yellow] {OUTPUT_FOLDER}",
        title="⚙️ Konfiguration",
        border_style="blue"
    )
    console.print(config_panel)
    
    # Ask for confirmation
    console.print("\n[bold yellow]Konfiguration OK? Drücke ENTER zum Starten oder CTRL+C zum Abbrechen...[/bold yellow]")
    try:
        input()
    except KeyboardInterrupt:
        console.print("\n[red]👋 Abgebrochen![/red]")
        return
    
    # Initialize fetcher
    fetcher = ForexCOTFetcher()
    
    # Fetch the data
    fetcher.fetch_historical_forex_data()
    
    console.print("\n[green]✅ Script beendet![/green]")

if __name__ == "__main__":
    main()