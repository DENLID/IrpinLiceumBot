from time import sleep
from telebot import TeleBot
from pytz import timezone
from datetime import datetime
import requests
import config

bot = TeleBot(config.air_alert_token, parse_mode="HTML")

def pull_air_alert():
    alertlater = False
    while True:
        ukraine_time = timezone('Europe/Kiev')
        dt = datetime.now(ukraine_time)
        r = requests.get("https://ubilling.net.ua/aerialalerts/")
        alertnow = r.json()["states"]["Київська область"]["alertnow"]

        if alertnow == True and alertlater == False:
            print(f"{dt.hour}:{dt.minute} Увага! Повітряна тривога 🔴")
            bot.send_message(config.channel_all_to, """
<b>Увага! Повітряна тривога</b> 🔴
Пройдіть всі в укриття, слідкуйте за вказівками вчителів!""")
            alertlater = True
        if alertnow == False and alertlater == True:
            print(f"{dt.hour}:{dt.minute} Відбій повітряної тривоги 🟢")
            bot.send_message(config.channel_all_to, """
<b>Відбій повітряної тривоги</b> 🟢""")
            alertlater = False
        sleep(3)
