import os
import json

from django.conf import settings
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

from apps.bots.telegrambot import start, message
from apps.bots import models

from utils.bot import (
    set_webhook_request,
    set_bot_name_request,
    get_bot_username_request,
)


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


class TelegramBotListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("account_login")

    model = models.TelegramBot
    template_name = "bots/telegram-bots-list.html"
    context_object_name = "telegram_bots"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class TelegramBotCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy("account_login")
    success_url = reverse_lazy("telegram-bots-list")

    model = models.TelegramBot
    fields = ("bot_name", "bot_token")
    template_name = "bots/telegram-bots-create.html"

    def form_valid(self, form):
        token = form.instance.bot_token
        bot_name = form.instance.bot_name

        response = set_webhook_request(token)
        if response.status_code != 200:
            form.add_error("bot_token", "Please enter valid telegram bot token.")
            return self.form_invalid(form)

        set_bot_name_request(token, bot_name)
        username = get_bot_username_request(token)

        form.instance.bot_username = username
        form.instance.created_by = self.request.user
        form.instance.is_active = True

        return super(TelegramBotCreateView, self).form_valid(form)
