# Generated by Django 4.0.4 on 2022-05-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_date_created_auction_date_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='auction',
            name='details',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
