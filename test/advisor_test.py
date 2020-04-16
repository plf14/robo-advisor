import os
import pytest
import datetime

from app.robo_advisor import to_usd, human_friendly_timestamp, compile_url, transform_response, create_lists

CI_ENV = os.environ.get("CI") == "true"
@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")

def test_to_usd():
    # it should apply USD formatting
    assert to_usd(4.50) == "$4.50"

    # it should display two decimal places
    assert to_usd(4.5) == "$4.50"

    # it should round to two places
    assert to_usd(4.55555) == "$4.56"

    # it should display thousands separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"

def test_human_friendly_timestamp():
    time = datetime.datetime(1776,7,4,11,36,42)
    time2 = datetime.datetime(1776,7,4,14,32,17)
    result = human_friendly_timestamp(time)
    result2 = human_friendly_timestamp(time2)
    # it should display a properly formatted time
    assert result == "11:36 AM"
    # it should properly display AM/PM
    assert result2 == "02:32 PM"

def test_url():
    result = compile_url('Symbol', 'APIkey')
    assert "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&outputsize=full&symbol=" in result

def test_transform_response():
    wsd = {
        "2020-04-15": {
            "1. open": "164.3500",
            "2. high": "173.7500",
            "3. low": "162.3000",
            "4. close": "171.8800",
            "5. volume": "135368325"
        },
        "2020-04-09": {
            "1. open": "160.3200",
            "2. high": "170.0000",
            "3. low": "157.5800",
            "4. close": "165.1400",
            "5. volume": "229630744"
        },
        "2020-04-03": {
            "1. open": "152.4400",
            "2. high": "164.7800",
            "3. low": "150.0100",
            "4. close": "153.8300",
            "5. volume": "290191457"
        }
    }

    transformed_response = [
        ["timestamp","open","high","low","close","volume"],
        ["2020-04-15","164.3500","173.7500","162.3000","171.8800","135368325"],
        ["2020-04-09","160.3200","170.0000","157.5800","165.1400","229630744"],
        ["2020-04-03","152.4400","164.7800","150.0100","153.8300","290191457"]
    ]

    Dates = list(wsd.keys())
    Headers = ['timestamp','open','high','low','close','volume']
    Rows = [Headers]

    assert transform_response(wsd, Dates, Rows) == transformed_response

def test_create_lists():
    wsd = {
        "2020-04-15": {
            "1. open": "164.3500",
            "2. high": "173.7500",
            "3. low": "162.3000",
            "4. close": "171.8800",
            "5. volume": "135368325"
        },
        "2020-04-09": {
            "1. open": "160.3200",
            "2. high": "170.0000",
            "3. low": "157.5800",
            "4. close": "165.1400",
            "5. volume": "229630744"
        },
        "2020-04-03": {
            "1. open": "152.4400",
            "2. high": "164.7800",
            "3. low": "150.0100",
            "4. close": "153.8300",
            "5. volume": "290191457"
        }
    }

    list_response = ["171.8800","165.1400","153.8300"]

    Dates = list(wsd.keys())
    Close = []

    assert create_lists(wsd, Dates, Close, "4. close") == list_response