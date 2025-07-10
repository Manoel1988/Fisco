# auditoria/urls.py

from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),
    path('cadastrar/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('auditar/<int:empresa_id>/', views.detalhes_auditoria, name='detalhes_auditoria'),
    path('upload/<int:empresa_id>/', views.upload_documentos, name='upload_documentos'),
    path('analisar_ajax/<int:empresa_id>/', views.analisar_empresa_ajax, name='analisar_empresa_ajax'),
    path('pdf/<int:empresa_id>/', views.gerar_pdf_analise, name='gerar_pdf_analise'),
    path('excluir/<int:empresa_id>/', views.excluir_empresa, name='excluir_empresa'),
    path('legislacoes/', views.legislacoes, name='legislacoes'),
    path('legislacoes/<int:legislacao_id>/', views.detalhes_legislacao, name='detalhes_legislacao'),
]