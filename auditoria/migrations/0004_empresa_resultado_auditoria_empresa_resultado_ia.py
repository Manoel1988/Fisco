# Generated by Django 5.2.4 on 2025-07-06 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0003_auto_20250705_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='resultado_auditoria',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='resultado_ia',
            field=models.TextField(blank=True, null=True),
        ),
    ]
