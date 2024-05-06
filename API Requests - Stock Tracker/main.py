"""
Users may set a stock to track and the company name.

After they do the user sets environment varibles with
the relevent API keys to get the stocks closing value and
the 3 most recent news articles.

Then formats and sends a message via a Telegram bot to the
users Telegram conversation with said bot.
"""
import os
import datetime as dt
import requests as rq

# Stock name and symbol
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Alpha Advantage API
AA_API_KEY = os.environ.get("AA_API_KEY")
AA_ENDPOINT = "https://www.alphavantage.co/query"
DATAPONT_KEY = "4. close"

# NewsAPI API
NAPI_API_KEY = os.environ.get("NAPI_API_KEY")
NAPI_ENDPOINT = "https://newsapi.org/v2/everything"

# Time vars
TODAY = dt.datetime.now()
YESTERDAY = TODAY - dt.timedelta(days=1)
TWO_DAY_AGO = YESTERDAY - dt.timedelta(days=1)

# Telegram bot
BOT_TOKEN = os.environ.get("BOT_API_TOKEN")
BOT_CHAT_ID = os.environ.get("BOT_CHAT_ID")
TELEGRAM_ENDPOINT = "https://api.telegram.org/bot"


def run():
    """
    Starts the stock check.
    """
    stock_data = check_stocks()
    if stock_data[0]:
        news_data = get_news()
        msg = format_alert(news_data, stock_data[1], stock_data[2])
        send_alert(msg)

def check_stocks():
    """
    Gets stock data from an API and selects data from yesterday
    and the day before yesterday to make a comparison againist.

    First value returned is to indicate if the change percent
    is enough to trigger an alert.
    """
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "datatype": "json",
        "apikey": AA_API_KEY,
    }
    response = rq.get(url=AA_ENDPOINT, params=parameters, timeout=30)
    response.raise_for_status()
    data = response.json()
    if check_limit(data):
        yday_str = YESTERDAY.date().isoformat()
        twoago_str = TWO_DAY_AGO.date().isoformat()
        stock_datasets = data["Time Series (Daily)"]
        yday_dataset = stock_datasets[yday_str]
        twoago_dataset = stock_datasets[twoago_str]
        yday_value = float(yday_dataset[DATAPONT_KEY])
        twoago_value = float(twoago_dataset[DATAPONT_KEY])
        change_value = yday_value - twoago_value
        change_percent = (change_value / twoago_value) * 100

        if change_percent >= 5 or change_percent <= -5:
            return (True, change_value, change_percent)
        return (False, change_value, change_percent)
    return (False, None, None)


# USED FOR DEBUGGING
def check_limit(data):
    """
    Checks to see if the API call
    returns with the 'daily limit reached'
    text and stops the code if it did.
    """
    info = data.get("Information")
    if info is None:
        return True
    return False

def get_news():
    """
    Gets the 3 most recent news articles
    and returns them.
    """
    parameters = {
        "q": COMPANY_NAME,
        "sortBy": "popularity",
        "apiKey": NAPI_API_KEY,
    }
    response = rq.get(url=NAPI_ENDPOINT, params=parameters, timeout=30)
    response.raise_for_status()
    data = response.json()
    news_data = data["articles"][:3]
    return news_data

def formet_news_articles(article_set):
    """
    Formats passed article set
    into a formatted set to be
    put into the message later on.
    """
    f_article_set = []
    for article in article_set:
        headline = article["title"]
        breif = article["description"]
        if "\n" in breif:
            breif = breif.split("\n", 1)[0]
        f_article = {"headline": headline, "breif": breif}
        f_article_set.append(f_article)
    return f_article_set


def get_emoji(change_percent):
    """
    Takes the change percentage and
    returns an 'up' or 'down' emoji
    depending on if it is negative or
    positive.
    """
    up = "🔺"
    down = "🔻"
    if change_percent > 0:
        return up
    return down


def format_alert(article_set, change_value, change_percent):
    """
    Takes the formated new articles, emoji
    and the values passed to it and creates
    a message to send to the users Telegram
    bot.
    """
    formatted_articles = formet_news_articles(article_set)
    emoji = get_emoji(change_percent)
    f_percent = abs(round(change_percent))
    f_value = abs(change_value)
    stock_title = f"{STOCK}: {emoji}{f_percent}% | USD ${f_value:.2f}"
    msg = stock_title
    for article in formatted_articles:
        headline = article["headline"]
        breif = article["breif"]
        msg += f"\n\nHeadline:  {headline}\nBreif: {breif}"
    return msg


def send_alert(bot_msg):
    """
    Uses the set constants to send a telegram
    message to alert the user of the stocks
    price change and the 3 most recent
    news articles about the company.
    """
    bot_endpoint = TELEGRAM_ENDPOINT + BOT_TOKEN + "/sendMessage"
    parameters = {
        "chat_id": BOT_CHAT_ID,
        "parse_mode": "Markdown",
        "text": bot_msg,
    }

    response = rq.get(url=bot_endpoint, params=parameters, timeout=30)
    response.raise_for_status()
    return response.json()

# Runs the starting function.
run()
