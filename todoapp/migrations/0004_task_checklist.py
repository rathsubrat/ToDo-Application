# Generated by Django 4.2.6 on 2024-06-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0003_alter_task_done_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='checklist',
            field=models.TextField(blank=True, default='Not Available', null=True),
        ),
    ]
