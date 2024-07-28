# Generated by Django 4.2.6 on 2024-07-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0034_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('UI/UX Designer', 'UI/UX Designer'), ('Backend Developer ', 'Backend Developer'), ('Full Stack Developer ', 'Full Stack Developer'), ('Cloud Developer ', 'Cloud Developer')], max_length=50, null=True),
        ),
    ]