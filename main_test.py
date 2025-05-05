import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Import our modular components
from utils.styles import apply_custom_styles
from utils.sidebar import render_sidebar
from utils.stock_preview import display_stock_preview
from utils.company_profile import display_company_profile
from utils.analysis import run_analysis
from utils.valuation_dashboard import display_valuation_dashboard

# Set page configuration
st.set_page_config(
    page_title="AI Stock Analysis Crew",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_styles()

# Main function to run the app
def main():
    # Render sidebar
    render_sidebar()

    # Main content
    st.markdown("<h1 class='main-header'>🤖 AI Stock Investment Crew</h1>", unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns([3, 1])
    with col1:
        if 'stock_symbol' not in st.session_state:
            st.session_state['stock_symbol'] = "AAPL"
        
        stock_symbol = st.text_input("Enter Stock Symbol:", 
                                    value=st.session_state['stock_symbol'],
                                    placeholder="e.g., AAPL, MSFT, GOOGL")

    with col2:
        st.write("")
        st.write("")
        analyze_button = st.button("🚀 Run Analysis", use_container_width=True)

    # Preview current stock price and chart before analysis
    if stock_symbol:
        try:
            # Fetch basic stock data
            ticker_data = yf.Ticker(stock_symbol.strip().upper())
            info = ticker_data.info
            
            # Display stock preview
            display_stock_preview(ticker_data, stock_symbol)
            
            # Display company profile expander
            display_company_profile(info)

            display_valuation_dashboard(stock_symbol)
                
        except Exception as e:
            st.error(f"Error retrieving stock data: {str(e)}")
            st.markdown(f"<details><summary>Error Details</summary>{str(e)}</details>", unsafe_allow_html=True)

    # Run the analysis when button is clicked
    if analyze_button:
        if stock_symbol.strip() == "":
            st.warning("⚠️ Please enter a valid stock symbol.")
        else:
            run_analysis(stock_symbol)

if __name__ == "__main__":
    main()