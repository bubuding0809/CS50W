# Generated by Django 4.0.4 on 2022-05-07 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_auction_image_file_auction_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_image',
            name='auction_item',
        ),
        migrations.AddField(
            model_name='auction',
            name='images',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='auctions.auction_image'),
        ),
    ]
