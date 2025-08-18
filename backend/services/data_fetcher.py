# backend/services/data_fetcher.py

import yfinance as yf
import pandas_datareader.data as pdr
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import logging

# Import the API key from our config file
from backend.services.config import NEWS_API_KEY

# --- INITIALIZATIONS ---

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the NewsAPI client
try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
except Exception as e:
    logging.error(f"Failed to initialize NewsApiClient. Check your API key in config.py. Error: {e}")
    newsapi = None

# --- DATA FETCHING FUNCTIONS ---

def get_yahoo_finance_data(ticker_symbol: str):
    """Fetches structured stock and company data from Yahoo Finance."""
    logging.info(f"Fetching yfinance data for ticker: {ticker_symbol}")
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist_data = ticker.history(period="1y")

        if hist_data.empty:
            logging.warning(f"No historical data from yfinance for {ticker_symbol}. It may be an invalid ticker.")
            return None

        hist_data.index = hist_data.index.astype(str)  # <-- Fix here
        info = ticker.info

        return {
            "historical_data": hist_data.to_dict(orient="index"),
            "info": {
                "longName": info.get("longName"), "sector": info.get("sector"),
                "industry": info.get("industry"), "country": info.get("country"),
                "marketCap": info.get("marketCap"), "trailingPE": info.get("trailingPE"),
                "dividendYield": info.get("dividendYield")
            }
        }
    except Exception as e:
        logging.error(f"yfinance error for {ticker_symbol}: {e}")
        return None

def get_world_bank_data(country_code: str = "WLD", indicator: str = "NY.GDP.MKTP.KD.ZG"):
    """Fetches structured macroeconomic data from the World Bank."""
    logging.info(f"Fetching World Bank data for indicator: {indicator}")
    try:
        start_year = datetime.now().year - 20
        end_year = datetime.now().year
        
        # pandas-datareader requires an end date
        wb_data = pdr.DataReader(indicator, 'world-bank', start=start_year, end=end_year)
        
        wb_data = wb_data.reset_index()
        country_data = wb_data[wb_data['country'] == 'World'].copy() # Example: Using 'World' data
        country_data['year'] = country_data['year'].astype(str)
        
        return country_data.to_dict(orient="records")
    except Exception as e:
        logging.error(f"World Bank data fetching error: {e}")
        return None

def get_news_data(query: str):
    """Fetches unstructured news articles from NewsAPI."""
    if not newsapi:
        logging.error("NewsAPI client not initialized. Cannot fetch news.")
        return None
        
    logging.info(f"Fetching news from NewsAPI for query: '{query}'")
    try:
        from_date = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')
        
        all_articles = newsapi.get_everything(
            q=query, language='en', sort_by='relevancy', from_param=from_date, page_size=20
        )
        
        articles = [{
            "source": article["source"]["name"], "title": article["title"],
            "url": article["url"], "publishedAt": article["publishedAt"],
            "content": article.get("content", "")
        } for article in all_articles["articles"]]
        
        return articles
    except Exception as e:
        logging.error(f"NewsAPI error for query '{query}': {e}")
        return None