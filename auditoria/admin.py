# auditoria/admin.py

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Empresa, NotaFiscal, DocumentoFiscal, TabelaTIPI, Legislacao

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'regime_tributario', 'data_cadastro')
    list_filter = ('regime_tributario', 'data_cadastro')
    search_fields = ('razao_social', 'cnpj')
    readonly_fields = ('data_cadastro',)
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('razao_social', 'cnpj', 'regime_tributario')
        }),
        ('Datas', {
            'fields': ('data_cadastro',)
        }),
        ('Resultados de Auditoria', {
            'fields': ('resultado_auditoria', 'resultado_ia'),
            'classes': ('collapse',)
        }),
    )

# @admin.register(NotaFiscal)
# class NotaFiscalAdmin(admin.ModelAdmin):
#     list_display = ('numero', 'empresa', 'data_emissao', 'valor_total', 'valor_pis', 'valor_cofins')
#     list_filter = ('empresa', 'data_emissao')
#     search_fields = ('numero', 'empresa__razao_social', 'descricao_produtos')
#     raw_id_fields = ('empresa',)

@admin.register(DocumentoFiscal)
class DocumentoFiscalAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'tipo_documento', 'mes', 'ano', 'data_upload', 'arquivo')
    list_filter = ('tipo_documento', 'ano', 'mes', 'data_upload')
    search_fields = ('empresa__razao_social', 'empresa__cnpj', 'tipo_documento')
    raw_id_fields = ('empresa',)
    list_per_page = 50
    date_hierarchy = 'data_upload'
    
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('empresa', 'tipo_documento', 'mes', 'ano')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'data_upload'),
        }),
    )
    readonly_fields = ('data_upload',)

@admin.register(TabelaTIPI)
class TabelaTIPIAdmin(admin.ModelAdmin):
    list_display = ('codigo_ncm', 'descricao', 'aliquota_ipi', 'ativo', 'data_atualizacao')
    list_filter = ('ativo', 'aliquota_ipi', 'data_atualizacao')
    search_fields = ('codigo_ncm', 'descricao', 'observacoes')
    list_editable = ('ativo',)
    list_per_page = 100
    
    fieldsets = (
        ('Informações TIPI', {
            'fields': ('codigo_ncm', 'descricao', 'aliquota_ipi')
        }),
        ('Detalhes', {
            'fields': ('observacoes', 'decreto_origem', 'ativo')
        }),
        ('Controle', {
            'fields': ('data_atualizacao',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('data_atualizacao',)
    
    def descricao_resumida(self, obj):
        return obj.descricao[:100] + "..." if len(obj.descricao) > 100 else obj.descricao
    descricao_resumida.short_description = "Descrição"
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Calcular estatísticas da TIPI
        from decimal import Decimal
        
        extra_context['ativos_count'] = TabelaTIPI.objects.filter(ativo=True).count()
        extra_context['isentos_count'] = TabelaTIPI.objects.filter(
            ativo=True, 
            aliquota_ipi=Decimal('0.00')
        ).count()
        extra_context['tributados_count'] = TabelaTIPI.objects.filter(
            ativo=True, 
            aliquota_ipi__gt=Decimal('0.00')
        ).count()
        
        return super().changelist_view(request, extra_context)

@admin.register(Legislacao)
class LegislacaoAdmin(admin.ModelAdmin):
    list_display = ('get_identificacao', 'titulo', 'tipo', 'area', 'esfera', 'relevancia', 'ativo')
    list_filter = ('tipo', 'area', 'esfera', 'orgao', 'relevancia', 'ativo', 'data_publicacao')
    search_fields = ('titulo', 'numero', 'ementa', 'palavras_chave')
    list_editable = ('relevancia', 'ativo')
    filter_horizontal = ('legislacao_relacionada',)
    list_per_page = 50
    date_hierarchy = 'data_publicacao'
    
    fieldsets = (
        ('Identificação', {
            'fields': ('titulo', 'numero', 'ano', 'tipo', 'area', 'orgao', 'esfera')
        }),
        ('Datas', {
            'fields': ('data_publicacao', 'data_vigencia', 'data_revogacao')
        }),
        ('Conteúdo', {
            'fields': ('ementa', 'resumo', 'texto_completo')
        }),
        ('Referências', {
            'fields': ('url_oficial', 'diario_oficial', 'legislacao_relacionada')
        }),
        ('Metadados', {
            'fields': ('palavras_chave', 'relevancia', 'ativo'),
            'classes': ('collapse',)
        }),
    )
    
    def get_identificacao(self, obj):
        return obj.get_identificacao()
    get_identificacao.short_description = 'Identificação'
    get_identificacao.admin_order_field = 'numero'

# Configuração do site admin
admin.site.site_header = 'Sistema Fisco - Administração'
admin.site.site_title = 'Fisco Admin'
admin.site.index_title = 'Painel de Controle'