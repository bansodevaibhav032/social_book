# Generated by Django 4.2.7 on 2024-02-29 08:38

from django.db import migrations
import registration.managers


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_customuser_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', registration.managers.UserManager()),
            ],
        ),
    ]
