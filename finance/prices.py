import matplotlib.pyplot as plt
import yfinance as yf

def historical_price(ticker, start=None, end=None, column='Close', scale='linear', ax=None):
    # 주가 다운로드
    price = yf.download(ticker)
    data = price[column]

    # 기간 필터링
    if start is not None and end is not None:
        data = data.loc[start:end]
    elif start is not None:
        data = data.loc[start:]
    elif end is not None:
        data = data.loc[:end]

    # If no ax provided, create one
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    # Plot
    ax.plot(data, color='darkslategray')
    ax.set_title(f"{ticker} - {column} Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)

    if scale == 'log':
        ax.set_yscale('log')
        ax.set_title(f"{ticker} - {column} Price in Log Scale")

    # Only show the plot if used standalone
    if ax is None:
        plt.tight_layout()
        plt.show()

    return data
