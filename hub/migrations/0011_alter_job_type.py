# Generated by Django 5.1.4 on 2025-03-21 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0010_application_email_application_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='type',
            field=models.CharField(blank=True, choices=[('internal', 'internal'), ('external', 'external'), ('combined', 'combined')], max_length=100, null=True),
        ),
    ]
