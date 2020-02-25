# Robo-Advisor Project

## Overview

This application pulls historical stock price data from the internet and issues a Buy/Sell Recomendation based on its top-secret algorithium.  Furthermore, it writes the historical data to a CSV File and creates a chart of the stock price throughout the past year.  Additionally, if there are large movements in the user's selected stock(s) within the past day, the program sends an SMS Alert about such movement.

## Setup

### Installation

Fork this repo, then clone your fork to download it locally onto your computer.  Then navigate there from the command line.

```sh
cd ~/Documents/OPIM-243/GitHub/robo-advisor
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```

### API Setup

First, you need to create a .env to exclude certain items from being uploaded to GitHub and potentially compromised.  The program already contains the proper .gitignore file to exclude what we are about to add to the .env file

#### AlphaVantage API

Your program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co).  Set an environment variable called `ALPHAVANTAGE_API_KEY`, and the program will read the API Key from this environment variable at run-time.

```
ALPHAVANTAGE_API_KEY="abc123"
```

#### Twilio Setup (SMS)

For SMS capabilities, [sign up for a Twilio account](https://www.twilio.com/try-twilio), click the link in a confirmation email to verify your account, then confirm a code sent to your phone to enable 2FA.

Then [create a new project](https://www.twilio.com/console/projects/create) with "Programmable SMS" capabilities. And from the console, view that project's Account SID and Auth Token. Update the contents of the ".env" file to specify these values as environment variables called `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`, respectively.

You'll also need to [obtain a Twilio phone number](https://www.twilio.com/console/sms/getting-started/build) to send the messages from. After doing so, update the contents of the ".env" file to specify this value (including the plus sign at the beginning) as an environment variable called `SENDER_SMS`.

Finally, set an environment variable called `RECIPIENT_SMS` to specify the recipient's phone number (including the plus sign at the beginning).

## Usage

Congratulations!  You are now ready to run the Robo Advisor Program!  Just enter the following into your command line

```sh
python robo_advisor.py
```