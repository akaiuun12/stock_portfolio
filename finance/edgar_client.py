import json
import os
from sec_edgar_api import EdgarClient

# Initialize client once per session with configurable user agent
user_agent = os.getenv('SEC_EDGAR_USER_AGENT', 'Stock Portfolio App your.email@example.com')
edgar = EdgarClient(user_agent=user_agent)

# Example CIK dictionary (extend or load from file)
with open("cik_dict.json", "r") as f:
    CIK = json.load(f)

def get_facts(ticker):
    if CIK.get(ticker.upper()) is None:
        return
    else:
        return edgar.get_company_facts(cik=CIK[ticker.upper()])