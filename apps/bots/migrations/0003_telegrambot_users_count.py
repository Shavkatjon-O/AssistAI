# Generated by Django 5.0.2 on 2024-02-24 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0002_rename__name_telegrambot__title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambot',
            name='users_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]