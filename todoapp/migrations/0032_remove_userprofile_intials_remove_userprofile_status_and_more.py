# Generated by Django 4.2.6 on 2024-07-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0031_alter_userprofile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='intials',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='status',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='designation',
            field=models.CharField(choices=[('User', 'User'), ('Super User', 'Super User'), ('Manager', 'Manager'), ('Team Lead', 'Team Lead')], default='User', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('UI/UX Designer', 'UI/UX Designer'), ('Backend Developer ', 'Backend Developer'), ('Full Stack Developer ', 'Full Stack Developer'), ('Cloud Developer ', 'Cloud Developer')], default=('In Active', 'In Active'), max_length=50),
        ),
    ]
