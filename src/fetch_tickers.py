import csv
import os, requests
# pandas as pd
import time
import requests

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
assert API_KEY, "Missing POLYGON_API_KEY env var"

LIMIT = 1000
url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"





response = requests.get(url)
tickers = []
# print(response)
data = response.json()

# # df = pd.DataFrame(data['results'])
# # print(df)
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    time.sleep(20)  # <-- fixed pause before each new request
    print("requesting next page")
    response = requests.get(data['next_url'] + f"&apiKey={API_KEY}")
    data = response.json()
    # print(data)
    for ticker in data['results']:
        tickers.append(ticker)

print(len(tickers))

example_ticker = {'ticker': 'SUSC',
                  'name': 'iShares Trust iShares ESG Aware USD Corporate Bond ETF', 
                  'market': 'stocks',
                  'locale': 'us',
                  'primary_exchange': 'XNAS',
                  'type': 'ETF',
                  'active': True,
                  'currency_name': 'usd',
                  'cik': '0001100663',
                  'composite_figi': 'BBG00H4BH2Q2',
            }

# write tickers to csv with exampl_ticker schema
fieldnames = list(example_ticker.keys())
output_csv = "tickers.csv"
with open(output_csv, mode='w', newline= '', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
       row = {key: t.get(key, '') for key in fieldnames}
       writer.writerow(row)
print(f"Wrote {len(tickers)} tickers to {output_csv}")