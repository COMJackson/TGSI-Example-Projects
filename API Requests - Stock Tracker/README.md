# Stock Tracker
### Purpose: 
The purpose of this script is to track a stock and send out an 
alert if the stock has increased or decreased by 5% with news
that is relevent to the stocks company.

### How to run.
1. Install Python and Requests module if not already done.
2. Add the required API keys and Telegram Chat ID to your environment variables listed below.
    - Alternatively, if you are using VSCode you can run a JSON file with the environment variables set in the file.
    - Learn more about this method [here](https://stackoverflow.com/questions/29971572/how-do-i-add-environment-variables-to-launch-json-in-vscode).
3. Open main.py.
4. Run main.py.
5. If the tracked stock has increased or decreased by 5%, then the bot will send a Telegram message to the chat.

### API Keys and Telegram Chat ID
In order to use this script you will need to setup these free API keys as environment variables:
- *AA_API_KEY* - https://www.alphavantage.co/
- *NAPI_API_KEY* - https://newsapi.org/
- **Telegram**
    - *BOT_API_TOKEN* - https://core.telegram.org/bots/tutorial
    - In order to use your bot you will need to get the Telegram chat ID
    - *BOT_CHAT_ID* - https://medium.com/@2mau/how-to-get-a-chat-id-in-telegram-1861a33ca1de

### Requeried Python Version and Modules
- Python 3.11.4 
> Earlier versions may work
- Requests 2.31.0
> Earlier versions may work
