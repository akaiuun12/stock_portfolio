import time
import numpy as np
import pandas as pd

import streamlit as st
import plotly.graph_objects as go

import yfinance as yf
from finance import get_facts, annual_net_income, annual_dividends, historical_price
from finance.fundamentals import calculate_net_income_growth

# Helper function to format large numbers
def format_large_number(value):
    """Format large numbers to B/M/K format for better readability"""
    if abs(value) >= 1e9:
        return f"${value/1e9:.1f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.0f}"

def get_scale_and_suffix(data_series):
    """Determine the appropriate scale and suffix for a data series"""
    max_value = abs(data_series.max())
    if max_value >= 1e9:
        return 1e9, "B", "$B"
    elif max_value >= 1e6:
        return 1e6, "M", "$M"
    elif max_value >= 1e3:
        return 1e3, "K", "$K"
    else:
        return 1, "", "$"

# Configure page for better deployment experience
# This function must be the first Streamlit command in the app.
st.set_page_config(
    page_title="Long-Term Stock Tracker",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
        /* Used for: main app title: "📈 Long-term Stock Analysis" */
        .main-header { 
            font-size: 2.5rem;      /* Large text (40px) */
            font-weight: bold;      /* Bold text */
            color: #1f77b4;         /* Blue color */
            text-align: center;     /* Center alignment */
            margin-bottom: 1rem;    /* Space below */
        }
        /* Used for: Peter Lynch and Rockefeller quotes */
        .quote-box {
            background-color: #f0f2f6;      /* Light gray background */
            padding: 1rem;                  /* Internal spacing */
            border-radius: 10px;            /* Rounded corners */
            border-left: 4px solid #1f77b4; /* Blue left border */
            margin: 1rem 0;                 /* Vertical spacing */
        }
        /* Used for: Business summary and data containers */
        .metric-card {
            background-color: white;                /* White background */
            padding: 1rem;                          /* Internal spacing */
            border-radius: 10px;                    /* Rounded corners */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* Subtle shadow */
            margin: 0.5rem 0;                       /* Vertical spacing */
        }
        /* Used for: Error messages (currently defined but not used) */
        .error-box {
            background-color: #ffebee;    /* Light red background */
            color: #c62828;              /* Dark red text */
            padding: 1rem;               /* Internal spacing */
            border-radius: 10px;         /* Rounded corners */
            border-left: 4px solid #c62828; /* Red left border */
        }
    </style>
    """, 
    unsafe_allow_html=True # Allows HTML/CSS to be rendered (required for custom styling)
)

# # Cache expensive operations for better performance
# # 1. SEC EDGAR data (financial statements) - Cache for 1 hour
# @st.cache_data(ttl=3600, show_spinner="Fetching financial data...")
# def get_cached_facts(ticker):
#     return get_facts(ticker)

# # 2. Yahoo Finance company info - Cache for 30 minutes  
# @st.cache_data(ttl=1800, show_spinner="Fetching market data...")
# def get_cached_yf_info(ticker):
#     return yf.Ticker(ticker)

# # 3. Price data - Cache for 15 minutes
# @st.cache_data(ttl=900, show_spinner="Downloading price data...")
# def get_cached_price_data(ticker):
#     return yf.download(ticker, progress=False)
    
# --- App Header ---
st.markdown(
    r'<h1 class="main-header">📈 Long-term Stock Analysis</h1>', 
    unsafe_allow_html=True
)
st.markdown(r"""
    > Often, there is no correlation between the success of a company's
    operations and the success of its stock over a few months or even a few years.
    In the long term, there is a 100% correlation between the success of the
    company and the success of its stock. This disparity is the key to making money.  
    > **— Peter Lynch**
    """, 
    unsafe_allow_html=True
)

custom_ticker = st.text_input("Enter ticker symbol", placeholder="e.g., META, NFLX", key="custom_ticker")

st.markdown("---")

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("🎯 Stock Selection")
    
    # Favorite tickers with better layout
    st.subheader("Quick Select")
    favorite_tickers = ["AAPL", "AMZN", "MSFT", "GOOGL", "TSLA", "NVDA", "V", "KO"]
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        ticker1 = st.button("AAPL", key="btn_aapl")
        ticker2 = st.button("AMZN", key="btn_amzn")
        ticker3 = st.button("MSFT", key="btn_msft")
        ticker4 = st.button("GOOGL", key="btn_googl")
    
    with col2:
        ticker5 = st.button("TSLA", key="btn_tsla")
        ticker6 = st.button("NVDA", key="btn_nvda")
        ticker7 = st.button("V", key="btn_v")
        ticker8 = st.button("KO", key="btn_ko")

    # Determine selected ticker
    selected_ticker = None
    if ticker1: selected_ticker = "AAPL"
    elif ticker2: selected_ticker = "AMZN"
    elif ticker3: selected_ticker = "MSFT"
    elif ticker4: selected_ticker = "GOOGL"
    elif ticker5: selected_ticker = "TSLA"
    elif ticker6: selected_ticker = "NVDA"
    elif ticker7: selected_ticker = "V"
    elif ticker8: selected_ticker = "KO"
    elif custom_ticker: selected_ticker = custom_ticker.upper()
    else: selected_ticker = "AAPL"  # Default
    
    # Display current selection
    st.markdown(f"**Current Selection:** {selected_ticker}")
    
    # Add some spacing
    st.markdown("---")
    st.markdown("**Data Sources:**")
    st.markdown("• SEC EDGAR (Financial Data)")
    st.markdown("• Yahoo Finance (Market Data)")

# --- Main Content Area ---
# Show loading state
with st.spinner(f"Analyzing {selected_ticker}..."):
    # Fetch data with caching
    facts = get_facts(selected_ticker)
    facts_yf = yf.Ticker(selected_ticker)

# Error handling for data fetching
if not facts:
    st.error(f"❌ Unable to fetch financial data for {selected_ticker}")
    st.info("💡 Try a different ticker or check if the symbol is correct")
else:
    # Process financial data
    df_net_income, _, _ = annual_net_income(facts['facts'])
    df_dividends, _, _ = annual_dividends(facts['facts'])
    
    # Company information section
    st.header(f"🏢 {facts['entityName']}")
    
    # Business summary with error handling
    if facts_yf and facts_yf.info and 'longBusinessSummary' in facts_yf.info:
        try:
            business_summary = facts_yf.info['longBusinessSummary']
            sentences = business_summary.split('. ')
            if len(sentences) >= 2:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Business Summary:</strong><br>
                    {sentences[0]}.<br>
                    {sentences[1]}.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Business Summary:</strong><br>
                    {business_summary}
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.warning("Business summary not available")
    else:
        st.warning("Business summary not available")
    
    st.markdown("---")
    
    # --- Net Income Analysis ---
    st.header("💰 Net Income Analysis")
    st.markdown(r"""
    > "There are many theories, but to me, it always comes down to earnings and assets. Especially earnings."  
    > **— Peter Lynch**
    """, unsafe_allow_html=True)
    
    if df_net_income is not None and not df_net_income.empty:
        df_growth = calculate_net_income_growth(df_net_income)
        
        # Determine scale and suffix for net income data
        scale, suffix, axis_title = get_scale_and_suffix(df_growth["net_income"])
        
        # Create enhanced Plotly figure
        fig_income = go.Figure()
        
        # Bar chart for Net Income
        fig_income.add_trace(go.Bar(
            x=df_growth["year"],
            y=df_growth["net_income"] / scale,  # Scale data dynamically
            name=f"Net Income ({axis_title})",
            marker_color='skyblue',
            yaxis='y1',
            hovertemplate=f'<b>%{{x}}</b><br>Net Income: $%{{y:.1f}}{suffix}<extra></extra>'
        ))
        
        # Line chart for Net Income Growth (%)
        fig_income.add_trace(go.Scatter(
            x=df_growth["year"],
            y=df_growth["net_income_growth"].round(2),
            name="Growth Rate (%)",
            mode='lines+markers',
            marker_color='orange',
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
        ))
        
        # Enhanced layout
        fig_income.update_layout(
            title=f"Net Income and Growth Rate for {selected_ticker}",
            xaxis=dict(title="Year", showgrid=True, gridcolor='lightgray'),
            yaxis=dict(
                title=f"Net Income ({axis_title})",
                showgrid=True,
                gridcolor='lightgray',
                tickformat=".1f",
                tickprefix="$",
                ticksuffix=suffix,
            ),
            yaxis2=dict(
                title="Growth Rate (%)",
                overlaying='y',
                side='right',
                showgrid=False,
            ),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
            hovermode='x unified',
            dragmode=False,
            height=500
        )
        
        st.plotly_chart(fig_income, use_container_width=True, config={"displayModeBar": False})
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            latest_income = df_growth["net_income"].iloc[-1]
            st.metric("Latest Net Income", format_large_number(latest_income))
        with col2:
            avg_growth = df_growth["net_income_growth"].mean()
            st.metric("Average Growth", f"{avg_growth:.1f}%")
        with col3:
            years_data = len(df_growth)
            st.metric("Years of Data", f"{years_data}")
    else:
        st.warning("⚠️ No net income data available for this ticker")
    
    st.markdown("---")
    
    # --- Dividend Analysis ---
    st.header("💵 Dividend Analysis")
    st.markdown(r"""
    > "Do you know the only thing that gives me pleasure? It's to see my dividends coming in."  
    > **— John D. Rockefeller**
    """, unsafe_allow_html=True)
    
    if df_dividends is not None and not df_dividends.empty:
        # Calculate Dividend Growth (%)
        df_dividends["dividend_growth"] = df_dividends["dividends"].pct_change() * 100
        
        # Determine scale and suffix for dividend data
        scale, suffix, axis_title = get_scale_and_suffix(df_dividends["dividends"])
        
        # Create enhanced dividend chart
        fig_div = go.Figure()
        
        # Bar chart for Dividends
        fig_div.add_trace(go.Bar(
            x=df_dividends["year"],
            y=df_dividends["dividends"] / scale,  # Scale data dynamically
            name=f"Dividends ({axis_title})",
            marker_color='mediumseagreen',
            yaxis='y1',
            hovertemplate=f'<b>%{{x}}</b><br>Dividends: $%{{y:.2f}}{suffix}<extra></extra>'
        ))
        
        # Line chart for Dividend Growth (%)
        fig_div.add_trace(go.Scatter(
            x=df_dividends["year"],
            y=df_dividends["dividend_growth"].round(2),
            name="Growth Rate (%)",
            mode='lines+markers',
            marker_color='purple',
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
        ))
        
        fig_div.update_layout(
            title=f"Dividends and Growth Rate for {selected_ticker}",
            xaxis=dict(title="Year", showgrid=True, gridcolor='lightgray'),
            yaxis=dict(
                title=f"Dividends ({axis_title})",
                showgrid=True,
                gridcolor='lightgray',
                tickformat=".2f",
                tickprefix="$",
                ticksuffix=suffix,
            ),
            yaxis2=dict(
                title="Growth Rate (%)",
                overlaying='y',
                side='right',
                showgrid=False,
            ),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
            hovermode='x unified',
            dragmode=False,
            height=500
        )
        
        st.plotly_chart(fig_div, use_container_width=True, config={"displayModeBar": False})
        
        # Dividend summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            latest_div = df_dividends["dividends"].iloc[-1]
            st.metric("Latest Dividend", format_large_number(latest_div))
        with col2:
            avg_div_growth = df_dividends["dividend_growth"].mean()
            st.metric("Avg Div Growth", f"{avg_div_growth:.1f}%")
        with col3:
            div_years = len(df_dividends)
            st.metric("Dividend Years", f"{div_years}")
    else:
        st.warning("⚠️ No dividend data available for this ticker")

# --- Footer ---
st.markdown("---")

# --- Glossary Section (Collapsible) ---
with st.expander("📚 Glossary", expanded=True):
    st.markdown(r"""
    #### Growth Rate Calculation
    -   If the sign of value changes (from loss to profit or profit to loss), the growth rate is calculated as:
    
        $$$
        (\text{Current} - \text{Previous}) / |\text{Previous}| \times 100
        $$$
        
        This means a dramatic turnaround (e.g., from -10 to +30) will show as a large positive percentage (e.g., 400%). 
        This approach ensures that turnarounds from loss to profit are reported as large positive growth, 
        reflecting business reality rather than just mathematical sign.
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        📈 Built with Streamlit | Data from SEC EDGAR & Yahoo Finance
    </div>
    """, unsafe_allow_html=True)
