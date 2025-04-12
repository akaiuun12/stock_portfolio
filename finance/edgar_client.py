from sec_edgar_api import EdgarClient

# Initialize client once per session
edgar = EdgarClient(user_agent="Your Name your.email@example.com")

# Example CIK dictionary (extend or load from file)
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

def get_facts(ticker):
    return edgar.get_company_facts(cik=CIK[ticker.upper()])['facts']
