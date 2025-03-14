# Telegram Bot
## Overview
This is a Python-based Telegram bot built using the Flask framework and the Telepot library. It provides functionalities such as weather updates, currency exchange rates, text translation, and more. The bot uses a webhook to receive and process messages from Telegram users.
## Features
- Weather Information: Fetches and displays real-time weather data.
- Currency Exchange Rates: Provides up-to-date currency exchange and gold prices.
- Text Translation: Translates user-inputted text into Persian.
- Date and Time Conversion: Shows both the Persian and Gregorian calendar dates.
- User Chat ID: Retrieves and displays the user's chat ID.
 ## Technologies Used
 - Python: Core programming language.
- Flask: Web framework to handle the webhook.
- Telepot: Telegram bot library.
- Requests: For making API calls.
- mtranslate: For language translation.
- Jalali Calendar (jdatetime): To provide Persian calendar dates.
## Installation
### Prerequisites
### Ensure you have the following installed:
```bash
**************************************************
pip install flask telepot requests mtranslate jdatetime urllib3
**************************************************
```
## Setup
1. Clone this repository or download the bot.py script.
2. Set up your Telegram bot and obtain a bot token.
3. Replace the mytoken import with your actual bot token.
4. Deploy the bot on a server (e.g., PythonAnywhere) and set up a webhook.
## Usage
1. Start the bot with /start.
2. Use the available commands or menu options:
- Weather Info: Enter a city name.
- Translation: Enter a text to translate.
- Currency Prices: Fetches latest exchange rates.
- Date & Time: Displays current dates in both calendars.
- Chat ID: Retrieves the user's chat ID.
## Deployment
To run the bot, use:
```bash
**************************************************
python bot.py
**************************************************
```
Ensure your server has the correct webhook URL configured to receive Telegram messages.
