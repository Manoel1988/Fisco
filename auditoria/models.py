from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
# auditoria/models.py

class Empresa(models.Model):
    razao_social = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=18, unique=True) # Formato XX.XXX.XXX/YYYY-ZZ
    regime_tributario = models.CharField(
        max_length=20,
        choices=[
            ('SIMPLES', 'Simples Nacional'),
            ('PRESUMIDO', 'Lucro Presumido'),
            ('REAL', 'Lucro Real'),
        ],
        default='SIMPLES'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    resultado_auditoria = models.JSONField(null=True, blank=True)
    resultado_ia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

class NotaFiscal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notas_fiscais')
    numero = models.CharField(max_length=50)
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pis = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_cofins = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_iss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_icms = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao_produtos = models.TextField(blank=True)
    xml_file = models.FileField(upload_to='nfe_xmls/', null=True, blank=True) # Para uploads de XML
    # Adicionar mais campos conforme a necessidade (ex: tipo de produto, NCM, etc.)

    def __str__(self):
        return f"NF {self.numero} de {self.empresa.razao_social} ({self.valor_total})"

    class Meta:
        unique_together = (('empresa', 'numero', 'data_emissao'),) # Garante que não haja NF duplicada para a mesma empresa na mesma data

# NOVO MODELO: DocumentoFiscal
class DocumentoFiscal(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DIRF', 'DIRF'),
        ('DMRI', 'DMRI'),
        ('DAS', 'DAS'),
        ('NFE', 'Nota Fiscal Eletrônica (NF-e)'),
        ('NFCE', 'Nota Fiscal de Consumidor Eletrônica (NFC-e)'),
        ('NFSE', 'Nota Fiscal de Serviço Eletrônica (NFS-e)'),
        ('CTE', 'Conhecimento de Transporte Eletrônico (CT-e)'),
        ('LIVRO_FISCAL', 'Livro Fiscal'),
        ('BALANCETE', 'Balancete'),
        ('SPED_ECF', 'SPED ECF'),
        ('SPED_ECD', 'SPED ECD'),
        ('SPED_EFD_ICMS_IPI', 'SPED EFD-ICMS/IPI'),
        ('SPED_EFD_CONTRIBUICOES', 'SPED EFD-Contribuições'),
        ('DCTF', 'DCTF'),
        ('DARF', 'DARF'),
        ('GPS', 'GPS'),
        ('GRF', 'GRF'),
        ('DEFIS', 'DEFIS'),
        ('MDFE', 'Manifesto de Documentos Fiscais Eletrônicos (MDF-e)'),
        # Adicione outros tipos conforme necessário
    ]

    MES_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='documentos_fiscais')
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    mes = models.IntegerField(choices=MES_CHOICES)
    ano = models.IntegerField()
    arquivo = models.FileField(upload_to='documentos_fiscais/%Y/%m/') # Organiza por ano/mes
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('empresa', 'tipo_documento', 'mes', 'ano'),) # Garante unicidade
        ordering = ['ano', 'mes'] # Ordena por ano e mês

    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.get_mes_display()}/{self.ano} ({self.empresa.razao_social})"

# NOVO MODELO: Tabela TIPI
class TabelaTIPI(models.Model):
    codigo_ncm = models.CharField(max_length=20, unique=True, help_text="Código NCM do produto")
    descricao = models.TextField(help_text="Descrição do produto conforme TIPI")
    aliquota_ipi = models.DecimalField(max_digits=5, decimal_places=2, help_text="Alíquota do IPI em %")
    observacoes = models.TextField(blank=True, help_text="Observações e exceções")
    data_atualizacao = models.DateTimeField(auto_now=True, help_text="Data da última atualização")
    decreto_origem = models.CharField(max_length=100, blank=True, help_text="Decreto que estabeleceu/alterou a alíquota")
    vigencia_inicio = models.DateField(null=True, blank=True, help_text="Data de início da vigência")
    vigencia_fim = models.DateField(null=True, blank=True, help_text="Data de fim da vigência (se aplicável)")
    ativo = models.BooleanField(default=True, help_text="Se o código está ativo")

    class Meta:
        verbose_name = "Tabela TIPI"
        verbose_name_plural = "Tabelas TIPI"
        ordering = ['codigo_ncm']

    def __str__(self):
        return f"{self.codigo_ncm} - {self.aliquota_ipi}% IPI"

# NOVO MODELO: Histórico de Atualizações TIPI
class HistoricoAtualizacaoTIPI(models.Model):
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    total_registros = models.IntegerField(help_text="Total de registros atualizados")
    registros_novos = models.IntegerField(help_text="Registros novos adicionados")
    registros_alterados = models.IntegerField(help_text="Registros existentes alterados")
    fonte_dados = models.CharField(max_length=255, help_text="URL ou fonte dos dados")
    usuario = models.CharField(max_length=100, help_text="Usuário que executou a atualização")
    sucesso = models.BooleanField(default=True)
    log_detalhes = models.TextField(blank=True, help_text="Log detalhado da atualização")

    class Meta:
        verbose_name = "Histórico de Atualização TIPI"
        verbose_name_plural = "Históricos de Atualizações TIPI"
        ordering = ['-data_atualizacao']

    def __str__(self):
        status = "Sucesso" if self.sucesso else "Falha"
        return f"Atualização {self.data_atualizacao.strftime('%d/%m/%Y %H:%M')} - {status}"
