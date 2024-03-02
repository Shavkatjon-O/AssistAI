from django.contrib import admin
from apps.bots import models


admin.site.register(models.TelegramProfile)


@admin.register(models.TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("id", "bot_name", "bot_token", "bot_username", "created_at")
