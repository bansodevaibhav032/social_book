# Generated by Django 5.0.2 on 2024-02-29 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_alter_customuser_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('visibility', models.BooleanField(default=True)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('year_published', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]