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
import tweepy
import praw
from textblob import TextBlob

class SocialMediaSentimentFetcher:
    def __init__(self, twitter_api_key=None, twitter_api_secret=None, twitter_access_token=None, 
                 twitter_access_token_secret=None, reddit_client_id=None, reddit_client_secret=None):
        """
        Initialisiert den Social Media Sentiment Fetcher
        
        Args:
            twitter_api_key (str, optional): Twitter API Key
            twitter_api_secret (str, optional): Twitter API Secret
            twitter_access_token (str, optional): Twitter Access Token
            twitter_access_token_secret (str, optional): Twitter Access Token Secret
            reddit_client_id (str, optional): Reddit Client ID
            reddit_client_secret (str, optional): Reddit Client Secret
        """
        self.console = Console()
        self.base_path = Path("/Users/josua/Documents/Coding/JosiTosi-quant-code/1.00-Data/forex_data/sentiment_data/social_media")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Lade API Keys
        load_dotenv()
        self.twitter_api_key = twitter_api_key or os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = twitter_api_secret or os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = twitter_access_token or os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = twitter_access_token_secret or os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.reddit_client_id = reddit_client_id or os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = reddit_client_secret or os.getenv('REDDIT_CLIENT_SECRET')
        
        # Initialisiere Twitter API
        if all([self.twitter_api_key, self.twitter_api_secret, self.twitter_access_token, self.twitter_access_token_secret]):
            auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
            auth.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)
            self.twitter_api = tweepy.API(auth)
        else:
            self.console.print("[yellow]Twitter API Credentials nicht vollständig. Twitter-Daten werden nicht abgerufen.[/yellow]")
            self.twitter_api = None
        
        # Initialisiere Reddit API
        if all([self.reddit_client_id, self.reddit_client_secret]):
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent="YOUR_USER_AGENT"
            )
        else:
            self.console.print("[yellow]Reddit API Credentials nicht vollständig. Reddit-Daten werden nicht abgerufen.[/yellow]")
            self.reddit = None
        
    def analyze_sentiment(self, text):
        """
        Analysiert den Sentiment eines Textes
        
        Args:
            text (str): Der zu analysierende Text
            
        Returns:
            tuple: (polarity, subjectivity)
        """
        analysis = TextBlob(text)
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity
    
    def fetch_twitter_sentiment(self, symbol, count=100):
        """
        Holt Twitter-Sentiment-Daten
        
        Args:
            symbol (str): Forex-Paar Symbol
            count (int): Anzahl der Tweets
        """
        if not self.twitter_api:
            return
        
        try:
            with self.console.status(f"[bold blue]Lade Twitter-Daten für {symbol}..."):
                # Suche nach Tweets mit dem Forex-Paar
                tweets = self.twitter_api.search_tweets(
                    q=f"#{symbol} OR {symbol}",
                    lang="en",
                    count=count
                )
                
                data = []
                for tweet in tweets:
                    polarity, subjectivity = self.analyze_sentiment(tweet.text)
                    data.append({
                        'date': tweet.created_at,
                        'symbol': symbol,
                        'text': tweet.text,
                        'user': tweet.user.screen_name,
                        'retweets': tweet.retweet_count,
                        'favorites': tweet.favorite_count,
                        'sentiment_polarity': polarity,
                        'sentiment_subjectivity': subjectivity
                    })
                
                if data:
                    df = pd.DataFrame(data)
                    output_file = self.base_path / f"twitter_sentiment_{symbol}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title=f"Twitter Sentiment für {symbol}")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Anzahl Tweets", str(len(df)))
                    table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d %H:%M:%S')} bis {df['date'].max().strftime('%Y-%m-%d %H:%M:%S')}")
                    table.add_row("Durchschnittlicher Sentiment", f"{df['sentiment_polarity'].mean():.2f}")
                    table.add_row("Gesamt-Retweets", str(df['retweets'].sum()))
                    table.add_row("Gesamt-Favorites", str(df['favorites'].sum()))
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print(f"[yellow]Keine Tweets gefunden für {symbol}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Twitter-Daten: {str(e)}[/red]")
    
    def fetch_reddit_sentiment(self, symbol, limit=100):
        """
        Holt Reddit-Sentiment-Daten
        
        Args:
            symbol (str): Forex-Paar Symbol
            limit (int): Maximale Anzahl der Posts
        """
        if not self.reddit:
            return
        
        try:
            with self.console.status(f"[bold blue]Lade Reddit-Daten für {symbol}..."):
                # Suche nach Posts in Forex-bezogenen Subreddits
                subreddits = ['forex', 'trading', 'investing']
                data = []
                
                for subreddit_name in subreddits:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    for post in subreddit.search(symbol, limit=limit):
                        polarity, subjectivity = self.analyze_sentiment(post.title + " " + post.selftext)
                        data.append({
                            'date': datetime.fromtimestamp(post.created_utc),
                            'symbol': symbol,
                            'title': post.title,
                            'text': post.selftext,
                            'score': post.score,
                            'subreddit': subreddit_name,
                            'sentiment_polarity': polarity,
                            'sentiment_subjectivity': subjectivity
                        })
                
                if data:
                    df = pd.DataFrame(data)
                    output_file = self.base_path / f"reddit_sentiment_{symbol}.csv"
                    df.to_csv(output_file, index=False)
                    
                    # Erstelle eine schöne Zusammenfassung
                    table = Table(title=f"Reddit Sentiment für {symbol}")
                    table.add_column("Metrik", style="cyan")
                    table.add_column("Wert", style="green")
                    
                    table.add_row("Anzahl Posts", str(len(df)))
                    table.add_row("Zeitraum", f"{df['date'].min().strftime('%Y-%m-%d %H:%M:%S')} bis {df['date'].max().strftime('%Y-%m-%d %H:%M:%S')}")
                    table.add_row("Durchschnittlicher Sentiment", f"{df['sentiment_polarity'].mean():.2f}")
                    table.add_row("Gesamt-Score", str(df['score'].sum()))
                    table.add_row("Subreddits", ", ".join(df['subreddit'].unique()))
                    table.add_row("Speicherort", str(output_file))
                    
                    self.console.print(table)
                else:
                    self.console.print(f"[yellow]Keine Reddit-Posts gefunden für {symbol}[/yellow]")
                
        except Exception as e:
            self.console.print(f"[red]Fehler beim Abrufen der Reddit-Daten: {str(e)}[/red]")
    
    def fetch_social_media_sentiment(self, symbols=None, twitter_count=100, reddit_limit=100):
        """
        Hauptfunktion zum Abrufen aller Social-Media-Sentiment-Daten
        
        Args:
            symbols (list, optional): Liste von Forex-Paaren
            twitter_count (int, optional): Anzahl der Tweets pro Symbol
            reddit_limit (int, optional): Maximale Anzahl der Reddit-Posts pro Symbol
        """
        # Standardwerte
        if not symbols:
            symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Lade Social-Media-Sentiment-Daten...", total=len(symbols) * 2)
            
            for symbol in symbols:
                self.console.print(f"\n[bold blue]Verarbeite {symbol}...[/bold blue]")
                self.fetch_twitter_sentiment(symbol, count=twitter_count)
                progress.update(task, advance=1)
                self.fetch_reddit_sentiment(symbol, limit=reddit_limit)
                progress.update(task, advance=1)

def main():
    parser = argparse.ArgumentParser(description='Social Media Sentiment Fetcher')
    parser.add_argument('--twitter-api-key', help='Twitter API Key')
    parser.add_argument('--twitter-api-secret', help='Twitter API Secret')
    parser.add_argument('--twitter-access-token', help='Twitter Access Token')
    parser.add_argument('--twitter-access-token-secret', help='Twitter Access Token Secret')
    parser.add_argument('--reddit-client-id', help='Reddit Client ID')
    parser.add_argument('--reddit-client-secret', help='Reddit Client Secret')
    parser.add_argument('--symbols', nargs='+', help='Liste von Forex-Paaren')
    parser.add_argument('--twitter-count', type=int, default=100, help='Anzahl der Tweets pro Symbol')
    parser.add_argument('--reddit-limit', type=int, default=100, help='Maximale Anzahl der Reddit-Posts pro Symbol')
    
    args = parser.parse_args()
    
    try:
        fetcher = SocialMediaSentimentFetcher(
            twitter_api_key=args.twitter_api_key,
            twitter_api_secret=args.twitter_api_secret,
            twitter_access_token=args.twitter_access_token,
            twitter_access_token_secret=args.twitter_access_token_secret,
            reddit_client_id=args.reddit_client_id,
            reddit_client_secret=args.reddit_client_secret
        )
        fetcher.fetch_social_media_sentiment(
            symbols=args.symbols,
            twitter_count=args.twitter_count,
            reddit_limit=args.reddit_limit
        )
    except Exception as e:
        rprint(f"[red]Fehler: {str(e)}[/red]")

if __name__ == "__main__":
    main() 