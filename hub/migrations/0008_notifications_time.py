# Generated by Django 5.1.4 on 2025-02-20 06:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0007_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
