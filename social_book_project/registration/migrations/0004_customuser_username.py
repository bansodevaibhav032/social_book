# Generated by Django 4.2.7 on 2024-02-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='default_username', max_length=30, unique=True),
        ),
    ]
