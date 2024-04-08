import requests
# TOKEN = "6952188490:AAFH68TkzPvukC2cHvLoycGHyiK7MkaKSN8"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

def send_massage(message):
    TOKEN = "6952188490:AAFH68TkzPvukC2cHvLoycGHyiK7MkaKSN8"
    chat_id = "1251487807"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()