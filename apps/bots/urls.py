from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path(
        "handle_telegram_webhook/<str:bot_token>",
        csrf_exempt(views.handle_telegram_webhook),
        name="telegram_webhook",
    ),
    path(
        "telegram-bots/",
        views.TelegramBotsListView.as_view(),
        name="telegram-bots-list",
    ),
]
