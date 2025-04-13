# 0. Get Packages and EdgarClient
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 0. Helper Function
def get_unit_formatting(unit, max_val):
    units = {
        'B': (1e9, 'USD (Billions)', lambda x: f'{x/1e9:.1f}B'),
        'M': (1e6, 'USD (Millions)', lambda x: f'{x/1e6:.0f}M'),
        'raw': (1, 'USD ($)', lambda x: str(int(x))),
    }

    if unit == 'auto':
        if max_val >= 1e9:
            unit = 'B'
        elif max_val >= 1e6:
            unit = 'M'
        else:
            unit = 'raw'

    if unit not in units:
        raise ValueError("unit must be one of: 'auto', 'M', 'B', or 'raw'")

    return units[unit]  # returns (scale, ylabel, label_format)

# 1. Annual Net Income
def annual_net_income(facts): 
    if 'NetIncomeLoss' in facts['us-gaap']:
        ni_var = 'NetIncomeLoss'
    elif 'NetIncomeLossAvailableToCommonStockholdersBasic' in facts['us-gaap']:
        ni_var = 'NetIncomeLossAvailableToCommonStockholdersBasic'
    else:
        return pd.DataFrame(), None, None

    date = []
    net_income = []

    for report in facts['us-gaap'][ni_var]['units']['USD']:
        try:
            if len(report['frame']) == 6:
                date.append(report['end'])
                net_income.append(report['val'])
        except:
            continue

    df_net_income = pd.DataFrame({'date': date, 'net_income': net_income})
    df_net_income['date'] = pd.to_datetime(df_net_income['date'])
    df_net_income['year'] = df_net_income['date'].dt.year

    return df_net_income.sort_values('year'), facts['us-gaap'][ni_var].get('label', ''), facts['us-gaap'][ni_var].get('description', '')


# 2. Plot Annual Net Income
def plot_annual_net_income(df_net_income, 
                           ticker='TICKER', 
                           title='Annual Net Income', description='', 
                           ymin=None, ymax=None, ystep=None, 
                           color='darkslategray',
                           unit='auto',
                           ax=None):
    df = df_net_income.copy()
    if 'year' not in df:
        df['year'] = pd.to_datetime(df['date']).dt.year
    max_val = df['net_income'].max()

    scale, ylabel, label_format = get_unit_formatting(unit, max_val)
    if ymin is None: ymin = 0
    if ymax is None: ymax = max_val * 1.2
    if ystep is None: ystep = (ymax - ymin) / 5
    yticks = np.arange(ymin, ymax, ystep)

    # Axes setup
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(df['year'].astype(str), df['net_income'], color=color)
    ax.set_title(f'{ticker}\n{title}')
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    ax.set_yticks(yticks)
    ax.set_yticklabels([label_format(x) for x in yticks])
    ax.grid(axis='y', linestyle='--', alpha=0.7)


# 3. Plot Net Income Growth (%) 
# BUGS-TO-SOLVE: yticks doesn't work as expected
def plot_net_income_growth(df_net_income, 
                           ticker='TICKER', 
                           title='Net Income Growth', 
                           description='', 
                           ymin=None, ymax=None, ystep=25, 
                           color='darkslategray',
                           ax=None):
    df = df_net_income.copy()
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['net_income_growth'] = df['net_income'].pct_change() * 100

    # Determine y-axis limits if not provided
    min_val = df['net_income_growth'].min()
    max_val = df['net_income_growth'].max()
    abs_max = max(abs(min_val), abs(max_val))

    if ymin is None and ymax is None:
        ymax = np.ceil(abs_max / ystep) * ystep
        ymin = -ymax
    elif ymin is None:
        ymin = -ymax
    elif ymax is None:
        ymax = -ymin

    yticks = np.arange(ymin, ymax + ystep, ystep)

    # Axes handling
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(data=df, x='year', y='net_income_growth', color=color, ax=ax)
    ax.set_title(f'{ticker}\n{title}\n{description}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Income Growth (%)')
    ax.set_yticks(yticks)
    ax.set_ylim((ymin, ymax))
    ax.grid(axis='y', linestyle='--', alpha=0.7)


# 4. Annual Dividends
def annual_dividends(facts):
    div_keys = [
        'PaymentsOfDividends',
        'PaymentsOfDividendsCommonStock',
        'PaymentsOfDividendsPreferredStock'
    ]
    div_var = next((key for key in div_keys if key in facts.get('us-gaap', {})), None)
    if not div_var:
        return pd.DataFrame(), None, None

    date, dividends = [], []
    for report in facts['us-gaap'][div_var]['units'].get('USD', []):
        try:
            if len(report['frame']) == 6:
                date.append(report['end'])
                dividends.append(report['val'])
        except:
            continue

    df_dividends = pd.DataFrame({'date': date, 'dividends': dividends})
    df_dividends['date'] = pd.to_datetime(df_dividends['date'])
    df_dividends['year'] = df_dividends['date'].dt.year

    return df_dividends.sort_values('year'), facts['us-gaap'][div_var].get('label', ''), facts['us-gaap'][div_var].get('description', '')


# 5. Plot Annual Dividends
def plot_annual_dividends(df_dividends, ticker='TICKER', title='Annual Dividends',
                          unit='auto', color='darkslategray', ax=None):
    if df_dividends is None or df_dividends.empty:
        print(f"[{ticker}] No dividend data available. Skipping annual dividend plot.")
        return

    df = df_dividends.copy()
    df['year_str'] = df['year'].astype(str)

    scale, ylabel, label_format = get_unit_formatting(unit, df['dividends'].max())
    df['dividends_scaled'] = df['dividends'] / scale

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(df['year_str'], df['dividends_scaled'], color=color)
    ax.set_title(f'{ticker}\n{title}')
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', linestyle='--', alpha=0.7)


# 6. Plot Dividends Growth
def plot_dividends_growth(df_dividends, ticker='TICKER', title='Dividends Growth',
                          ymin=None, ymax=None, ystep=10, color='darkslategray', ax=None):
    if df_dividends is None or df_dividends.empty:
        print(f"[{ticker}] No dividend data available. Skipping dividends growth plot.")
        return

    df = df_dividends.copy()
    df['year_str'] = df['year'].astype(str)
    df['dividends_growth'] = df['dividends'].pct_change() * 100
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['dividends_growth'])

    min_val = df['dividends_growth'].min()
    max_val = df['dividends_growth'].max()
    abs_max = max(abs(min_val), abs(max_val))

    if ymin is None and ymax is None:
        ymax = np.ceil(abs_max / ystep) * ystep
        ymin = -ymax
    elif ymin is None:
        ymin = -ymax
    elif ymax is None:
        ymax = -ymin

    yticks = np.arange(ymin, ymax + ystep, ystep)

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(df['year_str'], df['dividends_growth'], color=color)
    ax.set_title(f'{ticker}\n{title}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Growth (%)')
    ax.set_yticks(yticks)
    ax.set_ylim((ymin, ymax))
    ax.grid(axis='y', linestyle='--', alpha=0.7)