import requests

from django.conf import settings


def set_webhook_request(bot_token):
    webhook_url = settings.WEBHOOK_URL
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bots/handle_telegram_webhook/{bot_token}"
    response = requests.post(url)
    return response


def set_bot_name_request(bot_token, new_name):
    url = f"https://api.telegram.org/bot{bot_token}/setMyName"
    response = requests.post(url, params={"name": new_name})
    return response


def get_bot_username_request(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    username = response.json().get("result").get("username")
    return username
