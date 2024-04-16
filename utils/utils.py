from update_info.update_info import alphabet_ukr
from email.mime.text import MIMEText
import smtplib

import config

all_class = [f"{n}-{l}" for n in range(11) for l in alphabet_ukr]

def get_user_class(user):
    user_class = next((c for c in all_class if c in user["tags"]), None)
    return user_class


def send_email(receiver, text):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    sender = config.email_sender
    password = config.email_password

    try:
        server.login(sender, password)
        msg = MIMEText(text)
        msg["Subject"] = "CLICK ME PLEASE!"
        server.sendmail(sender, receiver, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"