import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CredLens", page_icon="🤖", layout="wide")

# -------------------------
# Load Font Awesome
# -------------------------
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

# -------------------------
# Custom CSS (Toolbar is now visible)
# -------------------------
st.markdown("""
    <style>
    /* Rules that hid the toolbar have been REMOVED from here */

    /* Sidebar button hover */
    .stButton button:hover {
        background-color: #ff3333 !important;
        transform: scale(1.05);
        box-shadow: 0px 4px 12px rgba(255, 0, 0, 0.4);
        transition: all 0.2s ease-in-out;
    }
    /* Sidebar input hover */
    .stTextInput input:hover {
        border: 2px solid #00c4cc !important;
        box-shadow: 0px 0px 8px rgba(0, 196, 204, 0.6);
        transition: all 0.2s ease-in-out;
    }
    /* Metric cards styling */
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 12px;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetric"] > div:first-child {
        font-size: 0.8em;
        font-weight: 600;
    }
    div[data-testid="stMetric"] > div:nth-child(2) {
        font-size: 1.8em;
        font-weight: 700;
    }
    /* Chart hover effect */
    .js-plotly-plot:hover {
        transform: scale(1.01);
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    /* News hover effect */
    a:hover {
        color: #00c4cc !important;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)


# -------------------------
# Configurations & Helpers
# -------------------------
AGENCY_RATINGS = {"AAPL": "AA+", "MSFT": "AAA", "GOOGL": "AA+", "NVDA": "A-", "JPM": "A-", "TSLA": "BB+"}
BACKEND_URL = "https://credit-risk-hackathon-production.up.railway.app/api/v1/score"

def get_api_data(ticker: str):
    """Fetches analysis data from the backend API."""
    try:
        response = requests.get(f"{BACKEND_URL}/{ticker}")
        if response.status_code == 500:
            st.error("An unexpected error occurred in the backend.")
            return None
        if response.status_code == 404:
            st.error(f"Could not find data for ticker '{ticker}'.")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        st.error("Error connecting to the backend API. Is the backend server running?")
        return None

def format_market_cap(mc):
    """Formats a large number into a human-readable market cap string."""
    if mc is None:
        return "N/A"
    if mc >= 1e12:
        return f"${mc/1e12:.2f} T"
    if mc >= 1e9:
        return f"${mc/1e9:.2f} B"
    if mc >= 1e6:
        return f"${mc/1e6:.2f} M"
    return str(mc)


# -------------------------
# Main UI Layout
# -------------------------

st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1em;">
        <div style="font-size: 2.5em; margin-right: 10px; font-weight: bold;
                    background: linear-gradient(45deg, #00897B, #01579B);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    color: transparent;">
            <i class="fa-solid fa-arrow-trend-up"></i> CredLens
        </div>
        <div style="font-size: 1.8em; color: #666;">
            Credit Scorecard
        </div>
    </div>
""", unsafe_allow_html=True)


st.sidebar.header("Analysis Options")
ticker_input = st.sidebar.text_input("Enter Company Ticker", value="SMCI").upper()
analyze_button = st.sidebar.button("Analyze Creditworthiness", type="primary")
st.sidebar.info("Enter a stock ticker (e.g., AAPL, SMCI, BA) to get its real-time, explainable stability score.")


# -------------------------
# Main Analysis Section
# -------------------------
if analyze_button:
    if not ticker_input:
        st.warning("Please enter a company ticker.")
    else:
        with st.spinner(f"Analyzing {ticker_input}..."):
            api_data = get_api_data(ticker_input)

        if api_data:
            score_result = api_data['score_result']
            info = api_data.get('company_info', {})
            company_name = api_data.get('company_name', ticker_input)
            
            # Default to light theme for charts - can be customized in the future
            plotly_template = 'plotly_white'
            
            st.header(f"Analysis for {company_name}")

            score = score_result.get('stability_score', 0)
            if score_result.get('assessment_type') != 'Heuristic':
                if score > 75:
                    st.success("✅ Stable: Credit-risk under control.")
                elif score > 50:
                    st.warning("⚠ Neutral: Some factors indicate potential risk.")
                else:
                    st.error("🚨 Volatile: Significant downside risk detected.")
            
            # --- Main Metrics Display ---
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if score_result.get('assessment_type') == 'Heuristic':
                    st.metric("Stability Score", score_result['stability_score'], "Heuristic")
                else:
                    outlook = 'Stable' if score > 75 else 'Neutral' if score > 50 else 'Volatile'
                    st.metric("Stability Score", score, f"{outlook} Outlook")
            
            with col2:
                sentiment = score_result.get('latest_sentiment', 0.0)
                sentiment_text = "Positive" if sentiment > 0.05 else "Negative" if sentiment < -0.05 else "Neutral"
                st.metric("News Sentiment", f"{sentiment:.2f}", sentiment_text)

            with col3:
                st.metric("Market Cap", format_market_cap(info.get('marketCap')))

            with col4:
                st.metric("P/E Ratio", f"{info.get('trailingPE'):.2f}" if info.get('trailingPE') else "N/A")

            with col5:
                st.metric("S&P Rating", AGENCY_RATINGS.get(ticker_input, "N/A"))

            st.markdown("---")

            # --- Chart Display ---
            col1, col2 = st.columns((1, 1))
            with col1:
                st.subheader("Why this score? (Key Drivers)")
                if score_result.get('assessment_type') == 'Heuristic':
                    st.warning("The ML model could not be trained. A qualitative assessment is provided instead.")
                    st.subheader("Qualitative Observations")
                    for obs in score_result['explanation']:
                        st.markdown(f"- {obs['feature']}: {obs['value']}")
                else:
                    explanation_df = pd.DataFrame(score_result['explanation'])
                    explanation_df = explanation_df[explanation_df['impact'].abs() > 0.001]
                    explanation_df['impact_description'] = explanation_df['impact'].apply(lambda x: "Increases Risk" if x > 0 else "Decreases Risk")
                    explanation_df['impact_abs'] = explanation_df['impact'].abs()
                    fig_drivers_chart = px.bar(
                        explanation_df,
                        x='impact_abs',
                        y='feature',
                        color='impact_description',
                        color_discrete_map={'Increases Risk': '#FF4B4B', 'Decreases Risk': '#2ECC71'},
                        orientation='h',
                        labels={'impact_abs': 'Magnitude of Impact', 'feature': 'Feature'},
                        template=plotly_template
                    )
                    fig_drivers_chart.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        title="Feature Impact on Downside Risk",
                        height=400,
                        margin=dict(l=170)
                    )
                    st.plotly_chart(fig_drivers_chart, use_container_width=True)

            with col2:
                st.subheader("Historical Stock Performance (1 Year)")
                stock_df = pd.DataFrame.from_dict(api_data['stock_history'], orient='index')
                stock_df.index = pd.to_datetime(stock_df.index)
                fig_stock_chart = px.line(
                    stock_df,
                    y='Close',
                    title=f"{ticker_input} Closing Price",
                    template=plotly_template
                )
                fig_stock_chart.update_layout(height=400)
                st.plotly_chart(fig_stock_chart, use_container_width=True)
            
            st.markdown("---")
            
            # --- News Display ---
            news = api_data.get('recent_news_for_context')
            if news:
                st.subheader("Recent News Headlines")
                for article in news:
                    st.markdown(f"[{article['title']}]({article['url']})** \n*Source: {article['source']} | Published: {pd.to_datetime(article['publishedAt']).strftime('%Y-%m-%d')}*")

else:
    st.info("Enter a ticker in the sidebar and click 'Analyze' to begin.")