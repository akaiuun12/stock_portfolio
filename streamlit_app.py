import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
from finance import (
    get_facts,
    annual_net_income, plot_annual_net_income, plot_net_income_growth,
    annual_dividends, plot_annual_dividends, plot_dividends_growth,
    historical_price
)

st.title("Stock Portfolio Tracker")

ticker = st.sidebar.text_input("Ticker", value="AAPL")

if ticker:
    facts = get_facts(ticker)
    df_net_income, _, _ = annual_net_income(facts)

    st.header("Net Income")
    fig1, ax1 = plt.subplots()
    plot_annual_net_income(df_net_income, ticker=ticker, ax=ax1)
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    plot_net_income_growth(df_net_income, ticker=ticker, ax=ax2)
    st.pyplot(fig2)

    df_dividends, _, _ = annual_dividends(facts)
    if not df_dividends.empty:
        st.header("Dividends")
        fig3, ax3 = plt.subplots()
        plot_annual_dividends(df_dividends, ticker=ticker, ax=ax3)
        st.pyplot(fig3)

        fig4, ax4 = plt.subplots()
        plot_dividends_growth(df_dividends, ticker=ticker, ax=ax4)
        st.pyplot(fig4)
    else:
        st.info("No dividend data available.")

    st.header("Historical Price")
    fig5, ax5 = plt.subplots()
    historical_price(ticker, ax=ax5)
    st.pyplot(fig5)

    fig6, ax6 = plt.subplots()
    historical_price(ticker, scale='log', ax=ax6)
    st.pyplot(fig6)

    st.header("P/E Ratio")
    price = yf.download(ticker)
    shares = yf.Ticker(ticker).info.get('sharesOutstanding')
    if shares and not df_net_income.empty:
        market_cap = price['Close'] * shares
        pe = market_cap.iloc[-1] / df_net_income.net_income.iloc[-1]
        st.write(f"Latest P/E Ratio for {ticker}: {pe:.2f}")
    else:
        st.info("P/E ratio unavailable.")
