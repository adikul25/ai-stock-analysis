import streamlit as st
from crew import create_crew
import json

def run_analysis(stock_symbol):
    """
    Run the AI crew analysis on the stock symbol
    
    Args:
        stock_symbol: The stock symbol to analyze
    """
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
        
        # Display results in tabs
        display_analysis_results(crew_result)
        
    except Exception as e:
        st.error(f"🚨 Something went wrong: {str(e)}")
        st.markdown(f"<details><summary>Error Details</summary>{str(e)}</details>", unsafe_allow_html=True)

def display_analysis_results(crew_result):
    """
    Display analysis results in tabs
    
    Args:
        crew_result: The result object from the AI crew analysis
    """
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