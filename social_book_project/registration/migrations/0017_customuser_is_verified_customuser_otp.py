# Generated by Django 4.2.7 on 2024-03-04 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_alter_customuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
