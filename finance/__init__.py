# Expose main functions for cleaner imports
from .fundamentals import (
    annual_net_income, plot_annual_net_income, plot_net_income_growth,
    annual_dividends, plot_annual_dividends, plot_dividends_growth
)
from .edgar_client import (
    get_facts
)
from .prices import historical_price
