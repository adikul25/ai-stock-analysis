import streamlit as st
import random

def render_sidebar():
    """Create and render the sidebar"""
    with st.sidebar:
        st.markdown("## 🔍 AI Stock Analysis")
        st.markdown("This tool uses AI agents to analyze stocks from multiple perspectives:")
        st.markdown("- 📊 **Technical Analysis**")
        st.markdown("- 💰 **Fundamental Analysis**")
        st.markdown("- 👥 **Sentiment Analysis**")
        st.markdown("- 🧠 **Strategic Recommendations**")
        
        st.markdown("---")
        st.markdown("### Quick Search")
        popular_stocks = {
            "Apple": "AAPL",
            "Microsoft": "MSFT",
            "Google": "GOOGL",
            "Amazon": "AMZN",
            "Tesla": "TSLA",
            "Nvidia": "NVDA"
        }
        
        if st.button("Random Popular Stock"):
            selected = random.choice(list(popular_stocks.items()))
            st.session_state['stock_symbol'] = selected[1]
            st.success(f"Selected: {selected[0]} ({selected[1]})")