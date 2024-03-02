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

from utils.bot import set_webhook_request


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
    fields = ("title", "bot_token")
    template_name = "bots/telegram-bots-create.html"    

    
    def get_form(self, form_class=None):
        form_class = super().get_form(form_class)
        form_class.fields["title"].label = "Bot name"
        return form_class
    

    def form_valid(self, form):
        token = form.instance.bot_token
        bot_exists = models.TelegramBot.objects.filter(bot_token=token).exists()
    
        if bot_exists:
            form.add_error("bot_token", "Telegram bot with this token already exists.")
            return self.form_invalid(form)
        
        response = set_webhook_request(token)
        if response.status_code != 200:
            form.add_error("bot_token", "Please enter valid telegram bot token.")
            return self.form_invalid(form)
            
        form.instance.created_by = self.request.user
        return super(TelegramBotCreateView, self).form_valid(form)
