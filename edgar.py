
# %% Stock Analysis with EDGAR Crawling 
# %% Import the Libraries
from sec_edgar_api import EdgarClient
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)
plt.style.use('ggplot')


# %% Get EdgarClient
from sec_edgar_api import EdgarClient
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")


# %% Load the Data
CIK = {
    "AAPL": "0000320193",
    "ADBE": "0000796343",
    "AMD": "0000002488",
    "AMZN": "0001018724",
    "BRK-B": "0001067983",
    "CPNG": "0001834584",
    "FB": "0001326801",
    "GOOG": "0001652044",
    "GOOGL": "0001652044",
    "INTC": "0000050863",
    "KO": "0000021344",
    "LOGI": "0001032975",
    "MA": "0001141391",
    "MSFT": "0000789019",
    "MMM": "0000066740",
    "NFLX": "0001065280",
    "NVDA": "0001045810",
    "PEP": "0000077476",
    "SBUX": "0000829224",
    "TSLA": "0001318605",
    "V": "0001403161"
}


# %% Annual Net Income(Loss)
def annual_net_income(facts):
    if 'NetIncomeLossAvailableToCommonStockholdersBasic' in facts['us-gaap'].keys():
        ni_var = 'NetIncomeLossAvailableToCommonStockholdersBasic'
    elif 'NetIncomeLoss' in facts['us-gaap'].keys():
        ni_var = 'NetIncomeLoss'
    else:
        return False

    title = facts['us-gaap'][ni_var]['label']
    description = facts['us-gaap'][ni_var]['description']

    date = []
    net_income = []

    for report in facts['us-gaap'][ni_var]['units']['USD']:
        try:
            frame = report['frame']

            if len(frame) == 6:
                date.append(report['end'])
                net_income.append(report['val'])
        except:
            pass

    df_net_income = pd.DataFrame({'date': date, 'net_income': net_income})

    return df_net_income, title, description


def plot_annual_net_income(df_net_income, title, description, ymin, ymax, ystep):
    fig, axes = plt.subplots(1, 1, figsize=(12, 6))

    df_net_income.plot(kind='bar', x='date', y='net_income', ax=axes, color='blue', alpha=0.5)

    plt.title(f'{ticker}\n{title}', fontsize=14)
    plt.xticks(ticks=df_net_income.index, labels=df_net_income.date.str[:4], rotation=0)
    plt.yticks(ticks=np.arange(ymin, ymax * 1e6, ystep * 1e6), labels=[str(x) for x in np.arange(ymin, ymax, ystep)])
    plt.ylabel('USD in milllions')
    plt.tight_layout()


def plot_net_income_growth(df_net_income, title, description, ymin, ymax, ystep):
    fig, axes = plt.subplots(1, 1, figsize=(12, 6))

    sns.barplot(data=df_net_income, x='date', y='net_income_growth', color='blue', alpha=0.5, ax=axes)

    plt.title(f'{ticker}\n{title}\n{description}', fontsize=12)

    plt.ylabel('Income Growth(%)')
    plt.yticks(ticks=np.arange(ymin, ymax, ystep), labels=[str(x) for x in np.arange(ymin, ymax, ystep)])
    plt.ylim((ymin,ymax))

    plt.tight_layout()


# %% Dividends
def annual_dividends(facts):

    if 'PaymentsOfDividends' in facts['us-gaap'].keys():
        div_var = 'PaymentsOfDividends'
    elif 'PaymentsOfDividendsCommonStock' in facts['us-gaap'].keys():
        div_var = 'PaymentsOfDividendsCommonStock'
    elif 'PaymentsOfDividendsPreferredStock' in facts['us-gaap'].keys():
        div_var = 'PaymentsOfDividendsPreferredStock'
    else:
        return False

    if div_var:
        title = facts['us-gaap'][div_var]['label']
        description = facts['us-gaap'][div_var]['description']

        date = []
        dividends = []

        for report in facts['us-gaap'][div_var]['units']['USD']:
            try:
                frame = report['frame']

                if len(frame) == 6:
                    date.append(report['end'])
                    dividends.append(report['val'])
            except:
                pass

        df_dividends = pd.DataFrame({'date': date, 'dividends': dividends})

        return df_dividends, title, description


def plot_annual_dividends(df_dividends, title, description, ymin, ymax, ystep):
    fig, axes = plt.subplots(1, 1, figsize=(12, 6))

    df_dividends.plot(kind='bar', x='date', y='dividends', ax=axes, color='blue', alpha=0.5)
    plt.title(ticker.upper() + '\n' + title, fontsize=12)
    plt.xticks(ticks=df_dividends.index, labels=df_dividends.date.str[:4], rotation=0)
    plt.yticks(ticks=np.arange(ymin, ymax * 1e6, ystep * 1e6), labels=[str(x) for x in np.arange(ymin, ymax, ystep)])
    plt.ylabel('USD($)')
    plt.tight_layout()


def plot_dividends_growth(df_dividends, title, description, ymin, ymax, ystep):
    fig, axes = plt.subplots(1, 1, figsize=(12, 6))

    sns.barplot(data=df_dividends, x='date', y='dividends_growth', color='blue', alpha=0.5, ax=axes)

    plt.title(f'{ticker}\n{title}\n{description}', fontsize=12)
    plt.ylabel('Income Growth(%)')
    plt.yticks(ticks=np.arange(ymin, ymax, ystep), labels=[str(x) for x in np.arange(ymin, ymax, ystep)])
    plt.ylim((ymin,ymax))

    plt.tight_layout()


# %% AMZN
ticker = 'NVDA'
facts = edgar.get_company_facts(cik=CIK[ticker.upper()])['facts']

# %% AMZN: Annual Net Income 
df_net_income, title, description = annual_net_income(facts)
plot_annual_net_income(df_net_income, title, description, 0, 120000, 10000)

# %% AMZN: Dividends
try:
    df_dividends, title, description = annual_dividends(facts)
    plot_annual_dividends(df_dividends, title, description, 0, 20000, 5000)
except TypeError:
    print('Dividends history does not exists')

# %%
df_net_income
# %%
