# 📈 Personal Stock Portfolio Tracker

![Portfolio Tracker](images/image.png)

Welcome to the Personal Stock Portfolio Tracker — a data-driven project built with **Python** and **Jupyter Notebook** to monitor and analyze individual stocks in your investment portfolio.

This project fetches data from SEC EDGAR (using `sec-edgar-api`) and tracks net income history over decades, providing tools for historical financial data, visualizing key metrics, and tracking performance over time.

---

## 🔧 Features

- Historical Net Income and Growth Rate (%)
- Dividends History

---

## 📂 Repository Structure

```
stock_portfolio/
│
├── README.md
├── requirements.txt
│
├── finance/
│   ├── __init__.py
│   ├── edgar_client.py     # SEC EDGAR data
│   ├── fundamentals.py     # Net income, dividends
│   └── prices.py           # Historical price data
│
├── analysis/
│   ├── AAPL_2025.ipynb
│   ├── ...
│   └── V_2025.ipynb
│
└── streamlit_app.py        # Main Streamlit app
```

---

## 🚀 Running the App Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open the provided local URL in your browser to interact with the app.

---

## ☁️ Deploying to Streamlit Cloud

> **Note:** Streamlit Community Cloud only supports public GitHub repositories.  
> If your repository is private, you must either make it public or upgrade to a paid plan for private repo support.

1. Push your code to a **public** GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click **New app**, select your repo and branch, and set `streamlit_app.py` as the app file.
4. Click **Deploy**.

For more details, see the [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app).

---

## 🔑 Secrets & API Keys

If your app requires API keys or credentials, use Streamlit's [Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management).

---

## 📊 Custom Analysis

To analyze a different stock, copy a notebook from the `analysis/` folder and change the ticker symbol.
