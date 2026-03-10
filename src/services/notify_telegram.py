import requests

BOT_TOKEN = "bot_token"
CHAT_ID = "chat_id"

def notify_telegram(message: str):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )
    print(response.status_code, response.text)