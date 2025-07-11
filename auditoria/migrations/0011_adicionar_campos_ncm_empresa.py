# Generated by Django 5.2.4 on 2025-07-10 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0010_adicionar_campos_empresa_avancados'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='principais_ncm',
            field=models.TextField(blank=True, help_text='Principais códigos NCM dos produtos (separados por vírgula)'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='produtos_principais',
            field=models.TextField(blank=True, help_text='Descrição dos principais produtos comercializados'),
        ),
    ]
