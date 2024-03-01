import requests

from django.conf import settings


def set_webhook_request(bot_token):
    webhook_url = settings.WEBHOOK_URL
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bots/handle_telegram_webhook/{bot_token}"
    response = requests.post(url)
    return response.json()


def set_name_request(bot_token, new_name):
    url = f"https://api.telegram.org/bot{bot_token}/setMyName"
    response = requests.post(url, params={"name": new_name})
    return response.json()


def get_username_request(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    return response.json().get("result").get("username")
