import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

def display_stock_preview(ticker_data, stock_symbol):
    """
    Display the stock preview with detailed charts and technical analysis
    
    Args:
        ticker_data: The yfinance ticker object
        stock_symbol: The stock symbol as a string
    """
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
        
        # Create the chart
        create_chart(range_hist, stock_symbol, selected_range, chart_type, show_ma, show_bb)
        
        # Add performance metrics
        display_performance_metrics(range_hist)

def create_chart(range_hist, stock_symbol, selected_range, chart_type, show_ma, show_bb):
    """Create the appropriate chart based on user selections"""
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
        add_moving_averages(detail_fig, range_hist, chart_type)
    
    if show_bb:
        add_bollinger_bands(detail_fig, range_hist, chart_type)
    
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

def add_moving_averages(fig, hist_data, chart_type):
    """Add moving averages to the chart"""
    # Calculate Moving Averages
    hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
    hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['MA20'],
        mode='lines',
        name='20-Day MA',
        line=dict(color='orange', width=1.5)
    ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['MA50'],
        mode='lines',
        name='50-Day MA',
        line=dict(color='magenta', width=1.5)
    ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)

def add_bollinger_bands(fig, hist_data, chart_type):
    """Add Bollinger Bands to the chart"""
    # Calculate Bollinger Bands
    window = 20
    hist_data['MA'] = hist_data['Close'].rolling(window=window).mean()
    hist_data['STD'] = hist_data['Close'].rolling(window=window).std()
    hist_data['Upper'] = hist_data['MA'] + (hist_data['STD'] * 2)
    hist_data['Lower'] = hist_data['MA'] - (hist_data['STD'] * 2)
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Upper'],
        mode='lines',
        name='Upper BB',
        line=dict(color='rgba(0, 128, 0, 0.5)', width=1),
        showlegend=True
    ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)
    
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Lower'],
        mode='lines',
        name='Lower BB',
        line=dict(color='rgba(0, 128, 0, 0.5)', width=1),
        fill='tonexty',
        fillcolor='rgba(0, 128, 0, 0.1)',
        showlegend=True
    ), row=1 if chart_type == "Volume + Price" else None, col=1 if chart_type == "Volume + Price" else None)

def display_performance_metrics(hist_data):
    """Display performance metrics for the selected time period"""
    st.markdown("### Performance Metrics")

    if not hist_data.empty and len(hist_data) > 1:
        start_price = hist_data['Close'].iloc[0]
        end_price = hist_data['Close'].iloc[-1]
        period_return = ((end_price / start_price) - 1) * 100
        
        # Calculate volatility (standard deviation of daily returns)
        daily_returns = hist_data['Close'].pct_change().dropna()
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
                f"{hist_data['Volume'].mean():,.0f}"
            ]
        }
        
        st.dataframe(pd.DataFrame(performance_metrics), hide_index=True)