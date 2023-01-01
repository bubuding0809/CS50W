# Generated by Django 4.0.4 on 2022-05-08 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auction_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='details',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(max_length=30),
        ),
        migrations.AlterField(
            model_name='auction',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]