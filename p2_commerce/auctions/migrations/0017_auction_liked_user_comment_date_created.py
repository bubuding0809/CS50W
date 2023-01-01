# Generated by Django 4.0.4 on 2022-05-09 15:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_auction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='liked_user',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
