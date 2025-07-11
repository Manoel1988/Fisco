# Generated by Django 5.2.4 on 2025-07-07 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditoria', '0007_legislacao_esfera_alter_legislacao_orgao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentofiscal',
            name='ano',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='documentofiscal',
            name='data_upload',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='documentofiscal',
            name='mes',
            field=models.IntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], db_index=True),
        ),
        migrations.AlterField(
            model_name='documentofiscal',
            name='tipo_documento',
            field=models.CharField(choices=[('DIRF', 'DIRF'), ('DMRI', 'DMRI'), ('DAS', 'DAS'), ('NFE', 'Nota Fiscal Eletrônica (NF-e)'), ('NFCE', 'Nota Fiscal de Consumidor Eletrônica (NFC-e)'), ('NFSE', 'Nota Fiscal de Serviço Eletrônica (NFS-e)'), ('CTE', 'Conhecimento de Transporte Eletrônico (CT-e)'), ('LIVRO_FISCAL', 'Livro Fiscal'), ('BALANCETE', 'Balancete'), ('SPED_ECF', 'SPED ECF'), ('SPED_ECD', 'SPED ECD'), ('SPED_EFD_ICMS_IPI', 'SPED EFD-ICMS/IPI'), ('SPED_EFD_CONTRIBUICOES', 'SPED EFD-Contribuições'), ('DCTF', 'DCTF'), ('DARF', 'DARF'), ('GPS', 'GPS'), ('GRF', 'GRF'), ('DEFIS', 'DEFIS'), ('MDFE', 'Manifesto de Documentos Fiscais Eletrônicos (MDF-e)')], db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(db_index=True, max_length=18, unique=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='data_cadastro',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='razao_social',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='regime_tributario',
            field=models.CharField(choices=[('SIMPLES', 'Simples Nacional'), ('PRESUMIDO', 'Lucro Presumido'), ('REAL', 'Lucro Real')], db_index=True, default='SIMPLES', max_length=20),
        ),
        migrations.AddIndex(
            model_name='documentofiscal',
            index=models.Index(fields=['empresa', 'ano'], name='auditoria_d_empresa_739f3a_idx'),
        ),
        migrations.AddIndex(
            model_name='documentofiscal',
            index=models.Index(fields=['tipo_documento', 'ano'], name='auditoria_d_tipo_do_c4aadf_idx'),
        ),
        migrations.AddIndex(
            model_name='documentofiscal',
            index=models.Index(fields=['ano', 'mes'], name='auditoria_d_ano_6ad1f2_idx'),
        ),
        migrations.AddIndex(
            model_name='documentofiscal',
            index=models.Index(fields=['data_upload'], name='auditoria_d_data_up_31e88f_idx'),
        ),
        migrations.AddIndex(
            model_name='empresa',
            index=models.Index(fields=['razao_social'], name='auditoria_e_razao_s_2a1c72_idx'),
        ),
        migrations.AddIndex(
            model_name='empresa',
            index=models.Index(fields=['cnpj'], name='auditoria_e_cnpj_a16676_idx'),
        ),
        migrations.AddIndex(
            model_name='empresa',
            index=models.Index(fields=['regime_tributario'], name='auditoria_e_regime__648047_idx'),
        ),
    ]
