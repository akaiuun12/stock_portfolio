import numpy as np
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from finance import get_facts, annual_net_income, annual_dividends, historical_price
from finance.fundamentals import calculate_net_income_growth
import pandas as pd

# --- App Title ---
st.title("Long-term Stock Analysis")

st.markdown(r'''
>"In the long term, there is a 100% correlation between the success of the company and the success of its stock.  
>\-- Peter Lynch \--
''')

# --- Ticker Input (Main Area) and Retrieve Financial Data  ---
with st.expander("Favorite Tickers"):
    ticker = st.radio("Choose", 
                      ["AAPL", "AMZN", "MSFT", "GOOGL", "TSLA", "NVDA", "V", "KO"], 
                      horizontal=True)

custom_ticker = st.text_input("Enter another ticker", value=ticker)

ticker = custom_ticker if custom_ticker != ticker else ticker

st.divider() # ---------------------------------------------
facts = get_facts(ticker)
facts_yf = yf.Ticker(ticker)

if not facts: 
    st.warning("No Data Available.")
else:
    df_net_income, _, _ = annual_net_income(facts['facts'])
    df_dividends, _, _ = annual_dividends(facts['facts'])

    st.header(f"{facts['entityName']}")
    st.markdown(f'''
        {facts_yf.info['longBusinessSummary'].split('. ')[0]+ '.'}
        {facts_yf.info['longBusinessSummary'].split('. ')[1]+ '.'}
    ''')

st.divider() # ---------------------------------------------

# --- Net Income and Net Income Growth Visualization ---
st.header("Net Income")
st.markdown(r'''
>"In the long term, there is a 100% correlation between the success of the company and the success of its stock.  
>\-- Peter Lynch \--
''')

if not facts:
    st.warning("No net income data available.")
elif df_net_income is not None and not df_net_income.empty:
    df_growth = calculate_net_income_growth(df_net_income)
    
    # Create Plotly figure with dual y-axes (custom mapping)
    fig_income = go.Figure()

    # Bar chart for Net Income
    fig_income.add_trace(go.Bar(
        x=df_growth["year"],
        y=df_growth["net_income"],
        name="Net Income",
        marker_color='skyblue',
        yaxis='y1'
    ))
    # Line chart for Net Income Growth (%)
    fig_income.add_trace(go.Scatter(
        x=df_growth["year"],
        y=df_growth["net_income_growth"].round(2),
        name="NI Growth (%)",
        mode='lines+markers',
        marker_color='orange',
        yaxis='y2'
    ))
    # Custom axis mapping
    fig_income.update_layout(
        title="Net Income and Net Income Growth (%)",
        xaxis=dict(title="Year"),
        yaxis=dict(
            title="Net Income ($)",
            showgrid=False,
            gridcolor='lightgray',
        ),
        yaxis2=dict(
            title="Net Income Growth (%)",
            overlaying='y',
            side='right',
            showgrid=False,
        ),
        legend=dict(x=0.01, y=0.99),
        dragmode=False
    )
    st.plotly_chart(
        fig_income, 
        use_container_width=True,
        config={
            "scrollZoom":False,
            "displayModeBar": False
        })
else:
    st.warning("No net income data available.")


st.divider() # ---------------------------------------------

# --- Dividends and Dividend Growth Visualization ---
st.header("Dividends")
st.markdown(r'''
>"Do you know the only thing that gives me pleasure? It's to see my dividends coming in."  
>\-- John D. Rockfeller \--
''')

if not facts:
    st.warning("No dividend data available.")
elif df_dividends is not None and not df_dividends.empty:
    # Calculate Dividend Growth (%)
    df_dividends["dividend_growth"] = df_dividends["dividends"].pct_change() * 100

    # Create Plotly figure with dual y-axes
    fig_div = go.Figure()
    # Bar chart for Dividends
    fig_div.add_trace(go.Bar(
        x=df_dividends["year"],
        y=df_dividends["dividends"],
        name="Dividends",
        marker_color='mediumseagreen',
        yaxis='y1'
    ))
    # Line chart for Dividend Growth (%)
    fig_div.add_trace(go.Scatter(
        x=df_dividends["year"],
        y=df_dividends["dividend_growth"].round(2),
        name="Div Growth (%)",
        mode='lines+markers',
        marker_color='purple',
        yaxis='y2'
    ))
    fig_div.update_layout(
        title="Dividends and Dividend Growth (%)",
        xaxis=dict(title="Year"),
        yaxis=dict(
            title="Dividends ($)",
            showgrid=True,
            gridcolor='lightgray',
        ),
        yaxis2=dict(
            title="Dividend Growth (%)",
            overlaying='y',
            side='right',
            showgrid=False,
        ),
        legend=dict(x=0.01, y=0.99),
        dragmode=False
    )
    st.plotly_chart(
        fig_div, 
        use_container_width=True,
        config={
            "scrollZoom":False,
            "displayModeBar": False
        })
else:
    st.warning("No dividend data available.")

st.divider() # ---------------------------------------------

# --- Historical Price Visualization ---
st.header("Historical Price")


import datetime
import plotly.express as px

price = yf.download(ticker)

st.line_chart(price['Close'])
# st.plotly_chart(
#     px.line(price['Close'].reset_index(), 
#             x='Date', 
#             y='AAPL', 
#             title='Line Graph with datetime64 Index'), 
#     use_container_width=True
#     )

# --- Glossary Section ---
st.markdown(r"""
### Glossary
**Growth Rate Calculation:**
- If the sign of value changes (from loss to profit or profit to loss), the growth rate is calculated as:
  
  $$(\text{Current} - \text{Previous}) / |\text{Previous}| \times 100$$
  
  This means a dramatic turnaround (e.g., from -10 to +30) will show as a large positive percentage (e.g., 400%). This approach ensures that turnarounds from loss to profit are reported as large positive growth, reflecting business reality rather than just mathematical sign.
""")
