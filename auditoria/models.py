from django.db import models
from django.contrib.postgres.fields import JSONField
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    """Valida extensões de arquivo permitidas"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.xml', '.txt', '.csv', '.xlsx', '.xls']
    if ext not in valid_extensions:
        raise ValidationError(f'Tipo de arquivo não permitido. Extensões válidas: {", ".join(valid_extensions)}')

def validate_file_size(value):
    """Valida tamanho máximo do arquivo (50MB)"""
    filesize = value.size
    if filesize > 50 * 1024 * 1024:  # 50MB
        raise ValidationError("O arquivo não pode ser maior que 50MB.")

# Create your models here.
# auditoria/models.py

class Empresa(models.Model):
    # Dados básicos
    razao_social = models.CharField(max_length=255, unique=True, db_index=True)
    cnpj = models.CharField(max_length=18, unique=True, db_index=True) # Formato XX.XXX.XXX/YYYY-ZZ
    regime_tributario = models.CharField(
        max_length=20,
        choices=[
            ('SIMPLES', 'Simples Nacional'),
            ('PRESUMIDO', 'Lucro Presumido'),
            ('REAL', 'Lucro Real'),
        ],
        default='SIMPLES',
        db_index=True
    )
    
    # Informações para análise fiscal avançada
    atividade_principal = models.CharField(max_length=300, blank=True, help_text="Atividade principal da empresa")
    cnae_principal = models.CharField(max_length=10, blank=True, help_text="CNAE principal (ex: 6201-5)")
    
    # Dados financeiros
    faturamento_anual = models.CharField(
        max_length=20,
        choices=[
            ('ATE_360K', 'Até R$ 360.000'),
            ('360K_4_8M', 'De R$ 360.000 a R$ 4.800.000'),
            ('4_8M_300M', 'De R$ 4.800.000 a R$ 300.000.000'),
            ('ACIMA_300M', 'Acima de R$ 300.000.000'),
        ],
        blank=True,
        help_text="Faixa de faturamento anual"
    )
    
    # Estrutura da empresa
    numero_funcionarios = models.CharField(
        max_length=20,
        choices=[
            ('0_9', '0 a 9 funcionários'),
            ('10_49', '10 a 49 funcionários'),
            ('50_99', '50 a 99 funcionários'),
            ('100_499', '100 a 499 funcionários'),
            ('500_MAIS', '500 ou mais funcionários'),
        ],
        blank=True,
        help_text="Número de funcionários"
    )
    
    # Características operacionais
    tem_filiais = models.BooleanField(default=False, help_text="Possui filiais?")
    estados_operacao = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Estados onde opera (separados por vírgula)"
    )
    
    # Operações especiais
    exporta = models.BooleanField(default=False, help_text="Realiza exportações?")
    importa = models.BooleanField(default=False, help_text="Realiza importações?")
    
    # Benefícios e regimes especiais
    tem_beneficios_fiscais = models.BooleanField(default=False, help_text="Possui benefícios fiscais?")
    quais_beneficios = models.TextField(blank=True, help_text="Quais benefícios fiscais possui?")
    
    regime_apuracao = models.CharField(
        max_length=20,
        choices=[
            ('MENSAL', 'Apuração Mensal'),
            ('TRIMESTRAL', 'Apuração Trimestral'),
            ('ANUAL', 'Apuração Anual'),
        ],
        blank=True,
        help_text="Regime de apuração dos tributos"
    )
    
    # Setor e atividades
    setor_atuacao = models.CharField(
        max_length=50,
        choices=[
            ('INDUSTRIA', 'Indústria'),
            ('COMERCIO', 'Comércio'),
            ('SERVICOS', 'Serviços'),
            ('CONSTRUCAO', 'Construção Civil'),
            ('AGRICULTURA', 'Agricultura'),
            ('TECNOLOGIA', 'Tecnologia'),
            ('SAUDE', 'Saúde'),
            ('EDUCACAO', 'Educação'),
            ('FINANCEIRO', 'Financeiro'),
            ('TRANSPORTES', 'Transportes'),
            ('OUTROS', 'Outros'),
        ],
        blank=True,
        help_text="Setor principal de atuação"
    )
    
    # Gastos especiais
    tem_gastos_pd = models.BooleanField(default=False, help_text="Tem gastos com Pesquisa e Desenvolvimento?")
    tem_gastos_treinamento = models.BooleanField(default=False, help_text="Tem gastos com treinamento de funcionários?")
    tem_gastos_ambientais = models.BooleanField(default=False, help_text="Tem gastos com preservação ambiental?")
    
    # Tipos de contratação
    usa_pj = models.BooleanField(default=False, help_text="Contrata Pessoa Jurídica (PJ)?")
    usa_terceirizacao = models.BooleanField(default=False, help_text="Usa serviços terceirizados?")
    
    # Produtos e NCM
    principais_ncm = models.TextField(
        blank=True,
        help_text="Principais códigos NCM dos produtos (separados por vírgula)"
    )
    produtos_principais = models.TextField(
        blank=True,
        help_text="Descrição dos principais produtos comercializados"
    )
    
    # Observações gerais
    observacoes_fiscais = models.TextField(
        blank=True, 
        help_text="Observações especiais sobre a situação fiscal da empresa"
    )
    
    # Campos existentes
    data_cadastro = models.DateTimeField(auto_now_add=True, db_index=True)
    resultado_auditoria = models.JSONField(null=True, blank=True)
    resultado_ia = models.TextField(null=True, blank=True)
    
    # Localização para cruzamento com legislações locais
    cidade = models.CharField(max_length=100, blank=True, help_text="Cidade onde está localizada a empresa")
    estado = models.CharField(max_length=50, blank=True, help_text="Estado onde está localizada a empresa")
    uf = models.CharField(
        max_length=2, 
        blank=True, 
        help_text="UF do estado (ex: SP, RJ, MG)",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ]
    )
    cep = models.CharField(
        max_length=9, 
        blank=True, 
        help_text="CEP da empresa (formato: XXXXX-XXX)"
    )

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

    class Meta:
        indexes = [
            models.Index(fields=['razao_social']),
            models.Index(fields=['cnpj']),
            models.Index(fields=['regime_tributario']),
        ]

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
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES, db_index=True)
    mes = models.IntegerField(choices=MES_CHOICES, db_index=True)
    ano = models.IntegerField(db_index=True)
    arquivo = models.FileField(
        upload_to='documentos_fiscais/%Y/%m/',
        validators=[validate_file_extension, validate_file_size]
    )
    data_upload = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = (('empresa', 'tipo_documento', 'mes', 'ano'),) # Garante unicidade
        ordering = ['ano', 'mes'] # Ordena por ano e mês
        indexes = [
            models.Index(fields=['empresa', 'ano']),
            models.Index(fields=['tipo_documento', 'ano']),
            models.Index(fields=['ano', 'mes']),
            models.Index(fields=['data_upload']),
        ]

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



# NOVO MODELO: Legislação
class Legislacao(models.Model):
    TIPO_CHOICES = [
        ('LEI', 'Lei'),
        ('DECRETO', 'Decreto'),
        ('INSTRUCAO_NORMATIVA', 'Instrução Normativa'),
        ('PORTARIA', 'Portaria'),
        ('RESOLUCAO', 'Resolução'),
        ('MEDIDA_PROVISORIA', 'Medida Provisória'),
        ('CONSTITUICAO', 'Constituição'),
        ('CODIGO', 'Código'),
        ('CONSOLIDACAO', 'Consolidação'),
        ('ATO_DECLARATORIO', 'Ato Declaratório'),
        ('SOLUCAO_CONSULTA', 'Solução de Consulta'),
        ('PARECER', 'Parecer'),
    ]
    
    AREA_CHOICES = [
        ('TRIBUTARIO', 'Tributário'),
        ('FISCAL', 'Fiscal'),
        ('TRABALHISTA', 'Trabalhista'),
        ('PREVIDENCIARIO', 'Previdenciário'),
        ('COMERCIAL', 'Comercial'),
        ('CIVIL', 'Civil'),
        ('PENAL', 'Penal'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('CONSTITUCIONAL', 'Constitucional'),
        ('AMBIENTAL', 'Ambiental'),
    ]
    
    ORGAO_CHOICES = [
        ('RECEITA_FEDERAL', 'Receita Federal do Brasil'),
        ('CONGRESSO_NACIONAL', 'Congresso Nacional'),
        ('PRESIDENCIA', 'Presidência da República'),
        ('MINISTERIO_FAZENDA', 'Ministério da Fazenda'),
        ('MINISTERIO_ECONOMIA', 'Ministério da Economia'),
        ('MINISTERIO_TRABALHO', 'Ministério do Trabalho'),
        ('INSS', 'Instituto Nacional do Seguro Social'),
        ('CONFAZ', 'Conselho Nacional de Política Fazendária'),
        ('CARF', 'Conselho Administrativo de Recursos Fiscais'),
        ('STF', 'Supremo Tribunal Federal'),
        ('STJ', 'Superior Tribunal de Justiça'),
        ('TST', 'Tribunal Superior do Trabalho'),
        ('TCU', 'Tribunal de Contas da União'),
        ('SENADO_FEDERAL', 'Senado Federal'),
        ('OUTROS', 'Outros'),
    ]
    
    ESFERA_CHOICES = [
        ('FEDERAL', 'Federal'),
        ('ESTADUAL', 'Estadual'),
        ('MUNICIPAL', 'Municipal'),
    ]

    # Campos básicos
    titulo = models.CharField(max_length=500, help_text="Título da legislação")
    numero = models.CharField(max_length=50, help_text="Número da legislação")
    ano = models.IntegerField(help_text="Ano da legislação")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, help_text="Tipo de legislação")
    area = models.CharField(max_length=30, choices=AREA_CHOICES, help_text="Área de aplicação")
    orgao = models.CharField(max_length=30, choices=ORGAO_CHOICES, help_text="Órgão emissor")
    esfera = models.CharField(max_length=20, choices=ESFERA_CHOICES, default='FEDERAL', help_text="Esfera de competência")
    
    # Localização específica para legislações estaduais e municipais
    estado_especifico = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Estado específico para legislações estaduais"
    )
    uf_especifica = models.CharField(
        max_length=2, 
        blank=True, 
        help_text="UF específica para legislações estaduais (ex: SP, RJ, MG)",
        choices=[
            ('', 'Não especificado'),
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ]
    )
    municipio_especifico = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Município específico para legislações municipais"
    )
    
    # Datas
    data_publicacao = models.DateField(help_text="Data de publicação")
    data_vigencia = models.DateField(null=True, blank=True, help_text="Data de início da vigência")
    data_revogacao = models.DateField(null=True, blank=True, help_text="Data de revogação (se aplicável)")
    
    # Conteúdo
    ementa = models.TextField(help_text="Ementa da legislação")
    texto_completo = models.TextField(blank=True, help_text="Texto completo da legislação")
    resumo = models.TextField(blank=True, help_text="Resumo executivo")
    
    # Links e referências
    url_oficial = models.URLField(blank=True, help_text="URL oficial da legislação")
    diario_oficial = models.CharField(max_length=200, blank=True, help_text="Referência do Diário Oficial")
    
    # Relacionamentos
    legislacao_relacionada = models.ManyToManyField('self', blank=True, symmetrical=False, help_text="Legislações relacionadas")
    
    # Metadados
    palavras_chave = models.TextField(blank=True, help_text="Palavras-chave separadas por vírgula")
    ativo = models.BooleanField(default=True, help_text="Se a legislação está ativa")
    relevancia = models.IntegerField(default=3, choices=[(1, 'Baixa'), (2, 'Média'), (3, 'Alta'), (4, 'Crítica')], help_text="Relevância para o sistema")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Legislação"
        verbose_name_plural = "Legislações"
        ordering = ['-data_publicacao', '-relevancia']
        unique_together = [['tipo', 'numero', 'ano', 'orgao']]
    
    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero}/{self.ano} - {self.titulo[:100]}"
    
    def get_identificacao(self):
        """Retorna identificação completa da legislação"""
        return f"{self.get_tipo_display()} nº {self.numero}/{self.ano}"
    
    def esta_vigente(self):
        """Verifica se a legislação está vigente"""
        from datetime import date
        hoje = date.today()
        
        if self.data_revogacao and self.data_revogacao <= hoje:
            return False
        
        if self.data_vigencia and self.data_vigencia > hoje:
            return False
            
        return self.ativo
