from celery import shared_task

from utils import bot


@shared_task
def set_webhook_request(bot_token):
    bot.set_webhook_request(bot_token)


@shared_task
def set_name_request(bot_token, new_name):
    bot.set_name_request(bot_token, new_name)
