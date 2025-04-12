import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def historical_price(ticker, start=None, end=None, column='Close', scale='linear'):
    # 주가 다운로드
    price = yf.download(ticker)

    # column로 해당 열 선택
    data = price[column]

    # 기간 필터링
    if start is not None and end is not None:
        data = data.loc[start:end]
    elif start is not None:
        data = data.loc[start:]
    elif end is not None:
        data = data.loc[:end]
    
    # 그래프 출력
    plt.figure(figsize=(10, 4))
    plt.plot(data, color='darkslategray')
    plt.title(f"{ticker} - {column} Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    # 로그 스케일 적용
    if scale == 'log':
        plt.yscale('log')

    plt.show()

    return data