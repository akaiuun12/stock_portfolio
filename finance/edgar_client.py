import json
from sec_edgar_api import EdgarClient

# Initialize client once per session
edgar = EdgarClient(user_agent="Your Name your.email@example.com")

# Example CIK dictionary (extend or load from file)
with open("cik_dict.json", "r") as f:
    CIK = json.load(f)


def get_facts(ticker):
    return edgar.get_company_facts(cik=CIK[ticker.upper()])['facts']


# %%
