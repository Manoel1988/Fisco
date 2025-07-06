# auditoria/logica_auditoria.py

from .models import Empresa, NotaFiscal
from django.db.models import Sum

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

# Outras funções de auditoria seriam criadas aqui, como:
# def auditar_inss_aviso_previo(empresa_id):
#     # Lógica para INSS
#     pass

# def auditar_pis_cofins_credito_real(empresa_id):
#     # Lógica para créditos de PIS/Cofins no Lucro Real
#     pass