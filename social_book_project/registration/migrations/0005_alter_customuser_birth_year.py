# Generated by Django 4.2.7 on 2024-02-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
