import requests
from twilio.rest import Client


# ---------------------------------- CONSTANTS ---------------------------------- #

# Enter Your Twilio Account Credentials || Sign up https://www.twilio.com/try-twilio
account_sid = ""
auth_token = ""
TWILIO_NUMBER = ""
RECEIVER_NUMBER = ""

# Alphavantage
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = ""  # Get your Alphavantage API Key here https://www.alphavantage.co/support/#api-key
STOCK = ""  # example: TSLA
COMPANY_NAME = ""  # example: Tesla Inc

# News API
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = ""  # Get your News API key here https://newsapi.org/register

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
    "language": "en",
}


# ---------------------------------- SEND MESSAGE ---------------------------------- #


def send_msg():
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=get_news(stock_percent),
                                     from_=TWILIO_NUMBER,
                                     to=RECEIVER_NUMBER
                                     )
    print(message.status)

# ---------------------------------- GET NEWS ---------------------------------- #


def get_news(percentage):
    response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    response.raise_for_status()
    data = response.json()["articles"]
    three_articles = data[:3]
    if percentage < 0:
        stock_percentage = f"🔻 {abs(percentage)}"
    else:
        stock_percentage = f"🔺 {abs(percentage)}"
    three_articles = [f"{STOCK}: {stock_percentage}%\n Headline: {article['title']}\nBrief: {article['description']}\n\n"
                      for article in three_articles]
    return "".join(three_articles)

# ---------------------------------- GET STOCK PRICE ---------------------------------- #


def stock_price():
    response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
    response.raise_for_status()

    data = response.json()["Time Series (Daily)"]
    yesterday = list(data.keys())[0]
    day_before_yesterday = list(data.keys())[1]

    yesterday_close = float(data[yesterday]["4. close"])
    day_before_yesterday_close = float(data[day_before_yesterday]["4. close"])

    difference = day_before_yesterday_close - yesterday_close
    return round((difference / day_before_yesterday_close) * 100, 2)


stock_percent = stock_price()
if abs(stock_percent) >= 5:
    send_msg()
