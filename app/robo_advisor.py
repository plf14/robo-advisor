# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")
print("-------------------------")

Symbol = input("Symbol:  ")
APIkey = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

request_url = ("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Symbol + "&apikey=" + APIkey)
print("URL:", request_url)

response = requests.get(request_url)
parsed_response = json.loads(response.text)

if "Error Message" in response.text:
    print("OOPS couldn't find that symbol, please try again")
    exit()

print(parsed_response)

tsd = parsed_response["Time Series (Daily)"]
for date, prices in tsd.items():
    print(date)
    print(prices)
    print("-------------------------")

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
