# backend/main.py

from fastapi import FastAPI, HTTPException
# --- THIS IS THE LINE TO CHANGE ---
from backend.services import data_fetcher  # Use absolute import

app = FastAPI(
    title="CredTech AI API",
    description="API for the Explainable Credit Intelligence Platform.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"message": "Welcome to the CredTech AI Backend!"}


@app.get("/api/v1/fetch-all/{ticker}")
def fetch_all_data(ticker: str):
    """
    An endpoint to fetch all combined data for a given company ticker.
    """
    print(f"Fetching all data for ticker: {ticker}")
    
    # 1. Fetch Yahoo Finance Data
    yf_data = data_fetcher.get_yahoo_finance_data(ticker)
    if not yf_data:
        raise HTTPException(status_code=404, detail=f"Could not fetch data for ticker {ticker}. Invalid or delisted symbol.")
    
    company_name = yf_data["info"].get("longName", ticker)
    
    # 2. Fetch World Bank Data
    wb_data = data_fetcher.get_world_bank_data()

    # 3. Fetch News Data
    news_data = data_fetcher.get_news_data(query=company_name)

    return {
        "ticker": ticker,
        "company_info": yf_data["info"],
        "stock_history": yf_data["historical_data"],
        "macro_economic_context": wb_data,
        "recent_news": news_data
    }