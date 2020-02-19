# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

date = datetime.date.today()
time = datetime.datetime.now()

print("-------------------------")
print("WELCOME TO THE ROBO STOCK ADVISOR")
print("ENTER THE SYMBOL OF YOUR STOCK TO RECIEVE MY RECOMENDATION")
Symbol = input("SYMBOL: ")
print("-------------------------")
print("REQUESTING SOME DATA FROM THE INTERNET...")
print("-------------------------")

APIkey = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

request_url = ("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Symbol + "&apikey=" + APIkey)
print("URL:", request_url)

response = requests.get(request_url)
parsed_response = json.loads(response.text)
tsd = parsed_response["Time Series (Daily)"]
Dates = list(tsd.keys())
Opens = []
Highs = []
Lows = []
Closes = []
Volumes = []
for Date in Dates:
    Opens.append(tsd[Date]["1. open"])
    Highs.append(tsd[Date]["2. high"])
    Lows.append(tsd[Date]["3. low"])
    Closes.append(tsd[Date]["4. close"])
    Volumes.append(tsd[Date]["5. volume"])

if "Error Message" in response.text:
    print("OOPS COULD NOT FIND THAT SYMBOL, PLEASE TRY AGAIN")
    exit()

#print(parsed_response)
#
#for date, prices in tsd.items():
#    print(date)

#    print(prices)
#    print("-------------------------")

print("-------------------------")
print("SELECTED SYMBOL: ", Symbol.upper())
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", date, time.strftime("%I:%M %p"))
print("-------------------------")
print("LATEST DAY: ", Dates[0])
print("LATEST CLOSE: ", to_usd(eval(Closes[0])))
print("RECENT HIGH: ", to_usd(eval(Highs[0])))
print("RECENT LOW: ", to_usd(eval(Lows[0])))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
