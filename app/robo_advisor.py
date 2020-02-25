# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import datetime
import plotly
import plotly.graph_objs as go
import csv
from twilio.rest import Client

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

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, PLEASE SPECIFY ENV VAR CALLED 'TWILIO_ACCOUNT_SID'")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, PLEASE SPECIFY ENV VAR CALLED 'TWILIO_AUTH_TOKEN'")
SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, PLEASE SPECIFY ENV VAR CALLED 'SENDER_SMS'")
RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, PLEASE SPECIFY ENV VAR CALLED 'RECIPIENT_SMS'")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

print("-------------------------")
print("WELCOME TO THE ROBO STOCK ADVISOR")
print("ENTER THE SYMBOL(S) OF YOUR STOCK(S) TO RECIEVE MY RECOMENDATION(S)")
print("DISCLAIMER:  PREIUM ACCOUNT REQUIRED TO REQUEST MORE THAN 5 STOCKS")
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
        continue

    for i in range(len(Symbol)):
        if Symbol[i].isnumeric():
            print("-------------------------")
            print("EXPECTING A SYMBOL CONTATINING ONLY LETTERS, PLEASE TRY AGAIN")
            continue

    print("-------------------------")
    print("REQUESTING SOME DATA FROM THE INTERNET...")
    print("-------------------------")

    APIkey = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

    request_url = ("https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&outputsize=full&symbol=" + Symbol + "&apikey=" + APIkey)
    print("URL:", request_url)

    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    if "Error Message" in response.text:
        print("-------------------------")
        print("OOPS COULD NOT FIND THAT SYMBOL, PLEASE TRY AGAIN")
        continue

    if "higher API call frequency" in response.text:
        print("-------------------------")
        print("OOPS LOOKS LIKE YOU ENTERED TOO MANY STOCKS, PLEASE TRY AGAIN")
        exit()

    meta = parsed_response["Meta Data"]
    wsd = parsed_response["Weekly Time Series"]

    Dates = list(wsd.keys())
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    Headers = ['timestamp','open','high','low','close','volume']
    Rows = [Headers]

    for Date in Dates:
        Open.append(wsd[Date]["1. open"])
        High.append(wsd[Date]["2. high"])
        Low.append(wsd[Date]["3. low"])
        Close.append(wsd[Date]["4. close"])
        Volume.append(wsd[Date]["5. volume"])
        Row = []
        Row.append(Date)
        Row.append(wsd[Date]["1. open"])
        Row.append(wsd[Date]["2. high"])
        Row.append(wsd[Date]["3. low"])
        Row.append(wsd[Date]["4. close"])
        Row.append(wsd[Date]["5. volume"])
        Rows.append(Row)

    FileName = str("data/" + Symbol.upper() + ".csv")
    with open(FileName, 'w+') as csvfile:
        thewriter = csv.writer(csvfile)
        for Row in Rows:
            thewriter.writerow(Row)
        csvfile.close()

    SymbolCode = meta["2. Symbol"].upper()
    FiftyTwoHigh = max(High[0:53])
    FiftyTwoLow = min(Low[0:53])
    Latest = Close[0]
    PercentChange = (eval(Close[0]) - eval(Close[1]))/eval(Close[1]) * 100

    if eval(Latest) >= eval(FiftyTwoHigh) * .85:
        Recomendation = "BUY!"
        Reason = "THE STOCK HAS BEEN DOING WELL, IT'S TRADING CLOSE TO ITS 52-WEEK HIGH"
    else:
        Recomendation = "SELL!"
        Reason = "THE STOCK ISN'T DOING WELL. IT'S TRADING WELL BELOW ITS 52-WEEK HIGH"

    print("-------------------------")
    NextStock = input("PRESS ENTER TO SEE MY RECOMENDATION FOR " + SymbolCode)

    if PercentChange >= 5:
        content = f"SINCE YESTERDAY'S CLOSE, {SymbolCode} IS UP {str(round(float(PercentChange), 2))}%.  BUY QUICKLY!"
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
    elif PercentChange <= -5:
        PercentChange = PercentChange * -1
        content = f"SINCE YESTERDAY'S CLOSE, {SymbolCode} IS DOWN {str(round(float(PercentChange), 2))}%.  SELL QUICKLY!"
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)

    print("-------------------------")
    print("SELECTED SYMBOL: ", SymbolCode)
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
    print("RECOMMENDATION: ", Recomendation)
    print("RECOMMENDATION REASON: ", Reason)
    print("-------------------------")
    Graph = input("PRESS ENTER TO SEE A CHART OF " + SymbolCode + " OVER THE LAST 52-WEEKS")
    print("GENERATING STOCK PRICE CHART...")

    plotly.offline.plot({
        "data": [go.Scatter(x=Dates[0:53], y=Close[0:53])],
        "layout": go.Layout(title= str(meta["2. Symbol"].upper()) + " WEEKLY CLOSE DATA")
    }, auto_open=True)

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
