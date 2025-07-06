#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from auditoria.models import TabelaTIPI
from datetime import datetime

# Continuação dos dados TIPI - Seções III a XXI
dados_tipi_continuacao = [
    # SEÇÃO III - GORDURAS E ÓLEOS
    {'codigo_ncm': '15.01.10.00', 'descricao': 'Banha de porco', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.02.10.00', 'descricao': 'Sebo bovino', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.03.00.00', 'descricao': 'Estearina solar', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.04.10.00', 'descricao': 'Óleos de peixes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.05.00.00', 'descricao': 'Lanolina', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.06.00.00', 'descricao': 'Outras gorduras animais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.07.10.00', 'descricao': 'Óleo de soja, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.08.10.00', 'descricao': 'Óleo de amendoim, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.09.10.00', 'descricao': 'Óleo de oliva virgem', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.10.00.00', 'descricao': 'Outros óleos de oliva', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.11.10.00', 'descricao': 'Óleo de palma, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.12.11.00', 'descricao': 'Óleo de girassol, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.13.11.00', 'descricao': 'Óleo de coco, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.14.11.00', 'descricao': 'Óleo de colza, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.15.11.00', 'descricao': 'Óleo de linho, em bruto', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.16.10.00', 'descricao': 'Gorduras e óleos animais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.17.10.00', 'descricao': 'Margarina', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.18.00.11', 'descricao': 'Linoxina', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.20.00.00', 'descricao': 'Glicerina', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.21.10.00', 'descricao': 'Ceras vegetais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '15.22.00.00', 'descricao': 'Dégras', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    
    # SEÇÃO IV - PRODUTOS ALIMENTÍCIOS
    {'codigo_ncm': '16.01.00.00', 'descricao': 'Enchidos e produtos semelhantes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '16.02.10.00', 'descricao': 'Preparações homogeneizadas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '16.03.00.00', 'descricao': 'Extratos e sucos de carne', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '16.04.11.00', 'descricao': 'Salmões, preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '16.05.10.00', 'descricao': 'Caranguejos, preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '17.01.12.00', 'descricao': 'Açúcar de beterraba', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '17.01.14.00', 'descricao': 'Açúcar de cana cristal', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '17.02.11.00', 'descricao': 'Lactose', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '17.03.10.00', 'descricao': 'Melaços de cana', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '17.04.10.00', 'descricao': 'Balas, caramelos e confeitos', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.01.00.00', 'descricao': 'Cacau inteiro ou partido', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.02.00.00', 'descricao': 'Cascas de cacau', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.03.10.00', 'descricao': 'Pasta de cacau, não desengordurada', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.04.00.00', 'descricao': 'Manteiga de cacau', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.05.00.00', 'descricao': 'Cacau em pó', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '18.06.10.00', 'descricao': 'Chocolate em pó', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.01.10.00', 'descricao': 'Preparações para alimentação infantil', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.02.11.00', 'descricao': 'Massas alimentícias', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.03.00.00', 'descricao': 'Tapioca', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.04.10.00', 'descricao': 'Produtos à base de cereais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.05.10.00', 'descricao': 'Pão torrado', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '19.05.31.00', 'descricao': 'Biscoitos doces', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.01.10.00', 'descricao': 'Legumes preparados em vinagre', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.02.10.00', 'descricao': 'Tomates preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.03.10.00', 'descricao': 'Cogumelos preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.04.10.00', 'descricao': 'Batatas preparadas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.05.10.00', 'descricao': 'Outros legumes preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.06.00.00', 'descricao': 'Legumes, frutas conservados em açúcar', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.07.10.00', 'descricao': 'Preparações homogeneizadas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.08.11.00', 'descricao': 'Amendoins preparados', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.11.00', 'descricao': 'Suco de laranja', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.21.00', 'descricao': 'Suco de toranja', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.31.00', 'descricao': 'Suco de limão', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.41.00', 'descricao': 'Suco de abacaxi', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.50.00', 'descricao': 'Suco de tomate', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.61.00', 'descricao': 'Suco de uva', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.71.00', 'descricao': 'Suco de maçã', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '20.09.89.00', 'descricao': 'Outros sucos de frutas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.01.11.00', 'descricao': 'Extratos de café', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.02.10.00', 'descricao': 'Leveduras vivas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.03.10.00', 'descricao': 'Molho de soja', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.04.10.00', 'descricao': 'Preparações para sopas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.05.00.00', 'descricao': 'Sorvetes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '21.06.10.00', 'descricao': 'Concentrados de proteínas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    
    # SEÇÃO V - PRODUTOS MINERAIS
    {'codigo_ncm': '22.01.10.00', 'descricao': 'Águas minerais naturais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.02.10.00', 'descricao': 'Águas minerais gaseificadas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.03.00.00', 'descricao': 'Cerveja de malte', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.764/2023'},
    {'codigo_ncm': '22.04.10.00', 'descricao': 'Vinhos de uvas frescas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.05.10.00', 'descricao': 'Vermutes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.06.00.00', 'descricao': 'Outras bebidas fermentadas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.07.10.00', 'descricao': 'Álcool etílico não desnaturado', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.20.00', 'descricao': 'Aguardente de cana', 'aliquota_ipi': 20.00, 'observacoes': 'Alíquota alterada', 'decreto_origem': 'Decreto 11.970/2024'},
    {'codigo_ncm': '22.08.30.00', 'descricao': 'Uísques', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.40.00', 'descricao': 'Rum e outras aguardentes', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.50.00', 'descricao': 'Gim e genebra', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.60.00', 'descricao': 'Vodca', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.70.00', 'descricao': 'Licores', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.08.90.00', 'descricao': 'Outras bebidas espirituosas', 'aliquota_ipi': 20.00, 'observacoes': 'Tributação normal', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '22.09.00.00', 'descricao': 'Vinagres', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    
    # SEÇÃO VI - PRODUTOS QUÍMICOS
    {'codigo_ncm': '23.01.10.00', 'descricao': 'Farinhas de peixes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.02.10.00', 'descricao': 'Sêmeas, farelos de cereais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.03.10.00', 'descricao': 'Resíduos da fabricação de amido', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.04.00.00', 'descricao': 'Tortas de soja', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.05.00.00', 'descricao': 'Tortas de amendoim', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.06.10.00', 'descricao': 'Tortas de sementes de algodão', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.07.00.00', 'descricao': 'Borras de vinho', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.08.00.00', 'descricao': 'Matérias vegetais para alimentação animal', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '23.09.10.00', 'descricao': 'Alimentos para cães ou gatos', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    
    # SEÇÃO VII - PRODUTOS DO TABACO
    {'codigo_ncm': '24.01.10.00', 'descricao': 'Tabaco não manufaturado', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '24.02.10.00', 'descricao': 'Charutos', 'aliquota_ipi': 330.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'ADE RFB 03/2024'},
    {'codigo_ncm': '24.02.20.00', 'descricao': 'Cigarros', 'aliquota_ipi': 300.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'ADE RFB 03/2024'},
    {'codigo_ncm': '24.02.90.00', 'descricao': 'Outros cigarros de tabaco', 'aliquota_ipi': 300.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'ADE RFB 03/2024'},
    {'codigo_ncm': '24.03.11.00', 'descricao': 'Tabaco para fumar', 'aliquota_ipi': 150.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '24.03.19.00', 'descricao': 'Outros tabacos para fumar', 'aliquota_ipi': 150.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '24.03.91.00', 'descricao': 'Tabaco homogeneizado', 'aliquota_ipi': 150.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '24.03.99.00', 'descricao': 'Outros tabacos manufaturados', 'aliquota_ipi': 150.00, 'observacoes': 'Alíquota específica', 'decreto_origem': 'Decreto 11.158/2022'},
    
    # SEÇÃO VIII - PELES, COUROS E PELES COM PELO
    {'codigo_ncm': '25.01.00.00', 'descricao': 'Sal', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.02.00.00', 'descricao': 'Pirites de ferro não ustuladas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.03.00.00', 'descricao': 'Enxofre', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.04.10.00', 'descricao': 'Grafita natural', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.05.10.00', 'descricao': 'Areias naturais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.06.10.00', 'descricao': 'Quartzo', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.07.00.00', 'descricao': 'Caulim', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.08.10.00', 'descricao': 'Bentonita', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.09.10.00', 'descricao': 'Cré', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.10.10.00', 'descricao': 'Fosfatos de cálcio naturais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.11.10.00', 'descricao': 'Sulfato de bário natural', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.12.00.00', 'descricao': 'Terras de diatomácea', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.13.10.00', 'descricao': 'Pedra-pomes', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.14.00.00', 'descricao': 'Ardósia', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.15.11.00', 'descricao': 'Mármore', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.16.11.00', 'descricao': 'Granito', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.17.10.00', 'descricao': 'Seixos', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.18.10.00', 'descricao': 'Dolomita', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.19.10.00', 'descricao': 'Carbonato de magnésio natural', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.20.10.00', 'descricao': 'Gesso', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.21.00.00', 'descricao': 'Castinas', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.22.10.00', 'descricao': 'Cal viva', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.23.21.00', 'descricao': 'Cimento Portland branco', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.23.29.00', 'descricao': 'Cimento Portland comum', 'aliquota_ipi': 0.00, 'observacoes': 'Isento - Regime monofásico', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.24.10.00', 'descricao': 'Crocidolita', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.25.10.00', 'descricao': 'Mica', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.26.10.00', 'descricao': 'Esteatita natural', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.28.10.00', 'descricao': 'Boratos naturais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.29.10.00', 'descricao': 'Feldspato', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
    {'codigo_ncm': '25.30.10.00', 'descricao': 'Matérias minerais', 'aliquota_ipi': 0.00, 'observacoes': 'Isento', 'decreto_origem': 'Decreto 11.158/2022'},
]

# Inserir dados no banco
total_inseridos = 0
for item in dados_tipi_continuacao:
    obj, created = TabelaTIPI.objects.get_or_create(
        codigo_ncm=item['codigo_ncm'],
        defaults={
            'descricao': item['descricao'],
            'aliquota_ipi': item['aliquota_ipi'],
            'observacoes': item['observacoes'],
            'decreto_origem': item['decreto_origem'],
            'vigencia_inicio': datetime.now().date(),
            'ativo': True
        }
    )
    if created:
        total_inseridos += 1

print(f'Segunda parte inserida: {total_inseridos} novos registros')
print(f'Total atual: {TabelaTIPI.objects.count()} registros') 