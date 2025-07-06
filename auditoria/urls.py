# auditoria/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),
    path('auditar/<int:empresa_id>/', views.detalhes_auditoria, name='detalhes_auditoria'),
    path('upload/<int:empresa_id>/', views.upload_documentos, name='upload_documentos'),
    path('analisar_ajax/<int:empresa_id>/', views.analisar_empresa_ajax, name='analisar_empresa_ajax'),
    path('upload-tipi-pdf/', views.upload_tipi_pdf, name='upload_tipi_pdf'),
]