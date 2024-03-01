# Generated by Django 5.0.2 on 2024-02-22 22:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30)),
                ('_name', models.CharField(blank=True, editable=False, max_length=30, null=True)),
                ('bot_token', models.CharField(max_length=255)),
                ('_bot_token', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('bot_username', models.CharField(blank=True, editable=False, max_length=125, null=True)),
            ],
            options={
                'db_table': 'telegram_bots',
            },
        ),
        migrations.CreateModel(
            name='TelegramProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('telegram_id', models.PositiveBigIntegerField()),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('bot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bots.telegrambot')),
            ],
            options={
                'db_table': 'telegram_profiles',
            },
        ),
    ]
