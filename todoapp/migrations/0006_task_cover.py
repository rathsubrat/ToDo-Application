# Generated by Django 4.2.6 on 2024-06-25 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_alter_task_name_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='cover',
            field=models.CharField(blank=True, default='#ffffff', max_length=100, null=True),
        ),
    ]
