# Generated by Django 5.0.2 on 2024-03-02 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0009_remove_telegrambot_status_telegrambot_is_activated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambot',
            name='bot_token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]