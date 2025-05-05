import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from crew import create_crew
import json
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="AI Stock Analysis Crew",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 20px;
        text-align: center;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
    }
    .success-box {
        background-color: #f0fff0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .dashboard-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
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
        import random
        selected = random.choice(list(popular_stocks.items()))
        st.session_state['stock_symbol'] = selected[1]
        st.success(f"Selected: {selected[0]} ({selected[1]})")

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
        
        # Display info card
        col1, col2, col3 = st.columns(3)
        
        # Get stock price history
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        hist = ticker_data.history(start=start_date, end=end_date)
        
        with st.expander("📈 View Detailed Charts & Technical Analysis"):

            # Add a time range selector
            time_options = {
                "1M": 30,
                "3M": 90, 
                "6M": 180,
                "1Y": 365,
                "5Y": 365*5
            }
            
            selected_range = st.radio(
                "Select Time Range:",
                options=list(time_options.keys()),
                index=1,  # Default to 3M
                horizontal=True
            )
            
            chart_type = st.selectbox(
                "Chart Type:",
                ["Price", "Candlestick", "OHLC", "Volume + Price"],
                index=0
            )

            # Technical indicators options
            show_ma = st.checkbox("Show Moving Averages", value=True)
            show_bb = st.checkbox("Show Bollinger Bands", value=False)
            
            # Get historical data based on selected time range
            days = time_options[selected_range]
            range_start = end_date - timedelta(days=days)
            range_hist = ticker_data.history(start=range_start, end=end_date)
            
            # Create figure based on selected chart type
            detail_fig = go.Figure()
            
            if chart_type == "Price":
                detail_fig.add_trace(go.Scatter(
                    x=range_hist.index,
                    y=range_hist['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='royalblue', width=2)
                ))
            
            elif chart_type == "Candlestick":
                detail_fig.add_trace(go.Candlestick(
                    x=range_hist.index,
                    open=range_hist['Open'],
                    high=range_hist['High'],
                    low=range_hist['Low'],
                    close=range_hist['Close'],
                    name="OHLC"
                ))
                # Candlestick styling
                detail_fig.update_layout(xaxis_rangeslider_visible=False)
            
            elif chart_type == "OHLC":
                detail_fig.add_trace(go.Ohlc(
                    x=range_hist.index,
                    open=range_hist['Open'],
                    high=range_hist['High'],
                    low=range_hist['Low'],
                    close=range_hist['Close'],
                    name="OHLC"
                ))
                # OHLC styling
                detail_fig.update_layout(xaxis_rangeslider_visible=False)
            
            # Add technical indicators if selected
            if show_ma:
                # Calculate Moving Averages
                range_hist['MA20'] = range_hist['Close'].rolling(window=20).mean()
                range_hist['MA50'] = range_hist['Close'].rolling(window=50).mean()
                
                detail_fig.add_trace(go.Scatter(
                    x=range_hist.index,
                    y=range_hist['MA20'],
                    mode='lines',
                    name='20-Day MA',
                    line=dict(color='orange', width=1.5)
                ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
                
                detail_fig.add_trace(go.Scatter(
                    x=range_hist.index,
                    y=range_hist['MA50'],
                    mode='lines',
                    name='50-Day MA',
                    line=dict(color='magenta', width=1.5)
                ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
            
            if show_bb:
                # Calculate Bollinger Bands
                window = 20
                range_hist['MA'] = range_hist['Close'].rolling(window=window).mean()
                range_hist['STD'] = range_hist['Close'].rolling(window=window).std()
                range_hist['Upper'] = range_hist['MA'] + (range_hist['STD'] * 2)
                range_hist['Lower'] = range_hist['MA'] - (range_hist['STD'] * 2)
                
                detail_fig.add_trace(go.Scatter(
                    x=range_hist.index,
                    y=range_hist['Upper'],
                    mode='lines',
                    name='Upper BB',
                    line=dict(color='rgba(0, 128, 0, 0.5)', width=1),
                    showlegend=True
                ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
                
                detail_fig.add_trace(go.Scatter(
                    x=range_hist.index,
                    y=range_hist['Lower'],
                    mode='lines',
                    name='Lower BB',
                    line=dict(color='rgba(0, 128, 0, 0.5)', width=1),
                    fill='tonexty',
                    fillcolor='rgba(0, 128, 0, 0.1)',
                    showlegend=True
                ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
            
            # Update layout for better appearance
            detail_fig.update_layout(
                title=f"{stock_symbol} - {selected_range} {chart_type} Chart",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                height=500,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(detail_fig, use_container_width=True)
        
        # Add a small performance metrics box
            st.markdown("### Performance Metrics")

            if not range_hist.empty and len(range_hist) > 1:
                start_price = range_hist['Close'].iloc[0]
                end_price = range_hist['Close'].iloc[-1]
                period_return = ((end_price / start_price) - 1) * 100
                
                # Calculate volatility (standard deviation of daily returns)
                daily_returns = range_hist['Close'].pct_change().dropna()
                volatility = daily_returns.std() * (252 ** 0.5) * 100  # Annualized
                
                # Calculate max drawdown
                cumulative_returns = (1 + daily_returns).cumprod()
                running_max = cumulative_returns.cummax()
                drawdown = (cumulative_returns / running_max) - 1
                max_drawdown = drawdown.min() * 100
                
                # Create table with metrics
                performance_metrics = {
                    "Metric": ["Period Return", "Annualized Volatility", "Max Drawdown", "Avg Daily Volume"],
                    "Value": [
                        f"{period_return:.2f}%",
                        f"{volatility:.2f}%",
                        f"{max_drawdown:.2f}%",
                        f"{range_hist['Volume'].mean():,.0f}"
                    ]
                }
                
                st.dataframe(pd.DataFrame(performance_metrics), hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        # COLLAPSIBLE COMPANY PROFILE
        #st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        with st.expander("📋 Company Profile & Details"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Company Overview")
                st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
                st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
                st.markdown(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})")
                st.markdown(f"**Business Summary:**")
                st.markdown(f"{info.get('longBusinessSummary', 'No summary available.')[:500]}...")
            
            with col2:
                st.subheader("Key Statistics")
                metrics = {
                    "Revenue (TTM)": f"${info.get('totalRevenue', 0)/1e9:.2f}B" if info.get('totalRevenue') else "N/A",
                    "Profit Margin": f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else "N/A",
                    "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A",
                    "Debt to Equity": f"{info.get('debtToEquity', 'N/A')}" if info.get('debtToEquity') else "N/A",
                    "Return on Equity": f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else "N/A",
                    "Beta": f"{info.get('beta', 'N/A')}" if info.get('beta') else "N/A"
                }
                
                for key, value in metrics.items():
                    st.markdown(f"**{key}:** {value}")
            
            # Executive team info (if available)
            if info.get('companyOfficers'):
                st.subheader("Key Executives")
                executives = info.get('companyOfficers', [])[:5]  # Limit to top 5
                if executives:
                    exec_data = []
                    for exec in executives:
                        if exec.get('name'):
                            exec_data.append({
                                "Name": exec.get('name', ''),
                                "Title": exec.get('title', ''),
                                "Age": exec.get('age', 'N/A'),
                            })
                    if exec_data:
                        st.dataframe(pd.DataFrame(exec_data), hide_index=True)
            
            # Financial ratios
            st.subheader("Financial Ratios")
            fin_col1, fin_col2 = st.columns(2)
            
            with fin_col1:
                valuation_metrics = {
                    "Price to Book": info.get('priceToBook', 'N/A'),
                    "Price to Sales": info.get('priceToSalesTrailing12Months', 'N/A'),
                    "Enterprise Value/EBITDA": info.get('enterpriseToEbitda', 'N/A'),
                    "Forward P/E": info.get('forwardPE', 'N/A')
                }
                
                st.markdown("**Valuation Ratios**")
                for key, value in valuation_metrics.items():
                    formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else value
                    st.markdown(f"**{key}:** {formatted_value}")
                    
            with fin_col2:
                growth_metrics = {
                    "Revenue Growth YoY": info.get('revenueGrowth', 'N/A'),
                    "Earnings Growth YoY": info.get('earningsGrowth', 'N/A'),
                    "Free Cash Flow": f"${info.get('freeCashflow', 0)/1e9:.2f}B" if info.get('freeCashflow') else "N/A",
                    "Operating Margin": f"{info.get('operatingMargins', 0)*100:.2f}%" if info.get('operatingMargins') else "N/A"
                }
                
                st.markdown("**Growth & Profitability**")
                for key, value in growth_metrics.items():
                    formatted_value = f"{value*100:.2f}%" if isinstance(value, (int, float)) and "Growth" in key else value
                    st.markdown(f"**{key}:** {formatted_value}")
            
            # Institutional ownership
            st.subheader("Ownership Structure")
            ownership_col1, ownership_col2 = st.columns(2)
            
            with ownership_col1:
                st.markdown("**Institutional Ownership**")
                inst_ownership = info.get('institutionPercentHeld', 0) * 100 if info.get('institutionPercentHeld') else 0
                insider_ownership = info.get('heldPercentInsiders', 0) * 100 if info.get('heldPercentInsiders') else 0
                individual_ownership = 100 - inst_ownership - insider_ownership
                
                # Create ownership data for the pie chart
                ownership_data = [
                    {'type': 'Institutional', 'percentage': inst_ownership},
                    {'type': 'Insider', 'percentage': insider_ownership},
                    {'type': 'Individual/Other', 'percentage': individual_ownership}
                ]
                
                # Create ownership pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=[d['type'] for d in ownership_data],
                    values=[d['percentage'] for d in ownership_data],
                    hole=.3,
                    marker_colors=['royalblue', 'lightblue', 'skyblue']
                )])
                
                fig.update_layout(
                    title="Ownership Distribution",
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with ownership_col2:
                st.markdown("**Major Holders**")
                # In a real implementation, you would fetch actual major holders
                # Here we're creating placeholder data
                major_holders = [
                    {"Institution": "Vanguard Group", "Percentage": "7.8%"},
                    {"Institution": "BlackRock Inc.", "Percentage": "6.2%"},
                    {"Institution": "State Street Corporation", "Percentage": "4.1%"},
                    {"Institution": "FMR, LLC", "Percentage": "3.5%"},
                    {"Institution": "Geode Capital Management", "Percentage": "1.9%"}
                ]
                
                st.dataframe(pd.DataFrame(major_holders), hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error retrieving stock data: {str(e)}")
        st.markdown(f"<details><summary>Error Details</summary>{str(e)}</details>", unsafe_allow_html=True)

# Run the analysis when button is clicked
if analyze_button:
    if stock_symbol.strip() == "":
        st.warning("⚠️ Please enter a valid stock symbol.")
    else:
        # Create progress bar and status message
        progress_bar = st.progress(0)
        status_message = st.empty()
        
        try:
            # Status updates
            status_message.markdown("🔍 **Status**: Initializing analysis agents...")
            progress_bar.progress(10)
            
            # Run the analysis
            status_message.markdown("📊 **Status**: Running stock research and analysis...")
            progress_bar.progress(30)
            
            crew_result = create_crew(stock_symbol.strip().upper())
            
            # Update progress as each task completes
            status_message.markdown("📈 **Status**: Analyzing sentiment data...")
            progress_bar.progress(60)
            
            status_message.markdown("💹 **Status**: Generating investment strategies...")
            progress_bar.progress(80)
            
            status_message.markdown("📝 **Status**: Compiling final report...")
            progress_bar.progress(100)
            
            # Show completion message
            st.success("✅ Analysis Complete!")
            
            # Create tabs for different outputs
            tabs = st.tabs(["Full Report", "Research", "Sentiment", "Analysis", "Strategy"])
            
            with tabs[0]:
                st.markdown(crew_result.tasks_output[-1].raw)  # Get last task output
            
            with tabs[1]:
                st.markdown("### 📊 Stock Research Results")
                st.markdown(crew_result.tasks_output[0].raw)
                
            with tabs[2]:
                st.markdown("### 👥 Sentiment Analysis")
                st.markdown(crew_result.tasks_output[2].raw)
                
            with tabs[3]:
                st.markdown("### 🔍 Financial Analysis")
                st.markdown(crew_result.tasks_output[1].raw)
                
            with tabs[4]:
                st.markdown("### 💰 Investment Strategy")
                st.markdown(crew_result.tasks_output[3].raw)
                
        except Exception as e:
            st.error(f"🚨 Something went wrong: {str(e)}")
            st.markdown(f"<details><summary>Error Details</summary>{str(e)}</details>", unsafe_allow_html=True)