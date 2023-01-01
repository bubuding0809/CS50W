# Generated by Django 4.0.4 on 2022-05-07 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_image_delete_auction_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('CR', ' Cars'), ('CT', 'Computers & Tech'), ('PT', 'Pets'), ('FD', 'Food & Drinks'), ('FS', 'Fashion'), ('TY', 'Toys'), ('HM', 'Home')], max_length=20, null=True),
        ),
    ]