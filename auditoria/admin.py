# auditoria/admin.py

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Empresa, NotaFiscal, DocumentoFiscal, TabelaTIPI, HistoricoAtualizacaoTIPI

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'regime_tributario', 'data_cadastro')
    search_fields = ('razao_social', 'cnpj')
    list_filter = ('regime_tributario',)

# @admin.register(NotaFiscal)
# class NotaFiscalAdmin(admin.ModelAdmin):
#     list_display = ('numero', 'empresa', 'data_emissao', 'valor_total', 'valor_pis', 'valor_cofins')
#     list_filter = ('empresa', 'data_emissao')
#     search_fields = ('numero', 'empresa__razao_social', 'descricao_produtos')
#     raw_id_fields = ('empresa',)

@admin.register(DocumentoFiscal)
class DocumentoFiscalAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'tipo_documento', 'mes', 'ano', 'data_upload', 'arquivo')
    list_filter = ('empresa', 'tipo_documento', 'ano', 'mes')
    search_fields = ('empresa__razao_social', 'tipo_documento')
    raw_id_fields = ('empresa',)

@admin.register(TabelaTIPI)
class TabelaTIPIAdmin(admin.ModelAdmin):
    list_display = ('codigo_ncm', 'descricao_resumida', 'aliquota_ipi', 'decreto_origem', 'vigencia_inicio', 'ativo', 'data_atualizacao')
    list_filter = ('ativo', 'aliquota_ipi', 'data_atualizacao')
    search_fields = ('codigo_ncm', 'descricao', 'decreto_origem')
    list_editable = ('ativo',)
    readonly_fields = ('data_atualizacao',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo_ncm', 'descricao', 'aliquota_ipi', 'ativo')
        }),
        ('Detalhes Legais', {
            'fields': ('decreto_origem', 'vigencia_inicio', 'vigencia_fim', 'observacoes')
        }),
        ('Controle', {
            'fields': ('data_atualizacao',),
            'classes': ('collapse',)
        })
    )
    
    def descricao_resumida(self, obj):
        return obj.descricao[:100] + "..." if len(obj.descricao) > 100 else obj.descricao
    descricao_resumida.short_description = "Descrição"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('atualizar-tipi/', self.admin_site.admin_view(self.atualizar_tipi_view), name='auditoria_tabelatipi_atualizar'),
        ]
        return custom_urls + urls
    
    def atualizar_tipi_view(self, request):
        """View para atualizar a tabela TIPI via webscraping"""
        from .services.tipi_service import TIPIService
        
        try:
            service = TIPIService()
            resultado = service.atualizar_tabela_tipi(request.user.username if request.user.is_authenticated else 'admin')
            
            if resultado['sucesso']:
                messages.success(request, 
                    f"Tabela TIPI atualizada com sucesso! "
                    f"Novos registros: {resultado['novos']}, "
                    f"Registros alterados: {resultado['alterados']}, "
                    f"Total: {resultado['total']}")
            else:
                messages.error(request, f"Erro ao atualizar tabela TIPI: {resultado['erro']}")
                
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
        
        return HttpResponseRedirect(reverse('admin:auditoria_tabelatipi_changelist'))
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['botao_atualizar'] = True
        return super().changelist_view(request, extra_context)

@admin.register(HistoricoAtualizacaoTIPI)
class HistoricoAtualizacaoTIPIAdmin(admin.ModelAdmin):
    list_display = ('data_atualizacao', 'total_registros', 'registros_novos', 'registros_alterados', 'sucesso', 'usuario')
    list_filter = ('sucesso', 'data_atualizacao')
    search_fields = ('usuario', 'fonte_dados')
    readonly_fields = ('data_atualizacao',)
    
    def has_add_permission(self, request):
        return False  # Não permite adicionar manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Apenas superuser pode deletar