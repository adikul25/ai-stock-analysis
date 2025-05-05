import streamlit as st
import plotly.graph_objs as go
import pandas as pd

def display_company_profile(info):
    """
    Display the company profile expander with company details
    
    Args:
        info: The company info dictionary from yfinance
    """
    with st.expander("📋 Company Profile & Details"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_company_overview(info)
        
        with col2:
            display_key_statistics(info)
        
        # Executive team info
        display_executive_team(info)
        
        # Financial ratios
        display_financial_ratios(info)
        
        # Ownership structure
        display_ownership_structure(info)

def display_company_overview(info):
    """Display company overview information"""
    st.subheader("Company Overview")
    st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
    st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
    st.markdown(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})")
    st.markdown(f"**Business Summary:**")
    st.markdown(f"{info.get('longBusinessSummary', 'No summary available.')[:500]}...")

def display_key_statistics(info):
    """Display key company statistics"""
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

def display_executive_team(info):
    """Display executive team information if available"""
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

def display_financial_ratios(info):
    """Display financial ratios in two columns"""
    st.subheader("Financial Ratios")
    fin_col1, fin_col2 = st.columns(2)
    
    with fin_col1:
        display_valuation_ratios(info)
            
    with fin_col2:
        display_growth_metrics(info)

def display_valuation_ratios(info):
    """Display company valuation ratios"""
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

def display_growth_metrics(info):
    """Display company growth metrics"""
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

def display_ownership_structure(info):
    """Display ownership structure with charts"""
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
        display_major_holders()

def display_major_holders():
    """Display major holders data (placeholder)"""
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