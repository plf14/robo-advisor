# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import datetime
import plotly
import plotly.graph_objs as go
import csv

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
print("ENTER THE SYMBOL(S) OF YOUR STOCK(S) TO RECIEVE MY RECOMENDATION(S)")
print("ENTER 'DONE' WHEN FINISHED")
SymbolList = []
condition = True
while condition == True:
    Symbol = input("SYMBOL: ")
    if Symbol.lower() == 'done':
        condition = False
    else:
        SymbolList.append(Symbol)

for Symbol in SymbolList:

    if len(Symbol) > 5 or len(Symbol) < 1:
        print("-------------------------")
        print("EXPECTING A SYMBOL BETWEEN 1 AND 5 CHARACTERS, PLEASE TRY AGAIN")
        print("-------------------------")
        exit()

    for i in range(len(Symbol)):
        if Symbol[i].isnumeric():
            print("-------------------------")
            print("EXPECTING A SYMBOL CONTATINING ONLY LETTERS, PLEASE TRY AGAIN")
            print("-------------------------")
            exit()

    print("-------------------------")
    print("REQUESTING SOME DATA FROM THE INTERNET...")
    print("-------------------------")

    APIkey = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

    request_url = ("https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&outputsize=full&symbol=" + Symbol + "&apikey=" + APIkey)
    print("URL:", request_url)

    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    if "Error Message" in response.text:
        print("OOPS COULD NOT FIND THAT SYMBOL, PLEASE TRY AGAIN")
        exit()

    meta = parsed_response["Meta Data"]
    wsd = parsed_response["Weekly Time Series"]

    Dates = list(wsd.keys())
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    for Date in Dates:
        Open.append(wsd[Date]["1. open"])
        High.append(wsd[Date]["2. high"])
        Low.append(wsd[Date]["3. low"])
        Close.append(wsd[Date]["4. close"])
        Volume.append(wsd[Date]["5. volume"])

    FiftyTwoHigh = max(High[0:53])
    FiftyTwoLow = min(Low[0:53])
    Lastest = Close[0]

    #Write the logic for recomendation

    print("-------------------------")
    print("SELECTED SYMBOL: ", meta["2. Symbol"].upper())
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: ", date, time.strftime("%I:%M %p"))
    print("-------------------------")
    print("LATEST DAY: ", Dates[0])
    print("LATEST CLOSE: ", to_usd(eval(Close[0])))
    print("RECENT HIGH: ", to_usd(eval(High[0])))
    print("RECENT LOW: ", to_usd(eval(Low[0])))
    print("-------------------------")
    print("52-WEEK HIGH: ", to_usd(eval(FiftyTwoHigh)))
    print("52-WEEK LOW: ", to_usd(eval(FiftyTwoLow)))
    print("-------------------------")
    print("GENERATING LINE GRAPH...")
    plotly.offline.plot({
        "data": [go.Scatter(x=Dates, y=Close)],
        "layout": go.Layout(title= str(meta["2. Symbol"].upper()) + " WEEKLY CLOSE DATA")
    }, auto_open=True)
    print("-------------------------")
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: TODO")

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")