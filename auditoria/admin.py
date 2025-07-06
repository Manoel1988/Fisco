# auditoria/admin.py

from django.contrib import admin
from .models import Empresa, NotaFiscal, DocumentoFiscal # Importe DocumentoFiscal

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'regime_tributario', 'data_cadastro')
    search_fields = ('razao_social', 'cnpj')
    list_filter = ('regime_tributario',)

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'empresa', 'data_emissao', 'valor_total', 'valor_pis', 'valor_cofins')
    list_filter = ('empresa', 'data_emissao')
    search_fields = ('numero', 'empresa__razao_social', 'descricao_produtos')
    raw_id_fields = ('empresa',)

@admin.register(DocumentoFiscal)
class DocumentoFiscalAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'tipo_documento', 'mes', 'ano', 'data_upload', 'arquivo')
    list_filter = ('empresa', 'tipo_documento', 'ano', 'mes')
    search_fields = ('empresa__razao_social', 'tipo_documento')
    raw_id_fields = ('empresa',)