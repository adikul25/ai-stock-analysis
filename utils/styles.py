import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
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