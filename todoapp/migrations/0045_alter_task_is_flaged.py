# Generated by Django 4.2.6 on 2024-07-26 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0044_task_approvals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='is_flaged',
            field=models.BooleanField(default=False, verbose_name='Flaged'),
        ),
    ]
