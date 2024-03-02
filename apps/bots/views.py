import os
import json

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from queue import Queue

from telegram import Update, Bot
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    PicklePersistence,
    Filters,
)

from .telegrambot import start, message
from .models import TelegramBot


def setup(token):
    bot = Bot(token=token)
    queue = Queue()
    # create the dispatcher
    if not os.path.exists(os.path.join(settings.BASE_DIR, "media", "state_record")):
        os.makedirs(os.path.join(settings.BASE_DIR, "media", "state_record"))
    dp = Dispatcher(
        bot,
        queue,
        workers=4,
        use_context=True,
        persistence=PicklePersistence(
            filename=os.path.join(
                settings.BASE_DIR, "media", "state_record", f"{bot.username}.pkl"
            ),
            single_file=True,
        ),
    )

    states = {}
    entry_points = [CommandHandler("start", start)]
    fallbacks = [CommandHandler("start", start)]
    conversation_handler = ConversationHandler(
        entry_points=entry_points,
        states=states,
        fallbacks=fallbacks,
        persistent=True,
        name=f"{bot.username}_conversation",
    )
    dp.add_handler(conversation_handler)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message))
    return dp


def handle_telegram_webhook(request, bot_token):
    bot = Bot(token=bot_token)
    update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
    dp = setup(bot_token)
    try:
        if update.message.chat.type == "private":
            dp.process_update(update)
    except Exception as e:
        print(e)
        dp.process_update(update)
    return JsonResponse({"status": "ok"})


class TelegramBotsListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("account_login")

    model = TelegramBot
    template_name = "bots/telegram-bots-list.html"
    context_object_name = "telegram_bots"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset