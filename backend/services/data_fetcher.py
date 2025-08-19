# backend/services/data_fetcher.py

import yfinance as yf
# ... other imports ...
from newsapi import NewsApiClient
from datetime import datetime
import logging, time
from .config import NEWS_API_KEY

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# --- get_yahoo_finance_data (MODIFIED) ---
def get_yahoo_finance_data(ticker_symbol: str):
    """
    V3: Now fetches critical fundamental ratios for true credit assessment.
    """
    logging.info(f"Fetching yfinance data for ticker: {ticker_symbol}")
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist_data = ticker.history(period="1y")
        if hist_data.empty: return None
        hist_data.index = hist_data.index.map(lambda x: x.strftime('%Y-%m-%d'))
        info = ticker.info
        
        # --- ADDING FUNDAMENTAL DATA ---
        return {
            "historical_data": hist_data.to_dict(orient="index"),
            "info": {
                "longName": info.get("longName"), "sector": info.get("sector"),
                "marketCap": info.get("marketCap"), "trailingPE": info.get("trailingPE"),
                "dividendYield": info.get("dividendYield"),
                "debtToEquity": info.get("debtToEquity"), # CRITICAL
                "totalCashPerShare": info.get("totalCashPerShare") # CRITICAL
            }
        }
    except Exception as e:
        logging.error(f"yfinance error for {ticker_symbol}: {e}")
        return None

# ... (get_market_sentiment_data and get_news_data are unchanged) ...
def get_market_sentiment_data():
    try:
        logging.info("Fetching S&P 500 data for market sentiment.")
        sp500 = yf.Ticker("^GSPC"); hist = sp500.history(period="4mo")
        if hist.empty or len(hist) < 2:
            logging.warning("Not enough S&P 500 data to calculate market sentiment."); return 0.0
        price_now = hist['Close'].iloc[-1]; price_ago = hist['Close'].iloc[0]
        market_sentiment_pct = ((price_now - price_ago) / price_ago) * 100
        return market_sentiment_pct
    except Exception as e:
        logging.error(f"Could not fetch market sentiment data: {e}"); return 0.0
def get_news_data(query: str):
    if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_API_KEY":
        logging.warning("NewsAPI key not configured. Skipping news fetch."); return None
    from datetime import timedelta
    logging.info(f"Fetching news from NewsAPI for query: '{query}'")
    try:
        from_date = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')
        all_articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy', from_param=from_date, page_size=20)
        return [{"source": article["source"]["name"], "title": article["title"], "url": article["url"], "publishedAt": article["publishedAt"], "content": article.get("content", "")} for article in all_articles["articles"]]
    except Exception as e:
        logging.error(f"NewsAPI error for query '{query}': {e}"); return None