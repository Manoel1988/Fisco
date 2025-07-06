# auditoria/logica_auditoria.py

from .models import Empresa, NotaFiscal, TabelaTIPI
from .services.tipi_service import TIPIService
from django.db.models import Sum
import re

# Lista SIMPLIFICADA de NCMs ou descrições de produtos monofásicos para PIS/Cofins
# Na vida real, isso seria muito mais complexo e dinâmico e idealmente viria de uma base de dados.
# Para este exemplo, estamos usando descrições de produtos.
PRODUTOS_MONOFASICOS_EXEMPLO = [
    "REFRIGERANTE", "CERVEJA", "AGUA MINERAL", "MEDICAMENTO PARA USO HUMANO",
    "PNEU", "AUTOPECA", # Exemplo de descrições simplificadas
    # NCMs (Nomenclatura Comum do Mercosul) seriam mais precisos e recomendados para um sistema real:
    # Ex: '2202.10.00', '2203.00.00', '3004.90.99', etc.
]

def auditar_pis_cofins_monofasico(empresa_id):
    """
    Função de auditoria SIMPLIFICADA para identificar potencial de recuperação
    de PIS/Cofins monofásico para empresas do Simples Nacional.

    ATENÇÃO: Este é um exemplo didático. A lógica de auditoria real é complexa
    e exige análise detalhada de NCMs, CSTs, alíquotas e documentos fiscais.
    """
    empresa = Empresa.objects.get(id=empresa_id)
    
    if empresa.regime_tributario != 'SIMPLES':
        return {
            'status': 'Não Aplicável',
            'mensagem': 'A auditoria de PIS/Cofins monofásico é relevante apenas para empresas do Simples Nacional neste contexto.',
            'total_potencial_recuperacao': 0,
            'detalhes_notas': []
        }

    notas_da_empresa = NotaFiscal.objects.filter(empresa=empresa)
    
    total_valor_monofasico_indevido = 0
    notas_com_potencial = []

    for nota in notas_da_empresa:
        # Simplificação: Verifica se a descrição de algum produto na nota contém termos monofásicos
        # Em um sistema real, você analisaria os ITENS da nota fiscal (se importados)
        # e seus respectivos NCMs (Nomenclatura Comum do Mercosul) ou CEST.
        
        produtos_monofasicos_na_nota = False
        if nota.descricao_produtos: # Garante que a descrição não seja nula
            for termo in PRODUTOS_MONOFASICOS_EXEMPLO:
                if termo in nota.descricao_produtos.upper(): # Converte para maiúsculas para comparação
                    produtos_monofasicos_na_nota = True
                    break
        
        if produtos_monofasicos_na_nota:
            # Aqui, você estimaria o valor do PIS/Cofins pago indevidamente.
            # O cálculo real depende das tabelas do Simples Nacional e da forma como a
            # receita foi informada (e não segregada) no PGDAS.
            
            # Para fins de demonstração, vamos supor um percentual fixo de "PIS/Cofins embutido"
            # ATENÇÃO: ESTE PERCENTUAL É FICTÍCIO E APENAS PARA EXEMPLIFICAR A LÓGICA.
            # O cálculo real é muito mais complexo e depende das alíquotas efetivas do Simples.
            aliquota_pis_cofins_simples_estimada = 0.02 # Exemplo: 2% da receita bruta relacionada ao produto monofásico
            
            valor_potencial_pis_cofins_indevido = float(nota.valor_total) * aliquota_pis_cofins_simples_estimada
            total_valor_monofasico_indevido += valor_potencial_pis_cofins_indevido
            
            notas_com_potencial.append({
                'numero': nota.numero,
                'data_emissao': nota.data_emissao,
                'valor_total': nota.valor_total,
                'descricao_produtos': nota.descricao_produtos,
                'potencial_recuperacao': round(valor_potencial_pis_cofins_indevido, 2)
            })

    return {
        'status': 'Sucesso',
        'empresa': empresa.razao_social,
        'total_potencial_recuperacao': round(total_valor_monofasico_indevido, 2),
        'detalhes_notas': notas_com_potencial
    }

def auditar_ipi_com_tipi(empresa_id):
    """
    Nova função de auditoria que utiliza a tabela TIPI para análise de IPI
    """
    empresa = Empresa.objects.get(id=empresa_id)
    tipi_service = TIPIService()
    
    notas_da_empresa = NotaFiscal.objects.filter(empresa=empresa)
    
    total_valor_ipi_potencial = 0
    notas_com_potencial_ipi = []
    alertas_tipi = []

    for nota in notas_da_empresa:
        if nota.descricao_produtos:
            # Tentar extrair códigos NCM da descrição dos produtos
            codigos_ncm = extrair_codigos_ncm(nota.descricao_produtos)
            
            for codigo_ncm in codigos_ncm:
                # Consultar tabela TIPI
                item_tipi = tipi_service.consultar_tipi(codigo_ncm)
                
                if item_tipi:
                    # Verificar se há IPI aplicável
                    if item_tipi.aliquota_ipi > 0:
                        # Calcular potencial de auditoria de IPI
                        valor_ipi_calculado = float(nota.valor_total) * (item_tipi.aliquota_ipi / 100)
                        valor_ipi_declarado = float(nota.valor_icms or 0)  # Assumindo que IPI pode estar no campo ICMS
                        
                        diferenca = valor_ipi_calculado - valor_ipi_declarado
                        
                        if diferenca > 10:  # Diferença significativa
                            total_valor_ipi_potencial += diferenca
                            
                            notas_com_potencial_ipi.append({
                                'numero': nota.numero,
                                'data_emissao': nota.data_emissao,
                                'valor_total': nota.valor_total,
                                'codigo_ncm': codigo_ncm,
                                'descricao_tipi': item_tipi.descricao,
                                'aliquota_tipi': item_tipi.aliquota_ipi,
                                'ipi_calculado': round(valor_ipi_calculado, 2),
                                'ipi_declarado': round(valor_ipi_declarado, 2),
                                'diferenca': round(diferenca, 2)
                            })
                    
                    # Verificar se há observações importantes na TIPI
                    if item_tipi.observacoes and any(termo in item_tipi.observacoes.upper() for termo in ['ISENTO', 'REDUZIDA', 'SUSPENSÃO']):
                        alertas_tipi.append({
                            'codigo_ncm': codigo_ncm,
                            'descricao': item_tipi.descricao,
                            'observacoes': item_tipi.observacoes,
                            'nota': nota.numero
                        })

    return {
        'status': 'Sucesso',
        'empresa': empresa.razao_social,
        'total_potencial_recuperacao_ipi': round(total_valor_ipi_potencial, 2),
        'detalhes_notas_ipi': notas_com_potencial_ipi,
        'alertas_tipi': alertas_tipi,
        'total_alertas': len(alertas_tipi)
    }

def extrair_codigos_ncm(texto):
    """
    Extrai códigos NCM de um texto usando regex
    """
    if not texto:
        return []
    
    # Padrões comuns de NCM: 0000.00.00 ou 00000000
    padroes_ncm = [
        r'\b\d{4}\.\d{2}\.\d{2}\b',  # Formato 0000.00.00
        r'\b\d{8}\b',                # Formato 00000000
        r'\b\d{2}\.\d{2}\.\d{2}\.\d{2}\b'  # Formato 00.00.00.00
    ]
    
    codigos_encontrados = []
    
    for padrao in padroes_ncm:
        matches = re.findall(padrao, texto)
        for match in matches:
            # Normalizar formato (remover pontos)
            codigo_limpo = match.replace('.', '')
            if len(codigo_limpo) == 8:
                # Reformatar como 00.00.00.00
                codigo_formatado = f"{codigo_limpo[:2]}.{codigo_limpo[2:4]}.{codigo_limpo[4:6]}.{codigo_limpo[6:8]}"
                if codigo_formatado not in codigos_encontrados:
                    codigos_encontrados.append(codigo_formatado)
    
    return codigos_encontrados

def gerar_contexto_tipi_para_ia(empresa_id):
    """
    Gera contexto da tabela TIPI para ser usado pela IA nas análises
    """
    empresa = Empresa.objects.get(id=empresa_id)
    notas_da_empresa = NotaFiscal.objects.filter(empresa=empresa)
    
    contexto_tipi = {
        'total_registros_tipi': TabelaTIPI.objects.filter(ativo=True).count(),
        'produtos_identificados': [],
        'aliquotas_relevantes': [],
        'observacoes_importantes': []
    }
    
    for nota in notas_da_empresa:
        if nota.descricao_produtos:
            codigos_ncm = extrair_codigos_ncm(nota.descricao_produtos)
            
            for codigo_ncm in codigos_ncm:
                tipi_service = TIPIService()
                item_tipi = tipi_service.consultar_tipi(codigo_ncm)
                
                if item_tipi:
                    contexto_tipi['produtos_identificados'].append({
                        'codigo_ncm': codigo_ncm,
                        'descricao': item_tipi.descricao,
                        'aliquota_ipi': item_tipi.aliquota_ipi,
                        'observacoes': item_tipi.observacoes,
                        'decreto_origem': item_tipi.decreto_origem
                    })
                    
                    if item_tipi.aliquota_ipi not in contexto_tipi['aliquotas_relevantes']:
                        contexto_tipi['aliquotas_relevantes'].append(item_tipi.aliquota_ipi)
                    
                    if item_tipi.observacoes:
                        contexto_tipi['observacoes_importantes'].append(item_tipi.observacoes)
    
    return contexto_tipi

# Outras funções de auditoria seriam criadas aqui, como:
# def auditar_inss_aviso_previo(empresa_id):
#     # Lógica para INSS
#     pass

# def auditar_pis_cofins_credito_real(empresa_id):
#     # Lógica para créditos de PIS/Cofins no Lucro Real
#     pass