import requests

from housedata.config import GROUP_TELEGRAM_ID, TELEGRAM_BOT_TOKEN

url_get_updates = (
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"  # retrieve ids
)
url_get_send_message = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(message):
    params = {"text": message, "chat_id": GROUP_TELEGRAM_ID}
    res = requests.get(url_get_send_message, params=params)
    data = res.json()
    print(data)


if __name__ == "__main__":
    send_message("test message")
