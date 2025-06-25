import numpy as np
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from finance import get_facts, annual_net_income, annual_dividends
import pandas as pd

# --- App Title ---
st.title("Stock Portfolio Tracker")

# --- Ticker Input (Main Area) ---
ticker = st.text_input("Ticker", value="AAPL")

if ticker:
    # --- Retrieve Financial Data ---
    facts = get_facts(ticker)
    df_net_income, _, _ = annual_net_income(facts)
    df_dividends, _, _ = annual_dividends(facts)

    # --- Net Income and Net Income Growth Visualization ---
    st.header("Net Income")

    if not df_net_income.empty:
        # Calculate Net Income Growth (%) with business logic reflecting magnitude
        df_growth = df_net_income.copy()
        df_growth['net_income_prev'] = df_growth['net_income'].shift(1)
        def business_growth_rate(row):
            current = row['net_income']
            previous = row['net_income_prev']
            if pd.isna(previous) or previous == 0:
                return np.nan
            # If sign changes, use abs(previous) for denominator
            if (previous < 0 and current > 0) or (previous > 0 and current < 0):
                return (current - previous) / abs(previous) * 100
            else:
                return (current - previous) / previous * 100
        df_growth['net_income_growth'] = df_growth.apply(business_growth_rate, axis=1)

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
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("No net income data available.")


    # --- Dividends and Dividend Growth Visualization ---
    st.header("Dividends")

    if not df_dividends.empty:
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
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_div, use_container_width=True)
    else:
        st.info("No dividend data available.")

# --- Glossary Section ---
st.markdown(r"""
---
### Glossary
**Net Income Growth Rate Calculation:**
- If the sign of value changes (from loss to profit or profit to loss), the growth rate is calculated as:
  
  $$(\text{Current} - \text{Previous}) / |\text{Previous}| \times 100$$
  
  This means a dramatic turnaround (e.g., from -10 to +30) will show as a large positive percentage (e.g., 400%).

This approach ensures that turnarounds from loss to profit are reported as large positive growth, reflecting business reality rather than just mathematical sign.
""")
