from django.db import models
from apps.common.models import TimeStampedModel

from utils import bot
from . import tasks


class TelegramBot(TimeStampedModel):
    title = models.CharField(max_length=30)
    _title = models.CharField(max_length=30, editable=False, null=True, blank=True)

    bot_token = models.CharField(max_length=255)
    _bot_token = models.CharField(max_length=255, editable=False, null=True, blank=True)

    bot_username = models.CharField(
        max_length=125, editable=False, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self._bot_token != self.bot_token:
            tasks.set_webhook_request.delay(self.bot_token)

            username = bot.get_username_request(self.bot_token)
            self.bot_username = username

            self._bot_token = self.bot_token

        if self._title != self.title:
            tasks.set_name_request.delay(self.bot_token, self.title)

            self._title = self.title

        super(TelegramBot, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "telegram_bots"


class TelegramProfile(TimeStampedModel):
    bot = models.ForeignKey(TelegramBot, models.CASCADE, null=True)
    telegram_id = models.PositiveBigIntegerField()
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username} {self.telegram_id}"

    class Meta:
        db_table = "telegram_profiles"
