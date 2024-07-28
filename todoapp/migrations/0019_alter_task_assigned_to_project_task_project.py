# Generated by Django 4.2.6 on 2024-07-08 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todoapp', '0018_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projname', models.CharField(max_length=100)),
                ('assignedTo', models.ManyToManyField(related_name='assigned_project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='todoapp.project'),
        ),
    ]