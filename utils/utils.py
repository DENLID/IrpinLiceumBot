from update_info.update_info import alphabet_ukr
from email.mime.text import MIMEText
from pymongo import MongoClient
import smtplib, sys, telebot

import config

all_class = [f"{n}-{l}" for n in range(11) for l in alphabet_ukr]


def read_wordlist():
    with open(config.path_wordlist, "r", encoding="utf-8") as wordlist:
        return [line.strip() for line in wordlist.readlines()]


def send_email(receiver, text):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    sender = config.email_sender
    password = config.email_password

    try:
        server.login(sender, password)
        msg = MIMEText(text)
        msg["Subject"] = "Ірпінський ліцей №2 | BOT"
        server.sendmail(sender, receiver, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


class ConsoleRedirector:
    def __init__(self):
        self.bot = telebot.TeleBot("8032219145:AAF11hJJP3In0kU8Vk8ZI8UmayvLBgfDy8g")
        self.db = MongoClient(config.mongo_api).ILdb
        self.console = sys.stdout

    def write(self, message):
        if message.strip() != "":
            for user in list(self.db.users.find({"tags": "logging"})):
                self.bot.send_message(user["_id"], message)
        self.console.write(message)
        self.console.flush()

    def flush(self):
        pass  # Для совместимости с интерфейсом sys.stdout
