# Generated by Django 4.2.6 on 2024-07-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0038_userprofile_wallet_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='wallet_money',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
