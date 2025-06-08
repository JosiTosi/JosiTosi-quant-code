import pandas as pd
import requests
from datetime import datetime, timedelta
import os
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class NewsSentimentFetcher:
    def __init__(self):
        """
        Initialisiert den News Sentiment Fetcher
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/sentiment_data/news_sentiment")
        self.base_path.mkdir(parents=True, exist_ok=True)
        load_dotenv()
        
        # Lade API-Key aus .env
        self.api_key = os.getenv('NEWS_API_KEY')
        if not self.api_key:
            self.console.print("[yellow]Warnung: Kein NEWS_API_KEY in .env gefunden[/yellow]")
        
        # Initialisiere NLTK
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
    def fetch_news_data(self, query, start_date=None, end_date=None, language='en'):
        """
        Holt News-Daten von der News API
        
        Args:
            query (str): Suchbegriff
            start_date (str, optional): Startdatum im Format YYYY-MM-DD
            end_date (str, optional): Enddatum im Format YYYY-MM-DD
            language (str, optional): Sprache der Artikel
        """
        try:
            with self.console.status("[bold blue]Lade News-Daten..."):
                if not self.api_key:
                    self.console.print("[red]Fehler: Kein API-Key verfügbar[/red]")
                    return
                
                # Setze Standardwerte
                if not end_date:
                    end_date = datetime.now()
                if not start_date:
                    start_date = end_date - timedelta(days=7)
                
                # News API URL
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': query,
                    'from': start_date.strftime('%Y-%m-%d'),
                    'to': end_date.strftime('%Y-%m-%d'),
                    'language': language,
                    'sortBy': 'publishedAt',
                    'apiKey': self.api_key
                }
                
                # Lade die Daten
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    articles = data['articles']
                    
                    # Verarbeite die Artikel
                    processed_articles = []
                    for article in articles:
                        # Analysiere den Sentiment
                        text = article['title'] + " " + article['description']
                        sentiment = TextBlob(text).sentiment
                        
                        processed_article = {
                            'date': article['publishedAt'],
                            'title': article['title'],
                            'description': article['description'],
                            'source': article['source']['name'],
                            'url': article['url'],
                            'polarity': sentiment.polarity,
                            'subjectivity': sentiment.subjectivity
                        }
                        processed_articles.append(processed_article)
                    
                    # Konvertiere zu DataFrame
                    df = pd.DataFrame(processed_articles)
                    df['date'] = pd.to_datetime(df['date'])
                    
                    # Speichere die Daten
                    output_file = self.base_path / f"news_sentiment_{query.replace(' ', '_')}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title="News Sentiment Zusammenfassung")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d')} bis {df['date'].max().strftime('%Y-%m-%d')}")
                    table.add_row("Anzahl Artikel", str(len(df)))
                    table.add_row("Durchschnittliche Polarität", f"{df['polarity'].mean():.2f}")
                    table.add_row("Durchschnittliche Subjektivität", f"{df['subjectivity'].mean():.2f}")
                    
                    # Füge Sentiment-Verteilung hinzu
                    positive = len(df[df['polarity'] > 0])
                    neutral = len(df[df['polarity'] == 0])
                    negative = len(df[df['polarity'] < 0])
                    
                    table.add_row("Positive Artikel", f"{positive} ({positive/len(df)*100:.1f}%)")
                    table.add_row("Neutrale Artikel", f"{neutral} ({neutral/len(df)*100:.1f}%)")
                    table.add_row("Negative Artikel", f"{negative} ({negative/len(df)*100:.1f}%)")
                    
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print(f"[yellow]Fehler beim Abrufen der News-Daten: {response.status_code}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der News-Daten: {str(e)}[/red]")
    
    def analyze_keywords(self, text):
        """
        Analysiert Schlüsselwörter in einem Text
        
        Args:
            text (str): Zu analysierender Text
        """
        # Tokenisiere und entferne Stopwords
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        # Zähle Häufigkeiten
        keyword_freq = pd.Series(keywords).value_counts()
        return keyword_freq.head(10)
    
    def get_sentiment_trend(self, data):
        """
        Analysiert den Sentiment-Trend
        
        Args:
            data (pd.DataFrame): News-Daten
        """
        # Berechne täglichen Durchschnitt
        daily_sentiment = data.groupby(data['date'].dt.date)['polarity'].mean()
        
        # Bestimme Trend
        if len(daily_sentiment) >= 2:
            trend = daily_sentiment.iloc[-1] - daily_sentiment.iloc[-2]
            
            if trend > 0.1:
                return "Verbesserung des Sentiments"
            elif trend < -0.1:
                return "Verschlechterung des Sentiments"
            else:
                return "Stabiles Sentiment"
        else:
            return "Nicht genügend Daten für Trend-Analyse"

def main():
    parser = argparse.ArgumentParser(description='News Sentiment Fetcher')
    parser.add_argument('--query', required=True, help='Suchbegriff')
    parser.add_argument('--start-date', help='Startdatum (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Enddatum (YYYY-MM-DD)')
    parser.add_argument('--language', default='en', help='Sprache (z.B. en, de, fr)')
    
    args = parser.parse_args()
    
    try:
        fetcher = NewsSentimentFetcher()
        fetcher.fetch_news_data(
            query=args.query,
            start_date=args.start_date,
            end_date=args.end_date,
            language=args.language
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 