"""from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)

if __name__ == "__main__":
    app.run()"""

import requests
import json
from colorama import Fore, Style

url = 'https://api.ukrainealarm.com/api/v3/alerts/2'

headers = {
    "accept": "application/json",
    "Authorization": "2d1f0ace:e0d9835d81a5d88eceeebb5420540b1a"
}

r = requests.get(url=url, headers=headers)

if r.status_code == 200:
    data = json.loads(r.text)
    print(data)
else:
    print(Fore.RED+f"REQUESTS ERROR! Status code: {r.status_code}"+Style.RESET_ALL)
