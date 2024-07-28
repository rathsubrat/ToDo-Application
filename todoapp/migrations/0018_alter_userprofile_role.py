# Generated by Django 4.2.6 on 2024-07-08 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0017_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('User', 'User'), ('Super User', 'Super User'), ('Manager', 'Manager')], default='User', max_length=50),
        ),
    ]
