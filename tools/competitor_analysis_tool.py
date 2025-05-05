import yfinance as yf
from crewai.tools import tool

@tool
def competitor_analysis(ticker: str, num_competitors: int = 5):
    """
    Perform competitor analysis for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        num_competitors (int): Number of top competitors to analyze.

    Returns:
        dict: Competitor analysis results.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    sector = info.get('sectorKey')
    industry = info.get('industryKey')

    # Get competitors in the same industry
    industry_stocks = yf.Industry(f"{industry}").top_companies[:num_competitors].index.tolist()
    competitors = [comp for comp in industry_stocks if comp != ticker][:num_competitors]

    competitor_data = []
    for comp in competitors:
        comp_stock = yf.Ticker(comp)
        comp_info = comp_stock.info
        competitor_data.append({
            "ticker": comp,
            "name": comp_info.get('longName'),
            "market_cap": comp_info.get('marketCap'),
            "pe_ratio": comp_info.get('trailingPE'),
            "revenue_growth": comp_info.get('revenueGrowth'),
            "profit_margins": comp_info.get('profitMargins')
        })

    return {
        "main_stock": ticker,
        "industry": industry,
        "competitors": competitor_data
    }

#competitor_analysis("AAPL")