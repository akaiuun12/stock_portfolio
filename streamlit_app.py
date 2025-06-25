import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from finance import get_facts, annual_net_income, annual_dividends

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
        # Calculate Net Income Growth (%)
        df_growth = df_net_income.copy()
        df_growth["net_income_growth"] = df_growth["net_income"].pct_change() * 100

        # Calculate dynamic axis ranges with margin
        ni_min, ni_max = df_growth["net_income"].min(), df_growth["net_income"].max()
        ni_margin = (ni_max - ni_min) * 0.1 if ni_max > ni_min else ni_max * 0.1
        ni_range = [max(0, ni_min - ni_margin), ni_max + ni_margin]

        # Calculate dynamic axis ranges for Net Income Growth (%)
        ng_min, ng_max = df_growth["net_income_growth"].min(), df_growth["net_income_growth"].max()
        ng_margin = (ng_max - ng_min) * 0.1 if ng_max > ng_min else abs(ng_max) * 0.1
        ng_range = [ng_min - ng_margin, ng_max + ng_margin]

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
            y=df_growth["net_income_growth"],
            name="Net Income Growth (%)",
            mode='lines+markers',
            marker_color='orange',
            yaxis='y2'
        ))
        # Custom axis mapping: 0 net income = -20%, 20B = 0%, 40B = 20%
        fig_income.update_layout(
            title="Net Income and Net Income Growth (%)",
            xaxis=dict(title="Year"),
            yaxis=dict(
                title="Net Income",
                range=ni_range,
                showgrid=True,
                gridcolor='lightgray',
            ),
            yaxis2=dict(
                title="Net Income Growth (%)",
                overlaying='y',
                side='right',
                range=ng_range,
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
            y=df_dividends["dividend_growth"],
            name="Dividend Growth (%)",
            mode='lines+markers',
            marker_color='purple',
            yaxis='y2'
        ))
        fig_div.update_layout(
            title="Dividends and Dividend Growth (%)",
            xaxis=dict(title="Year"),
            yaxis=dict(
                title="Dividends",
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

    # --- P/E Ratio Calculation and Display ---
    st.header("P/E Ratio")
    price = yf.download(ticker)
    shares = yf.Ticker(ticker).info.get('sharesOutstanding')
    if shares and not df_net_income.empty:
        # Calculate market capitalization and P/E ratio
        market_cap = price['Close'] * shares
        pe = market_cap.iloc[-1] / df_net_income.net_income.iloc[-1]
        st.write(f"Latest P/E Ratio for {ticker}: {pe:.2f}")
    else:
        st.info("P/E ratio unavailable.")
