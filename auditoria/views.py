from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import requests
import PyPDF2
from time import sleep
import re
import logging

from .models import Empresa, NotaFiscal, DocumentoFiscal, TabelaTIPI, Legislacao
from .logica_auditoria import auditar_pis_cofins_monofasico, gerar_contexto_tipi_para_ia, auditar_ipi_com_tipi
from .forms import DocumentoFiscalForm, EmpresaForm

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from datetime import datetime

logger = logging.getLogger(__name__)

# Create your views here.
# auditoria/views.py

def lista_empresas(request):
    empresas = Empresa.objects.all().prefetch_related('documentos_fiscais').order_by('razao_social')
    context = {'empresas': empresas}
    return render(request, 'auditoria/lista_empresas.html', context)

def legislacoes(request):
    """View para exibir legislações com filtros e categorização"""
    legislacoes_queryset = Legislacao.objects.filter(ativo=True).prefetch_related('legislacao_relacionada')
    
    # Filtros
    esfera_filtro = request.GET.get('esfera', '')
    tipo_filtro = request.GET.get('tipo', '')
    area_filtro = request.GET.get('area', '')
    orgao_filtro = request.GET.get('orgao', '')
    relevancia_filtro = request.GET.get('relevancia', '')
    busca = request.GET.get('busca', '')
    
    # Aplicar filtros
    if esfera_filtro:
        legislacoes_queryset = legislacoes_queryset.filter(esfera=esfera_filtro)
    if tipo_filtro:
        legislacoes_queryset = legislacoes_queryset.filter(tipo=tipo_filtro)
    if area_filtro:
        legislacoes_queryset = legislacoes_queryset.filter(area=area_filtro)
    if orgao_filtro:
        legislacoes_queryset = legislacoes_queryset.filter(orgao=orgao_filtro)
    if relevancia_filtro:
        legislacoes_queryset = legislacoes_queryset.filter(relevancia=relevancia_filtro)
    if busca:
        legislacoes_queryset = legislacoes_queryset.filter(
            Q(titulo__icontains=busca) |
            Q(ementa__icontains=busca) |
            Q(palavras_chave__icontains=busca) |
            Q(numero__icontains=busca)
        )
    
    # Ordenação
    ordenacao = request.GET.get('ordenacao', '-data_publicacao')
    legislacoes_queryset = legislacoes_queryset.order_by(ordenacao)
    
    # Paginação
    paginator = Paginator(legislacoes_queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas por categoria
    estatisticas = {
        'total': Legislacao.objects.filter(ativo=True).count(),
        'por_esfera': {},
        'por_tipo': {},
        'por_area': {},
        'por_relevancia': {},
    }
    
    for esfera_code, esfera_name in Legislacao.ESFERA_CHOICES:
        count = Legislacao.objects.filter(ativo=True, esfera=esfera_code).count()
        estatisticas['por_esfera'][esfera_code] = {'name': esfera_name, 'count': count}
    
    for tipo_code, tipo_name in Legislacao.TIPO_CHOICES:
        count = Legislacao.objects.filter(ativo=True, tipo=tipo_code).count()
        if count > 0:
            estatisticas['por_tipo'][tipo_code] = {'name': tipo_name, 'count': count}
    
    for area_code, area_name in Legislacao.AREA_CHOICES:
        count = Legislacao.objects.filter(ativo=True, area=area_code).count()
        if count > 0:
            estatisticas['por_area'][area_code] = {'name': area_name, 'count': count}
    
    for relevancia in [1, 2, 3, 4, 5]:
        count = Legislacao.objects.filter(ativo=True, relevancia=relevancia).count()
        if count > 0:
            relevancia_names = {1: 'Baixa', 2: 'Média', 3: 'Alta', 4: 'Crítica', 5: 'Essencial'}
            estatisticas['por_relevancia'][relevancia] = {
                'name': relevancia_names.get(relevancia, f'Nível {relevancia}'),
                'count': count
            }
    
    # Opções para os filtros
    opcoes_filtros = {
        'esferas': Legislacao.ESFERA_CHOICES,
        'tipos': [(t, n) for t, n in Legislacao.TIPO_CHOICES if Legislacao.objects.filter(ativo=True, tipo=t).exists()],
        'areas': [(a, n) for a, n in Legislacao.AREA_CHOICES if Legislacao.objects.filter(ativo=True, area=a).exists()],
        'orgaos': [(o, n) for o, n in Legislacao.ORGAO_CHOICES if Legislacao.objects.filter(ativo=True, orgao=o).exists()],
        'relevancias': [(r, n) for r, n in [(1, 'Baixa'), (2, 'Média'), (3, 'Alta'), (4, 'Crítica'), (5, 'Essencial')] if Legislacao.objects.filter(ativo=True, relevancia=r).exists()],
        'ordenacoes': [
            ('-data_publicacao', 'Data de Publicação (Mais Recente)'),
            ('data_publicacao', 'Data de Publicação (Mais Antiga)'),
            ('-relevancia', 'Relevância (Maior)'),
            ('relevancia', 'Relevância (Menor)'),
            ('titulo', 'Título (A-Z)'),
            ('-titulo', 'Título (Z-A)'),
        ]
    }
    
    context = {
        'page_obj': page_obj,
        'estatisticas': estatisticas,
        'opcoes_filtros': opcoes_filtros,
        'filtros_ativos': {
            'esfera': esfera_filtro,
            'tipo': tipo_filtro,
            'area': area_filtro,
            'orgao': orgao_filtro,
            'relevancia': relevancia_filtro,
            'busca': busca,
            'ordenacao': ordenacao,
        },
        'total_resultados': paginator.count,
    }
    
    return render(request, 'auditoria/legislacoes.html', context)

def detalhes_legislacao(request, legislacao_id):
    """View para exibir detalhes de uma legislação específica"""
    legislacao = get_object_or_404(
        Legislacao.objects.prefetch_related('legislacao_relacionada'), 
        id=legislacao_id
    )
    
    # Legislações relacionadas
    relacionadas = legislacao.legislacao_relacionada.filter(ativo=True)[:5]
    
    # Legislações similares (mesma área e tipo)
    similares = Legislacao.objects.filter(
        area=legislacao.area,
        tipo=legislacao.tipo,
        ativo=True
    ).exclude(id=legislacao.id)[:5]
    
    context = {
        'legislacao': legislacao,
        'relacionadas': relacionadas,
        'similares': similares,
    }
    
    return render(request, 'auditoria/detalhes_legislacao.html', context)

def detalhes_auditoria(request, empresa_id):
    empresa = get_object_or_404(
        Empresa.objects.prefetch_related('documentos_fiscais', 'notas_fiscais'), 
        id=empresa_id
    )
    resultado_auditoria = empresa.resultado_auditoria if empresa.resultado_auditoria else None
    resultado_ia = empresa.resultado_ia if empresa.resultado_ia else None

    # Edição inline dos dados da empresa
    if request.method == 'POST' and 'edit_empresa' in request.POST:
        empresa.razao_social = request.POST.get('razao_social', empresa.razao_social)
        empresa.cnpj = request.POST.get('cnpj', empresa.cnpj)
        empresa.regime_tributario = request.POST.get('regime_tributario', empresa.regime_tributario)
        empresa.save()

    # Upload individual de documento fiscal
    if request.method == 'POST' and 'upload_btn' in request.POST:
        tipo_doc = request.POST.get('tipo_documento')
        mes_doc = request.POST.get('mes')
        ano_doc = request.POST.get('ano')
        arquivo_doc = request.FILES.get('arquivo')
        if tipo_doc and mes_doc and ano_doc and arquivo_doc:
            try:
                DocumentoFiscal.objects.update_or_create(
                    empresa=empresa,
                    tipo_documento=tipo_doc,
                    mes=int(mes_doc),
                    ano=int(ano_doc),
                    defaults={'arquivo': arquivo_doc}
                )
                return redirect('detalhes_auditoria', empresa_id=empresa.id)
            except Exception as e:
                pass # Tratar erro de forma mais robusta

    # Análise de auditoria somente quando solicitado
    if request.method == 'POST' and 'analisar_empresa' in request.POST:
        resultado_auditoria = auditar_pis_cofins_monofasico(empresa_id)
        # --- DeepSeek API com integração TIPI ---
        docs = DocumentoFiscal.objects.filter(empresa=empresa)
        documentos_texto = []
        for doc in docs:
            texto = ''
            if doc.arquivo and doc.arquivo.name:
                caminho = doc.arquivo.path
                if caminho.lower().endswith('.pdf'):
                    try:
                        with open(caminho, 'rb') as f:
                            reader = PyPDF2.PdfReader(f)
                            texto = '\n'.join(page.extract_text() or '' for page in reader.pages)
                    except Exception as e:
                        texto = f'[Erro ao extrair texto do PDF: {e}]'
                elif caminho.lower().endswith('.xml'):
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            texto = f.read()
                    except Exception as e:
                        texto = f'[Erro ao ler XML: {e}]'
                elif caminho.lower().endswith('.txt'):
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            texto = f.read()
                    except Exception as e:
                        texto = f'[Erro ao ler TXT: {e}]'
                else:
                    texto = '[Tipo de arquivo não suportado para extração de texto]'
                if texto:
                    pass  # Não limitar o tamanho do texto enviado para a IA
                documentos_texto.append(f"{doc.get_tipo_documento_display()} - {doc.get_mes_display()}/{doc.ano} - Conteúdo:\n{texto}")
        
        # Gerar contexto TIPI para a IA
        contexto_tipi = gerar_contexto_tipi_para_ia(empresa_id)
        
        # Realizar auditoria de IPI com TIPI
        auditoria_ipi = auditar_ipi_com_tipi(empresa_id)
        
        # Montar prompt enriquecido com dados da TIPI
        prompt_tipi = ""
        if contexto_tipi['produtos_identificados']:
            prompt_tipi = f"\n\nDADOS DA TABELA TIPI IDENTIFICADOS:\n"
            prompt_tipi += f"Total de registros TIPI disponíveis: {contexto_tipi['total_registros_tipi']}\n"
            prompt_tipi += "Produtos identificados nos documentos:\n"
            for produto in contexto_tipi['produtos_identificados']:
                prompt_tipi += f"- NCM {produto['codigo_ncm']}: {produto['descricao']} - IPI: {produto['aliquota_ipi']}%\n"
                if produto['observacoes']:
                    prompt_tipi += f"  Observações: {produto['observacoes']}\n"
        
        if auditoria_ipi['detalhes_notas_ipi']:
            prompt_tipi += f"\n\nAUDITORIA DE IPI DETECTADA:\n"
            prompt_tipi += f"Potencial de recuperação IPI: R$ {auditoria_ipi['total_potencial_recuperacao_ipi']}\n"
            for nota in auditoria_ipi['detalhes_notas_ipi']:
                prompt_tipi += f"- Nota {nota['numero']}: NCM {nota['codigo_ncm']} - Diferença: R$ {nota['diferenca']}\n"
        
        prompt = f"Audite os documentos fiscais abaixo e aponte possíveis valores pagos de forma errada ao governo, considerando os últimos 5 anos. Liste inconsistências e explique o motivo.\n\nEmpresa: {empresa.razao_social} - Regime: {empresa.regime_tributario}\n\nDocumentos:\n" + "\n\n".join(documentos_texto) + prompt_tipi
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "Você é um auditor fiscal especialista em tributos brasileiros."},
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=120
            )
            if response.status_code == 200:
                resultado_ia = response.json()["choices"][0]["message"]["content"]
            else:
                resultado_ia = f"Erro na análise IA: {response.status_code} - {response.text}"
        except Exception as e:
            resultado_ia = f"Erro ao conectar à IA: {e}"

    # Gerar lista de documentos esperados para os últimos 5 anos
    documentos_por_tipo_e_periodo = {}
    anos_para_exibir = list(range(2021, 2026)) # De 2021 até 2025 (últimos 5 anos completos até o momento)
    meses = DocumentoFiscal.MES_CHOICES

    # Otimizar consulta de documentos existentes
    documentos_existentes = DocumentoFiscal.objects.filter(
        empresa=empresa, 
        ano__in=anos_para_exibir
    ).select_related('empresa')

    documentos_map = {(doc.tipo_documento, doc.mes, doc.ano): doc for doc in documentos_existentes}

    for tipo_doc_choice_val, tipo_doc_choice_label in DocumentoFiscal.TIPO_DOCUMENTO_CHOICES:
        documentos_por_tipo_e_periodo[tipo_doc_choice_val] = {}
        for ano in anos_para_exibir:
            documentos_por_tipo_e_periodo[tipo_doc_choice_val][ano] = {}
            for mes_val, mes_label in meses:
                key = (tipo_doc_choice_val, mes_val, ano)
                documento_ja_enviado = documentos_map.get(key)
                documentos_por_tipo_e_periodo[tipo_doc_choice_val][ano][mes_val] = {
                    'label': mes_label,
                    'uploaded': documento_ja_enviado is not None,
                    'file_url': documento_ja_enviado.arquivo.url if documento_ja_enviado else None,
                    'documento_id': documento_ja_enviado.id if documento_ja_enviado else None
                }

    context = {
        'empresa': empresa,
        'resultado_auditoria': resultado_auditoria,
        'resultado_ia': resultado_ia,
        'documentos_por_tipo_e_periodo': documentos_por_tipo_e_periodo,
        'tipos_documento': DocumentoFiscal.TIPO_DOCUMENTO_CHOICES,
        'anos_para_exibir': anos_para_exibir,
        'meses': meses,
    }
    return render(request, 'auditoria/detalhes_auditoria.html', context)

# NOVA VIEW: Página de Upload de Documentos
def upload_documentos(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)

    if request.method == 'POST':
        # Recupera os dados do POST para o upload específico
        tipo_doc = request.POST.get('tipo_documento')
        mes_doc = request.POST.get('mes')
        ano_doc = request.POST.get('ano')
        arquivo_doc = request.FILES.get('arquivo')

        if tipo_doc and mes_doc and ano_doc and arquivo_doc:
            try:
                documento, created = DocumentoFiscal.objects.update_or_create(
                    empresa=empresa,
                    tipo_documento=tipo_doc,
                    mes=int(mes_doc),
                    ano=int(ano_doc),
                    defaults={'arquivo': arquivo_doc}
                )
                messages.success(request, f'Documento {documento.get_tipo_documento_display()} de {documento.get_mes_display()}/{documento.ano} enviado com sucesso!')
                return redirect('upload_documentos', empresa_id=empresa.id)
            except ValueError as e:
                messages.error(request, f'Erro nos dados fornecidos: {str(e)}')
            except Exception as e:
                messages.error(request, f'Erro ao fazer upload do documento: {str(e)}')
        else:
            messages.error(request, 'Todos os campos são obrigatórios para o upload.')

    # Gerar lista de documentos esperados para os últimos 5 anos
    documentos_por_tipo_e_periodo = {}
    anos_para_exibir = list(range(2021, 2026)) # De 2021 até 2025 (últimos 5 anos completos até o momento)
    meses = DocumentoFiscal.MES_CHOICES

    # Otimizar consulta de documentos existentes
    documentos_existentes = DocumentoFiscal.objects.filter(
        empresa=empresa, 
        ano__in=anos_para_exibir
    ).select_related('empresa')

    documentos_map = {(doc.tipo_documento, doc.mes, doc.ano): doc for doc in documentos_existentes}

    for tipo_doc_choice_val, tipo_doc_choice_label in DocumentoFiscal.TIPO_DOCUMENTO_CHOICES:
        documentos_por_tipo_e_periodo[tipo_doc_choice_val] = {}
        for ano in anos_para_exibir:
            documentos_por_tipo_e_periodo[tipo_doc_choice_val][ano] = {}
            for mes_val, mes_label in meses:
                key = (tipo_doc_choice_val, mes_val, ano)
                documento_ja_enviado = documentos_map.get(key)
                documentos_por_tipo_e_periodo[tipo_doc_choice_val][ano][mes_val] = {
                    'label': mes_label,
                    'uploaded': documento_ja_enviado is not None,
                    'file_url': documento_ja_enviado.arquivo.url if documento_ja_enviado else None,
                    'documento_id': documento_ja_enviado.id if documento_ja_enviado else None
                }

    context = {
        'empresa': empresa,
        'documentos_por_tipo_e_periodo': documentos_por_tipo_e_periodo,
        'tipos_documento': DocumentoFiscal.TIPO_DOCUMENTO_CHOICES,
        'anos_para_exibir': anos_para_exibir,
        'meses': meses,
    }
    return render(request, 'auditoria/upload_documentos.html', context)

def analisar_empresa_ajax(request, empresa_id):
    import os
    empresa = get_object_or_404(Empresa, id=empresa_id)
    docs = DocumentoFiscal.objects.filter(empresa=empresa)
    total_docs = docs.count()
    sess_key = f"analise_progresso_{empresa_id}"
    # Inicializa progresso se não existir
    if sess_key not in request.session or request.GET.get('reset') == '1':
        request.session[sess_key] = {
            'idx': 0,
            'resultados_parciais': [],
            'total_recuperar': 0,
            'documentos_texto': [],
        }
    progresso = request.session[sess_key]
    idx = progresso['idx']
    resultados_parciais = progresso['resultados_parciais']
    total_recuperar = progresso['total_recuperar']
    documentos_texto = progresso.get('documentos_texto', [])
    if idx < total_docs:
        doc = docs[idx]
        nome_arquivo = os.path.basename(doc.arquivo.name) if doc.arquivo else 'Sem arquivo'
        texto = ''
        if doc.arquivo and doc.arquivo.name:
            caminho = doc.arquivo.path
            if caminho.lower().endswith('.pdf'):
                try:
                    with open(caminho, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        texto = '\n'.join(page.extract_text() or '' for page in reader.pages)
                except Exception as e:
                    texto = f'[Erro ao extrair texto do PDF: {e}]'
            elif caminho.lower().endswith('.xml'):
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        texto = f.read()
                except Exception as e:
                    texto = f'[Erro ao ler XML: {e}]'
            elif caminho.lower().endswith('.txt'):
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        texto = f.read()
                except Exception as e:
                    texto = f'[Erro ao ler TXT: {e}]'
            else:
                texto = '[Tipo de arquivo não suportado para extração de texto]'
        # Adiciona texto para análise IA
        documentos_texto.append(f"{doc.get_tipo_documento_display()} - {doc.get_mes_display()}/{doc.ano} - Conteúdo:\n{texto}")
        # Aqui você pode rodar uma análise real por documento, se desejar
        # valor_encontrado = sua_funcao_de_auditoria(texto)
        valor_encontrado = 0  # Deixe 0 aqui, pois a análise real será feita ao final
        total_recuperar += valor_encontrado
        resultados_parciais.append({
            'arquivo': nome_arquivo,
            'valor': valor_encontrado,
            'total_parcial': total_recuperar
        })
        idx += 1
        # Salva progresso na sessão
        request.session[sess_key] = {
            'idx': idx,
            'resultados_parciais': resultados_parciais,
            'total_recuperar': total_recuperar,
            'documentos_texto': documentos_texto,
        }
        progresso_percent = int((idx / total_docs) * 100)
        return JsonResponse({
            'progresso': progresso_percent,
            'arquivo_atual': nome_arquivo,
            'valor_atual': valor_encontrado,
            'total_parcial': total_recuperar,
            'finalizado': False,
            'resultados_parciais': resultados_parciais
        })
    else:
        # Ao final, roda a análise real e a IA
        from .logica_auditoria import auditar_pis_cofins_monofasico
        resultado_auditoria = auditar_pis_cofins_monofasico(empresa_id)
        total_potencial = 0
        if resultado_auditoria and isinstance(resultado_auditoria, dict):
            total_potencial = resultado_auditoria.get('total_potencial_recuperacao', 0)
        # Chama a IA DeepSeek
        resultado_ia = None
        try:
            import requests
            from django.conf import settings
            
            # Verificar se a chave da API está configurada
            api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
            if not api_key or api_key == 'sk-demo-key-for-testing':
                # Resposta de demonstração quando a API não está configurada
                resultado_ia = f"""
# 📋 Análise Fiscal - Empresa: {empresa.razao_social}

## ⚠️ **Modo Demonstração**
Esta é uma análise simulada pois a chave da API DeepSeek não está configurada.

## 🔍 **Análise dos Documentos Fiscais**

### **Possíveis Inconsistências Identificadas:**

#### 1. **PIS/COFINS - Regime de Apuração**
- **Valor estimado de recuperação**: R$ 15.750,00
- **Motivo**: Possível pagamento indevido de PIS/COFINS no regime cumulativo quando poderia ser não-cumulativo
- **Base legal**: Lei 10.833/2003

#### 2. **IPI - Classificação Fiscal**
- **Valor estimado de recuperação**: R$ 8.200,00
- **Motivo**: Possível aplicação de alíquota incorreta baseada na classificação NCM
- **Base legal**: Tabela TIPI 2024

#### 3. **ICMS - Créditos Não Aproveitados**
- **Valor estimado de recuperação**: R$ 12.300,00
- **Motivo**: Créditos de ICMS nas aquisições que podem não ter sido aproveitados adequadamente
- **Base legal**: Lei Complementar 87/96

### **💰 Total Estimado de Recuperação: R$ 36.250,00**

### **📋 Próximos Passos Recomendados:**
1. Análise detalhada dos documentos por especialista
2. Verificação da classificação fiscal dos produtos
3. Revisão do regime de apuração do PIS/COFINS
4. Análise dos créditos de ICMS disponíveis

---

**Para usar a análise real com IA, configure sua chave da API DeepSeek no arquivo .env**
"""
                return JsonResponse({
                    'progresso': 100,
                    'finalizado': True,
                    'total_recuperar': 36250.00,
                    'resultados_parciais': resultados_parciais,
                    'relatorio': f"Total recuperável (simulado): R$ 36.250,00",
                    'resultado_ia': resultado_ia,
                    'resultado_auditoria': resultado_auditoria,
                    'valor_ia_recuperacao': 36250.00,
                })
            
            # Se a chave está configurada, fazer a chamada real
            contexto_empresa = gerar_contexto_empresa_detalhado(empresa)
            prompt = f"""Audite os documentos fiscais abaixo e aponte possíveis valores pagos de forma errada ao governo, considerando os últimos 5 anos. 
            
Com base nas informações da empresa, identifique oportunidades específicas de recuperação fiscal.

{contexto_empresa}

Documentos para análise:
{"\n\n".join(documentos_texto)}

Instruções:
1. Considere o regime tributário e setor da empresa
2. Identifique oportunidades baseadas nas características específicas da empresa
3. Aponte inconsistências e explique o motivo
4. Sugira valores estimados de recuperação quando possível
5. Priorize oportunidades com maior potencial de recuperação
"""
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "Você é um auditor fiscal especialista em tributos brasileiros."},
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=120
            )
            if response.status_code == 200:
                resultado_ia = response.json()["choices"][0]["message"]["content"]
            else:
                resultado_ia = f"Erro na análise IA: {response.status_code} - {response.text}"
        except Exception as e:
            resultado_ia = f"Erro ao conectar à IA: {e}"
        # Salva resultados na empresa
        empresa.resultado_auditoria = resultado_auditoria
        empresa.resultado_ia = resultado_ia
        empresa.save(update_fields=["resultado_auditoria", "resultado_ia"])
        # Extrai valor sugerido pela IA (R$) usando regex
        valor_ia_recuperacao = None
        if resultado_ia:
            match = re.search(r"R\$\s*([\d\.]+,[\d]{2})", resultado_ia)
            if match:
                valor_str = match.group(1).replace('.', '').replace(',', '.')
                try:
                    valor_ia_recuperacao = float(valor_str)
                except Exception:
                    valor_ia_recuperacao = None
        # Limpa progresso ao finalizar
        request.session.pop(sess_key, None)
        return JsonResponse({
            'progresso': 100,
            'finalizado': True,
            'total_recuperar': total_potencial,
            'resultados_parciais': resultados_parciais,
            'relatorio': f"Total recuperável: R$ {total_potencial:.2f}",
            'resultado_ia': resultado_ia,
            'resultado_auditoria': resultado_auditoria,
            'valor_ia_recuperacao': valor_ia_recuperacao,
        })



# auditoria/views.py
# ...
from .logica_auditoria import auditar_pis_cofins_monofasico # Linha 9 ou próxima
# ...

def gerar_pdf_analise(request, empresa_id):
    """Gera PDF da análise fiscal da empresa"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    # Criar buffer de memória para o PDF
    buffer = io.BytesIO()
    
    # Criar documento PDF
    pdf_doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Preparar estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#764ba2')
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50')
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    ))
    
    # Conteúdo do PDF
    story = []
    
    # Título
    story.append(Paragraph("📋 RELATÓRIO DE ANÁLISE FISCAL", styles['CustomTitle']))
    story.append(Spacer(1, 20))
    
    # Informações da empresa
    empresa_info = f"""
    <b>Empresa:</b> {empresa.razao_social}<br/>
    <b>CNPJ:</b> {empresa.cnpj}<br/>
    <b>Regime Tributário:</b> {empresa.get_regime_tributario_display()}<br/>
    <b>Data da Análise:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}<br/>
    """
    story.append(Paragraph(empresa_info, styles['CustomBody']))
    story.append(Spacer(1, 20))
    
    # Resultado da análise
    story.append(Paragraph("🔍 ANÁLISE DETALHADA", styles['CustomHeading']))
    
    if empresa.resultado_ia:
        try:
            # Limpar e preparar o texto da análise para PDF
            import re
            texto_analise = str(empresa.resultado_ia)
            
            # Remover caracteres problemáticos mas manter a formatação
            texto_analise = texto_analise.replace('"', "'")
            texto_analise = texto_analise.replace('&', 'e')
            texto_analise = re.sub(r'[{}[\]<>]', '', texto_analise)
            
            # Dividir em seções por quebras de linha duplas
            secoes = texto_analise.split('\n\n')
            
            for secao in secoes:
                if secao.strip():
                    # Verificar se é um título (começa com #)
                    if secao.strip().startswith('#'):
                        titulo = secao.replace('#', '').strip()
                        if titulo:
                            story.append(Paragraph(titulo, styles['CustomHeading']))
                    else:
                        # Texto normal - dividir em parágrafos menores se muito longo
                        linhas = secao.split('\n')
                        paragrafo_atual = ""
                        
                        for linha in linhas:
                            if linha.strip():
                                paragrafo_atual += linha + " "
                                # Se o parágrafo ficar muito longo, criar um novo
                                if len(paragrafo_atual) > 800:
                                    story.append(Paragraph(paragrafo_atual.strip(), styles['CustomBody']))
                                    story.append(Spacer(1, 6))
                                    paragrafo_atual = ""
                        
                        # Adicionar o último parágrafo se houver
                        if paragrafo_atual.strip():
                            story.append(Paragraph(paragrafo_atual.strip(), styles['CustomBody']))
                    
                    story.append(Spacer(1, 10))
                    
        except Exception as e:
            # Em caso de erro, mostrar mensagem informativa
            story.append(Paragraph("Erro ao processar o texto da análise para PDF.", styles['CustomBody']))
            story.append(Paragraph("A análise completa está disponível na interface web do sistema.", styles['CustomBody']))
    else:
        story.append(Paragraph("Nenhuma análise foi realizada para esta empresa ainda.", styles['CustomBody']))
        story.append(Paragraph("Execute uma análise na interface web para gerar o relatório completo.", styles['CustomBody']))
    
    story.append(Spacer(1, 30))
    
    # Rodapé
    rodape = f"""
    <br/><br/>
    <i>Relatório gerado pelo Sistema Fisco - Auditoria Fiscal Inteligente<br/>
    Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</i>
    """
    story.append(Paragraph(rodape, styles['CustomBody']))
    
    # Gerar PDF
    pdf_doc.build(story)
    
    # Retornar resposta HTTP
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="analise_fiscal_{empresa.cnpj.replace(".", "").replace("/", "").replace("-", "")}_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    
    return response

def excluir_empresa(request, empresa_id):
    """Exclui uma empresa e todos os seus dados relacionados"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        razao_social = empresa.razao_social
        # Excluir empresa (cascata exclui documentos relacionados)
        empresa.delete()
        messages.success(request, f'Empresa "{razao_social}" foi excluída com sucesso.')
        return redirect('auditoria:lista_empresas')
    
    # Se não for POST, redirecionar para detalhes
    return redirect('auditoria:detalhes_auditoria', empresa_id=empresa_id)

def gerar_contexto_empresa_detalhado(empresa):
    """Gera contexto detalhado da empresa para análise da IA"""
    contexto = f"""
INFORMAÇÕES DETALHADAS DA EMPRESA:

Dados Básicos:
- Razão Social: {empresa.razao_social}
- CNPJ: {empresa.cnpj}
- Regime Tributário: {empresa.get_regime_tributario_display()}
"""
    
    # Adicionar informações apenas se preenchidas
    if empresa.atividade_principal:
        contexto += f"- Atividade Principal: {empresa.atividade_principal}\n"
    
    if empresa.cnae_principal:
        contexto += f"- CNAE Principal: {empresa.cnae_principal}\n"
    
    if empresa.setor_atuacao:
        contexto += f"- Setor de Atuação: {empresa.get_setor_atuacao_display()}\n"
    
    if empresa.principais_ncm:
        contexto += f"- Principais NCM: {empresa.principais_ncm}\n"
    
    if empresa.produtos_principais:
        contexto += f"- Principais Produtos: {empresa.produtos_principais}\n"
    
    if empresa.faturamento_anual:
        contexto += f"- Faturamento Anual: {empresa.get_faturamento_anual_display()}\n"
    
    if empresa.numero_funcionarios:
        contexto += f"- Número de Funcionários: {empresa.get_numero_funcionarios_display()}\n"
    
    if empresa.regime_apuracao:
        contexto += f"- Regime de Apuração: {empresa.get_regime_apuracao_display()}\n"
    
    # Características operacionais
    if empresa.estados_operacao:
        contexto += f"- Estados de Operação: {empresa.estados_operacao}\n"
    
    if empresa.tem_filiais:
        contexto += "- Possui filiais\n"
    
    if empresa.exporta:
        contexto += "- Realiza exportações\n"
    
    if empresa.importa:
        contexto += "- Realiza importações\n"
    
    # Benefícios fiscais
    if empresa.tem_beneficios_fiscais:
        contexto += "- Possui benefícios fiscais"
        if empresa.quais_beneficios:
            contexto += f": {empresa.quais_beneficios}\n"
        else:
            contexto += "\n"
    
    # Gastos especiais
    gastos_especiais = []
    if empresa.tem_gastos_pd:
        gastos_especiais.append("Pesquisa e Desenvolvimento")
    if empresa.tem_gastos_treinamento:
        gastos_especiais.append("Treinamento de funcionários")
    if empresa.tem_gastos_ambientais:
        gastos_especiais.append("Preservação ambiental")
    
    if gastos_especiais:
        contexto += f"- Gastos Especiais: {', '.join(gastos_especiais)}\n"
    
    # Tipos de contratação
    if empresa.usa_pj:
        contexto += "- Contrata Pessoa Jurídica (PJ)\n"
    
    if empresa.usa_terceirizacao:
        contexto += "- Utiliza serviços terceirizados\n"
    
    # Observações
    if empresa.observacoes_fiscais:
        contexto += f"- Observações Fiscais: {empresa.observacoes_fiscais}\n"
    
    # Localização da empresa
    if empresa.cidade or empresa.estado or empresa.uf:
        contexto += "\nLocalização da Empresa:\n"
        if empresa.cidade:
            contexto += f"- Cidade: {empresa.cidade}\n"
        if empresa.estado:
            contexto += f"- Estado: {empresa.estado}\n"
        if empresa.uf:
            contexto += f"- UF: {empresa.uf}\n"
        if empresa.cep:
            contexto += f"- CEP: {empresa.cep}\n"
    
    # Buscar legislações específicas por localização
    legislacoes_locais = obter_legislacoes_por_localizacao(empresa)
    if legislacoes_locais.exists():
        contexto += "\n🏛️ LEGISLAÇÕES ESPECÍFICAS POR LOCALIZAÇÃO:\n"
        contexto += f"Total de legislações aplicáveis: {legislacoes_locais.count()}\n"
        
        # Contar por esfera
        federais = legislacoes_locais.filter(esfera='FEDERAL').count()
        estaduais = legislacoes_locais.filter(esfera='ESTADUAL').count()
        municipais = legislacoes_locais.filter(esfera='MUNICIPAL').count()
        
        contexto += f"- Federais: {federais}\n"
        if empresa.uf:
            contexto += f"- Estaduais ({empresa.uf}): {estaduais}\n"
        if empresa.cidade:
            contexto += f"- Municipais ({empresa.cidade}): {municipais}\n"
        
        # Destacar as mais relevantes
        contexto += "\nLegislações mais relevantes:\n"
        legislacoes_relevantes = legislacoes_locais.filter(relevancia__gte=4)[:10]
        for leg in legislacoes_relevantes:
            contexto += f"- {leg.get_identificacao()} ({leg.get_esfera_display()}): {leg.titulo[:100]}...\n"
            if leg.resumo:
                contexto += f"  Resumo: {leg.resumo[:150]}...\n"
    
    contexto += """
OPORTUNIDADES DE RECUPERAÇÃO SUGERIDAS BASEADAS NO PERFIL:

Com base no perfil da empresa, considere especialmente:
"""
    
    # Sugestões baseadas no regime tributário
    if empresa.regime_tributario == 'SIMPLES':
        contexto += "- Verificar se há recolhimentos indevidos de tributos já inclusos no Simples Nacional\n"
        contexto += "- Analisar possibilidade de exclusão retroativa do Simples se benéfico\n"
    elif empresa.regime_tributario == 'PRESUMIDO':
        contexto += "- Verificar se há base de cálculo superior ao presumido em alguns períodos\n"
        contexto += "- Analisar créditos de PIS/COFINS não aproveitados\n"
    elif empresa.regime_tributario == 'REAL':
        contexto += "- Verificar aproveitamento integral de créditos de PIS/COFINS\n"
        contexto += "- Analisar créditos de ICMS não aproveitados\n"
    
    # Sugestões baseadas no setor
    if empresa.setor_atuacao == 'INDUSTRIA':
        contexto += "- Verificar créditos de IPI na aquisição de matérias-primas\n"
        contexto += "- Analisar aproveitamento de créditos presumidos\n"
    elif empresa.setor_atuacao == 'TECNOLOGIA':
        contexto += "- Verificar incentivos fiscais para inovação tecnológica\n"
        contexto += "- Analisar benefícios da Lei de Informática\n"
    
    # Sugestões baseadas em gastos especiais
    if empresa.tem_gastos_pd:
        contexto += "- Verificar incentivos fiscais para P&D (Lei do Bem)\n"
    
    if empresa.exporta:
        contexto += "- Verificar imunidade de PIS/COFINS sobre exportações\n"
        contexto += "- Analisar créditos presumidos de IPI\n"
    
    if empresa.importa:
        contexto += "- Verificar aproveitamento de créditos na importação\n"
        contexto += "- Analisar regimes especiais de importação\n"
    
    # Adicionar dados TIPI específicos baseados nos NCMs da empresa
    if empresa.principais_ncm:
        contexto += "\n📊 DADOS TIPI ESPECÍFICOS DA EMPRESA:\n"
        contexto += f"Total de registros na tabela TIPI: {TabelaTIPI.objects.count()}\n"
        
        # Extrair códigos NCM da empresa
        ncm_codes = [ncm.strip() for ncm in empresa.principais_ncm.split(',') if ncm.strip()]
        
        for ncm in ncm_codes:
            # Buscar na tabela TIPI
            tipi_item = TabelaTIPI.objects.filter(codigo_ncm=ncm, ativo=True).first()
            if tipi_item:
                contexto += f"- NCM {ncm}: {tipi_item.descricao}\n"
                contexto += f"  Alíquota IPI: {tipi_item.aliquota_ipi}%\n"
                if tipi_item.observacoes:
                    contexto += f"  Observações: {tipi_item.observacoes}\n"
                
                # Sugestões específicas baseadas na alíquota
                if tipi_item.aliquota_ipi == 0:
                    contexto += "  ⚠️  Produto isento de IPI - verificar se não há cobrança indevida\n"
                elif tipi_item.aliquota_ipi > 0:
                    contexto += f"  💡 Produto tributado - verificar se IPI de {tipi_item.aliquota_ipi}% está sendo aplicado corretamente\n"
                
                contexto += "\n"
            else:
                contexto += f"- NCM {ncm}: Não encontrado na tabela TIPI atual\n"
                contexto += "  ⚠️  Verificar se o código NCM está correto\n\n"
    
    return contexto

def obter_legislacoes_por_localizacao(empresa):
    """
    Busca legislações específicas baseadas na localização da empresa.
    Inclui legislações federais, estaduais do estado da empresa e municipais da cidade.
    """
    from .models import Legislacao
    
    # Sempre incluir legislações federais
    legislacoes_relevantes = Legislacao.objects.filter(
        ativo=True,
        esfera='FEDERAL'
    ).order_by('-relevancia', '-data_publicacao')
    
    # Legislações estaduais específicas
    if empresa.uf:
        legislacoes_estaduais = Legislacao.objects.filter(
            ativo=True,
            esfera='ESTADUAL',
            uf_especifica=empresa.uf
        ).order_by('-relevancia', '-data_publicacao')
        
        # Também incluir legislações estaduais genéricas (sem UF específica)
        legislacoes_estaduais_genericas = Legislacao.objects.filter(
            ativo=True,
            esfera='ESTADUAL',
            uf_especifica__isnull=True
        ).order_by('-relevancia', '-data_publicacao')
        
        legislacoes_relevantes = legislacoes_relevantes.union(
            legislacoes_estaduais, 
            legislacoes_estaduais_genericas
        )
    
    # Legislações municipais específicas
    if empresa.cidade and empresa.uf:
        legislacoes_municipais = Legislacao.objects.filter(
            ativo=True,
            esfera='MUNICIPAL',
            municipio_especifico__icontains=empresa.cidade,
            uf_especifica=empresa.uf
        ).order_by('-relevancia', '-data_publicacao')
        
        # Também incluir legislações municipais genéricas
        legislacoes_municipais_genericas = Legislacao.objects.filter(
            ativo=True,
            esfera='MUNICIPAL',
            municipio_especifico__isnull=True
        ).order_by('-relevancia', '-data_publicacao')
        
        legislacoes_relevantes = legislacoes_relevantes.union(
            legislacoes_municipais,
            legislacoes_municipais_genericas
        )
    
    return legislacoes_relevantes

def cadastrar_empresa(request):
    """Cadastra uma nova empresa com informações completas para análise fiscal"""
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save()
            messages.success(request, f'Empresa "{empresa.razao_social}" foi cadastrada com sucesso!')
            return redirect('auditoria:detalhes_auditoria', empresa_id=empresa.id)
        else:
            messages.error(request, 'Erro ao cadastrar empresa. Verifique os campos marcados.')
    else:
        form = EmpresaForm()
    
    return render(request, 'auditoria/cadastrar_empresa.html', {'form': form})