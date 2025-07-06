from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
from datetime import datetime
import requests
import PyPDF2
from time import sleep
import re
import logging

from .models import Empresa, NotaFiscal, DocumentoFiscal, TabelaTIPI, HistoricoAtualizacaoTIPI
from .logica_auditoria import auditar_pis_cofins_monofasico, gerar_contexto_tipi_para_ia, auditar_ipi_com_tipi
from .forms import DocumentoFiscalForm
from .services.tipi_pdf_extractor import TIPIPDFExtractor

logger = logging.getLogger(__name__)

# Create your views here.
# auditoria/views.py

def lista_empresas(request):
    empresas = Empresa.objects.all().order_by('razao_social')
    context = {'empresas': empresas}
    return render(request, 'auditoria/lista_empresas.html', context)

def detalhes_auditoria(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
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
    documentos_existentes = DocumentoFiscal.objects.filter(empresa=empresa, ano__in=anos_para_exibir)
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
                # Mensagem de sucesso (opcional, pode usar o sistema de mensagens do Django)
                # messages.success(request, f'Documento {documento.get_tipo_documento_display()} de {documento.get_mes_display()}/{documento.ano} enviado com sucesso!')
                return redirect('upload_documentos', empresa_id=empresa.id) # Redireciona para a mesma página
            except Exception as e:
                # Mensagem de erro
                # messages.error(request, f'Erro ao fazer upload do documento: {e}')
                pass # Tratar erro de forma mais robusta

    # Gerar lista de documentos esperados para os últimos 5 anos
    documentos_por_tipo_e_periodo = {}
    anos_para_exibir = list(range(2021, 2026)) # De 2021 até 2025 (últimos 5 anos completos até o momento)
    meses = DocumentoFiscal.MES_CHOICES

    # Recupera documentos já enviados para preencher o status
    documentos_existentes = DocumentoFiscal.objects.filter(empresa=empresa, ano__in=anos_para_exibir)
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
            prompt = f"Audite os documentos fiscais abaixo e aponte possíveis valores pagos de forma errada ao governo, considerando os últimos 5 anos. Liste inconsistências e explique o motivo.\nDocumentos:\n" + "\n\n".join(documentos_texto)
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

@login_required
def upload_tipi_pdf(request):
    """View para upload e processamento de PDF da TIPI"""
    if request.method == 'POST':
        if 'pdf_file' not in request.FILES:
            messages.error(request, 'Nenhum arquivo foi enviado.')
            return redirect('auditoria:upload_tipi_pdf')
        
        pdf_file = request.FILES['pdf_file']
        
        # Validar tipo de arquivo
        if not pdf_file.name.lower().endswith('.pdf'):
            messages.error(request, 'Apenas arquivos PDF são aceitos.')
            return redirect('auditoria:upload_tipi_pdf')
        
        # Validar tamanho (máximo 50MB)
        if pdf_file.size > 50 * 1024 * 1024:
            messages.error(request, 'Arquivo muito grande. Máximo permitido: 50MB.')
            return redirect('auditoria:upload_tipi_pdf')
        
        try:
            # Processar PDF
            extractor = TIPIPDFExtractor()
            extracted_data = extractor.extract_from_pdf(pdf_file)
            
            if not extracted_data:
                messages.warning(request, 'Nenhum dado da TIPI foi encontrado no PDF.')
                return redirect('auditoria:upload_tipi_pdf')
            
            # Importar dados para o banco
            imported_count, updated_count = import_tipi_data(extracted_data, request.user)
            
            # Registrar histórico
            HistoricoAtualizacaoTIPI.objects.create(
                usuario=request.user,
                fonte='Upload PDF',
                registros_importados=imported_count,
                registros_atualizados=updated_count,
                observacoes=f'Arquivo: {pdf_file.name}, Total extraído: {len(extracted_data)}'
            )
            
            messages.success(
                request, 
                f'Importação concluída! {imported_count} novos registros e {updated_count} atualizados.'
            )
            
        except Exception as e:
            logger.error(f"Erro ao processar PDF da TIPI: {str(e)}")
            messages.error(request, f'Erro ao processar PDF: {str(e)}')
        
        return redirect('auditoria:upload_tipi_pdf')
    
    # GET - mostrar formulário
    context = {
        'total_registros': TabelaTIPI.objects.count(),
        'ultimo_historico': HistoricoAtualizacaoTIPI.objects.order_by('-data_atualizacao').first()
    }
    
    return render(request, 'auditoria/upload_tipi_pdf.html', context)

def import_tipi_data(extracted_data, user):
    """
    Importa dados extraídos do PDF para o banco de dados
    
    Returns:
        tuple: (imported_count, updated_count)
    """
    imported_count = 0
    updated_count = 0
    
    with transaction.atomic():
        for item in extracted_data:
            try:
                codigo_ncm = item.get('codigo_ncm')
                if not codigo_ncm:
                    continue
                
                # Verificar se já existe
                existing = TabelaTIPI.objects.filter(codigo_ncm=codigo_ncm).first()
                
                if existing:
                    # Atualizar registro existente
                    existing.descricao = item.get('descricao', existing.descricao)
                    existing.aliquota_ipi = item.get('aliquota_ipi', existing.aliquota_ipi)
                    existing.observacoes = item.get('observacoes', existing.observacoes)
                    existing.decreto_origem = 'Upload PDF - ADE 008/2024'
                    existing.data_atualizacao = datetime.now()
                    existing.ativo = True
                    existing.save()
                    updated_count += 1
                    
                else:
                    # Criar novo registro
                    TabelaTIPI.objects.create(
                        codigo_ncm=codigo_ncm,
                        descricao=item.get('descricao', ''),
                        aliquota_ipi=item.get('aliquota_ipi', 0),
                        observacoes=item.get('observacoes', ''),
                        decreto_origem='Upload PDF - ADE 008/2024',
                        vigencia_inicio=datetime.now().date(),
                        ativo=True
                    )
                    imported_count += 1
                    
            except Exception as e:
                logger.error(f"Erro ao importar item {item.get('codigo_ncm')}: {str(e)}")
                continue
    
    logger.info(f"Importação concluída: {imported_count} novos, {updated_count} atualizados")
    return imported_count, updated_count

# auditoria/views.py
# ...
from .logica_auditoria import auditar_pis_cofins_monofasico # Linha 9 ou próxima
# ...