import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool
)
from tools.yf_tech_analysis_tool import yf_tech_analysis
from tools.yf_fundamental_analysis_tool import yf_fundamental_analysis
from tools.competitor_analysis_tool import competitor_analysis
from tools.risk_assessment_tool import risk_assessment


# Load environment variables from .env file
load_dotenv()

# Set up the environment variable for Serper API key

def create_crew(stock_symbol):

    serper_api_key = os.getenv('SERPER_API_KEY')
    # Initialize Ollama LLM
    llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    temperature=0.2,
    api_key=os.getenv("GEMINI_API_KEY"),
    )

    search_tool = SerperDevTool()
    scraper_tool = ScrapeWebsiteTool()

    # Define Agents
    researcher = Agent(
        role='Stock Market Researcher',
        goal='Gather and analyze comprehensive data about the stock',
        backstory="You're an experienced stock market researcher with a keen eye for detail and a talent for uncovering hidden trends.",
        tools=[yf_tech_analysis, yf_fundamental_analysis, competitor_analysis],
        llm=llm
    )

    analyst = Agent(
        role='Financial Analyst',
        goal='Analyze the gathered data and provide investment insights',
        backstory="You're a seasoned financial analyst known for your accurate predictions and ability to synthesize complex information.",
        tools=[yf_tech_analysis, yf_fundamental_analysis, risk_assessment],
        llm=llm
    )

    sentiment_analyst = Agent(
        role='Sentiment Analyst',
        goal='Analyze market sentiment and its potential impact on the stock',
        backstory="You're an expert in behavioral finance and sentiment analysis, capable of gauging market emotions and their effects on stock performance.",
        tools=[search_tool, scraper_tool],
        llm=llm
    )

    strategist = Agent(
        role='Investment Strategist',
        goal='Develop a comprehensive investment strategy based on all available data',
        backstory="You're a renowned investment strategist known for creating tailored investment plans that balance risk and reward.",
        tools=[],
        llm=llm
    )

    # Define Tasks
    research_task = Task(
        description=f"""Research {stock_symbol} comprehensively:
        1. Analyze fundamentals: P/E, PEG, debt ratios, profitability, growth metrics
        2. Perform technical analysis: SMAs, RSI, MACD, support/resistance levels, patterns
        3. Compare with key competitors on valuation, growth, and market position""",
        agent=researcher,
        expected_output="""A structured summary including:
        1. Key fundamental metrics with interpretations
        2. Technical indicators and price action insights
        3. Competitive positioning analysis
        4. Identified strengths/weaknesses
        5. Data-driven outlook across timeframes"""
    )

    analysis_task = Task(
        description=f"""Synthesize research and sentiment data for {stock_symbol}:
        1. Connect technical, fundamental, and sentiment indicators
        2. Assess specific risks with probability ratings
        3. Identify opportunities and optimal entry/exit points""",
        agent=analyst,
        expected_output="""An analysis report with:
        1. Integrated findings across all data sources
        2. Quantified risk assessment
        3. Opportunity analysis with scenarios
        4. Data-driven conviction rating (Buy/Hold/Sell)"""
)

    sentiment_task = Task(
        description=f"""Analyze {stock_symbol} market sentiment:
        1. Evaluate recent news coverage and themes from multiple sources
        2. Assess social media sentiment patterns
        3. Review analyst opinions and institutional activity
        4. Document ALL sources used (with URLs when available)
        5. Note the publication date of each source""",
        agent=sentiment_analyst,
        expected_output="""A sentiment report containing:
        1. Quantified sentiment scores (bullish/bearish/neutral)
        2. Key sentiment drivers with evidence
        3. Recent sentiment shifts and catalysts
        4. Sentiment-based price predictions with confidence level
        5. Source appendix with links to all referenced content
        6. Citation of specific sources throughout the analysis"""
    )

    strategy_task = Task(
        description=f"""Develop investment strategies for {stock_symbol} based on previous analyses:
        1. Create recommendations for different investor profiles
        2. Provide strategies across short, mid, and long-term horizons
        3. Include contingency plans for different market scenarios""",
        agent=strategist,
        expected_output="""An actionable strategy containing:
        1. Clear recommendation with conviction level
        2. Tailored approaches by investor risk tolerance
        3. Specific entry points, targets, and stop-losses
        4. Risk management guidelines
        5. Timeline-based roadmap with triggers for strategy adjustments""",
        context=[research_task, analysis_task, sentiment_task]
    )

    # Create Crew
    crew = Crew(
        agents=[researcher, analyst, sentiment_analyst, strategist],
        tasks=[research_task, analysis_task, sentiment_task, strategy_task],
        process=Process.sequential,
        output_log_file="crew_logs.txt",
    )

    result = crew.kickoff()

    return result
    


