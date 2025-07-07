import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações municipais sobre tributação e recuperação fiscal'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🏛️ Carregando legislações municipais tributárias...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # ISS - Imposto Sobre Serviços
            {
                'titulo': 'Lei Complementar 116/2003 - ISS Nacional',
                'numero': '116',
                'ano': 2003,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2003, 7, 31),
                'data_vigencia': date(2003, 7, 31),
                'ementa': 'Dispõe sobre o Imposto Sobre Serviços de Qualquer Natureza, de competência dos Municípios e do Distrito Federal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm',
                'palavras_chave': 'ISS, imposto serviços, municípios, lista serviços, restituição ISS, créditos municipais',
                'relevancia': 5,
                'resumo': 'Lei nacional do ISS que estabelece regras gerais para todos os municípios, incluindo lista de serviços e limites de alíquotas.'
            },
            # IPTU - Imposto Predial e Territorial Urbano
            {
                'titulo': 'Constituição Federal - IPTU (Art. 156)',
                'numero': '156',
                'ano': 1988,
                'tipo': 'CONSTITUICAO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(1988, 10, 5),
                'data_vigencia': date(1988, 10, 5),
                'ementa': 'Competência municipal para instituir o Imposto sobre a Propriedade Predial e Territorial Urbana.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm',
                'palavras_chave': 'IPTU, propriedade predial, territorial urbana, progressividade, restituição IPTU',
                'relevancia': 5,
                'resumo': 'Base constitucional do IPTU, estabelece competência municipal e princípios gerais de tributação imobiliária.'
            },
            # ITBI - Imposto de Transmissão de Bens Imóveis
            {
                'titulo': 'Constituição Federal - ITBI (Art. 156)',
                'numero': '156',
                'ano': 1988,
                'tipo': 'CONSTITUICAO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(1988, 10, 5),
                'data_vigencia': date(1988, 10, 5),
                'ementa': 'Competência municipal para instituir o Imposto sobre Transmissão de Bens Imóveis.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm',
                'palavras_chave': 'ITBI, transmissão bens imóveis, inter vivos, onerosa, restituição ITBI',
                'relevancia': 4,
                'resumo': 'Base constitucional do ITBI, estabelece competência municipal para tributar transmissão onerosa de imóveis.'
            },
            # Taxas Municipais
            {
                'titulo': 'Código Tributário Nacional - Taxas (Art. 77-80)',
                'numero': '5172',
                'ano': 1966,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(1966, 10, 25),
                'data_vigencia': date(1967, 1, 1),
                'ementa': 'Disciplina as taxas municipais pelo poder de polícia e utilização de serviços públicos.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l5172.htm',
                'palavras_chave': 'taxas municipais, poder polícia, serviços públicos, restituição taxas, cobrança indevida',
                'relevancia': 4,
                'resumo': 'Disciplina geral das taxas municipais, base para identificar cobranças indevidas e oportunidades de restituição.'
            },
            # Contribuição de Melhoria
            {
                'titulo': 'Decreto-Lei 195/1967 - Contribuição de Melhoria',
                'numero': '195',
                'ano': 1967,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(1967, 2, 24),
                'data_vigencia': date(1967, 2, 24),
                'ementa': 'Dispõe sobre a cobrança da Contribuição de Melhoria.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del0195.htm',
                'palavras_chave': 'contribuição melhoria, obras públicas, valorização imobiliária, restituição melhoria',
                'relevancia': 3,
                'resumo': 'Regulamenta contribuição de melhoria municipal, importante para identificar cobranças sem obra ou valorização efetiva.'
            },
            # COSIP - Contribuição para Custeio da Iluminação Pública
            {
                'titulo': 'Emenda Constitucional 39/2002 - COSIP',
                'numero': '39',
                'ano': 2002,
                'tipo': 'CONSTITUICAO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2002, 12, 19),
                'data_vigencia': date(2002, 12, 19),
                'ementa': 'Acrescenta artigo ao Ato das Disposições Constitucionais Transitórias, instituindo a Contribuição para o Custeio do Serviço de Iluminação Pública.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc39.htm',
                'palavras_chave': 'COSIP, iluminação pública, contribuição municipal, restituição COSIP, cobrança indevida',
                'relevancia': 4,
                'resumo': 'Criou a COSIP, base para verificar cobranças indevidas da contribuição de iluminação pública.'
            },
            # Simples Nacional Municipal
            {
                'titulo': 'Lei Complementar 123/2006 - Simples Nacional ISS',
                'numero': '123',
                'ano': 2006,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2006, 12, 14),
                'data_vigencia': date(2007, 7, 1),
                'ementa': 'Institui o Estatuto Nacional da Microempresa e da Empresa de Pequeno Porte - Simples Nacional - ISS.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm',
                'palavras_chave': 'Simples Nacional, ISS, microempresas, pequenas empresas, restituição Simples municipal',
                'relevancia': 5,
                'resumo': 'Regula ISS no Simples Nacional, fonte de oportunidades de restituição para micro e pequenas empresas prestadoras de serviços.'
            },
            # ISS Eletrônico
            {
                'titulo': 'Lei 12.741/2012 - Transparência Tributária Municipal',
                'numero': '12741',
                'ano': 2012,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2012, 12, 8),
                'data_vigencia': date(2013, 6, 8),
                'ementa': 'Dispõe sobre as medidas de esclarecimento ao consumidor sobre tributos incidentes sobre mercadorias e serviços.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12741.htm',
                'palavras_chave': 'transparência tributária, ISS, informação tributos, consumidor, restituição transparência',
                'relevancia': 3,
                'resumo': 'Obriga informação sobre tributos ao consumidor, base para verificar cobranças de ISS em notas fiscais.'
            },
            # Lei Geral de Proteção de Dados - Impacto Municipal
            {
                'titulo': 'Lei 13.709/2018 - LGPD Tributos Municipais',
                'numero': '13709',
                'ano': 2018,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2018, 8, 14),
                'data_vigencia': date(2020, 9, 18),
                'ementa': 'Lei Geral de Proteção de Dados Pessoais aplicada à tributação municipal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm',
                'palavras_chave': 'LGPD, proteção dados, tributação municipal, privacidade, fiscalização municipal',
                'relevancia': 2,
                'resumo': 'LGPD aplicada à tributação municipal, estabelece limites para uso de dados pessoais em fiscalização tributária.'
            },
            # Marco Legal das Startups - ISS
            {
                'titulo': 'Lei Complementar 182/2021 - Marco Legal Startups ISS',
                'numero': '182',
                'ano': 2021,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2021, 6, 1),
                'data_vigencia': date(2021, 6, 1),
                'ementa': 'Marco Legal das Startups e do Empreendedorismo Inovador - ISS.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp182.htm',
                'palavras_chave': 'startups, empreendedorismo inovador, ISS, benefícios fiscais municipais, restituição startups',
                'relevancia': 3,
                'resumo': 'Marco legal das startups com benefícios fiscais municipais, oportunidades de restituição para empresas inovadoras.'
            },
            # Lei de Responsabilidade Fiscal Municipal
            {
                'titulo': 'Lei Complementar 101/2000 - LRF Municipal',
                'numero': '101',
                'ano': 2000,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2000, 5, 4),
                'data_vigencia': date(2000, 5, 4),
                'ementa': 'Estabelece normas de finanças públicas voltadas para a responsabilidade na gestão fiscal municipal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm',
                'palavras_chave': 'responsabilidade fiscal, gestão municipal, receita tributária, transparência municipal',
                'relevancia': 4,
                'resumo': 'LRF aplicada aos municípios, estabelece regras de transparência e responsabilidade na arrecadação tributária municipal.'
            },
            # Estatuto da Cidade - Tributação Urbanística
            {
                'titulo': 'Lei 10.257/2001 - Estatuto da Cidade Tributação',
                'numero': '10257',
                'ano': 2001,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2001, 7, 10),
                'data_vigencia': date(2001, 10, 10),
                'ementa': 'Regulamenta os arts. 182 e 183 da Constituição Federal, estabelece diretrizes gerais da política urbana.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/leis_2001/l10257.htm',
                'palavras_chave': 'Estatuto da Cidade, IPTU progressivo, função social propriedade, tributação urbanística',
                'relevancia': 3,
                'resumo': 'Estatuto da Cidade com regras de tributação urbanística, base para verificar aplicação correta do IPTU progressivo.'
            },
        ]

        with transaction.atomic():
            for leg_data in legislacoes:
                try:
                    self.stdout.write(f'📖 Processando: {leg_data["titulo"]}')
                    
                    # Verificar se já existe
                    existing = Legislacao.objects.filter(
                        tipo=leg_data['tipo'],
                        numero=leg_data['numero'],
                        ano=leg_data['ano'],
                        orgao=leg_data['orgao']
                    ).first()

                    if existing:
                        # Atualizar esfera para municipal se necessário
                        existing.esfera = 'MUNICIPAL'
                        for key, value in leg_data.items():
                            if key != 'texto_completo':  # Preservar texto existente
                                setattr(existing, key, value)
                        existing.save()
                        self.stdout.write(
                            self.style.WARNING(f'✏️  Atualizada: {leg_data["titulo"]}')
                        )
                        legislacao = existing
                    else:
                        # Criar nova
                        legislacao = Legislacao.objects.create(**leg_data)
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Criada: {leg_data["titulo"]}')
                        )

                    # Para legislações municipais, adicionar conteúdo explicativo específico
                    if not legislacao.texto_completo or len(legislacao.texto_completo) < 1000:
                        legislacao.texto_completo = f"""
{leg_data['tipo']} Nº {leg_data['numero']}/{leg_data['ano']} - LEGISLAÇÃO MUNICIPAL

{leg_data['ementa']}

RESUMO:
{leg_data.get('resumo', '')}

APLICAÇÃO MUNICIPAL:
Esta legislação estabelece regras para tributos municipais com foco em:
- Identificação de oportunidades de recuperação fiscal municipal
- Análise de créditos de ISS não aproveitados
- Verificação de IPTU cobrado indevidamente
- Restituição de tributos municipais pagos indevidamente
- Compensação de créditos municipais

TRIBUTOS MUNICIPAIS ABRANGIDOS:
1. ISS - Imposto Sobre Serviços de Qualquer Natureza
2. IPTU - Imposto sobre Propriedade Predial e Territorial Urbana
3. ITBI - Imposto sobre Transmissão de Bens Imóveis
4. Taxas Municipais (poder de polícia e serviços públicos)
5. Contribuição de Melhoria
6. COSIP - Contribuição para Custeio da Iluminação Pública

OPORTUNIDADES DE RECUPERAÇÃO MUNICIPAL:
- ISS cobrado sobre serviços não tributáveis
- ISS com alíquotas acima do limite legal
- IPTU com progressividade irregular
- IPTU sobre imóveis com isenção não aplicada
- ITBI sobre transmissões não onerosas
- Taxas sem contrapartida de serviço
- Contribuição de melhoria sem obra efetiva
- COSIP cobrada indevidamente
- Simples Nacional com ISS em duplicidade

PROCEDIMENTOS MUNICIPAIS:
- Pedidos de restituição nas Secretarias Municipais de Fazenda
- Processos administrativos tributários municipais
- Recursos ao Conselho de Contribuintes Municipal
- Ações judiciais na Justiça Estadual (competência)
- Mandado de segurança preventivo

PRAZOS MUNICIPAIS:
- Prescrição: 5 anos (regra geral)
- Decadência: 5 anos para lançamento
- Defesa: 30 dias em processo administrativo
- Recurso: 30 dias da decisão de primeira instância
- Repetição de indébito: 5 anos do pagamento

CONTROLES NECESSÁRIOS:
- Escrituração fiscal de serviços (ISS)
- Declarações municipais (DMS, DIMOB, etc.)
- Notas fiscais de serviços (NFS-e)
- Comprovantes de pagamento de tributos municipais
- Cadastro imobiliário municipal
- Alvará de funcionamento

PARTICULARIDADES MUNICIPAIS:
- Autonomia municipal para legislar sobre tributos locais
- Variação de alíquotas entre municípios
- Regimes especiais municipais
- Convênios intermunicipais
- Programas de recuperação fiscal municipal

GUERRA FISCAL MUNICIPAL:
- Competição por empresas de serviços
- Benefícios fiscais de ISS
- Alíquotas diferenciadas
- Regimes especiais setoriais
- Incentivos ao desenvolvimento local

PRINCIPAIS SETORES AFETADOS:
- Prestadores de serviços (ISS)
- Proprietários de imóveis (IPTU/ITBI)
- Empresas com estabelecimentos (taxas)
- Beneficiários de obras públicas (contribuição de melhoria)
- Consumidores de energia (COSIP)

TECNOLOGIA E MUNICIPAL:
- Nota Fiscal de Serviços Eletrônica (NFS-e)
- Sistemas de arrecadação online
- Cadastros digitais
- Fiscalização eletrônica
- Inteligência artificial na auditoria

Para informações específicas de cada município, consulte:
- Secretaria Municipal de Fazenda
- Código Tributário Municipal
- Regulamento de cada tributo
- Conselho de Contribuintes Municipal
- Procuradoria Geral do Município

URL Oficial: {leg_data['url_oficial']}
"""
                        legislacao.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Conteúdo explicativo adicionado: {len(legislacao.texto_completo)} caracteres')
                        )

                    # Pausa entre requisições
                    time.sleep(0.5)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        total_legislacoes = Legislacao.objects.count()
        municipais = Legislacao.objects.filter(esfera='MUNICIPAL').count()
        iss = Legislacao.objects.filter(palavras_chave__icontains='ISS').count()
        iptu = Legislacao.objects.filter(palavras_chave__icontains='IPTU').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   🏛️  Legislações municipais: {municipais}\n'
                f'   💰 Legislações ISS: {iss}\n'
                f'   🏠 Legislações IPTU: {iptu}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações municipais carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades municipais
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🏛️ OPORTUNIDADES DE RECUPERAÇÃO FISCAL MUNICIPAL:\n'
                f'   ✅ ISS cobrado sobre serviços não tributáveis\n'
                f'   ✅ ISS com alíquotas acima do limite legal\n'
                f'   ✅ IPTU com progressividade irregular\n'
                f'   ✅ IPTU sobre imóveis com isenção não aplicada\n'
                f'   ✅ ITBI sobre transmissões não onerosas\n'
                f'   ✅ Taxas sem contrapartida de serviço\n'
                f'   ✅ Contribuição de melhoria sem obra efetiva\n'
                f'   ✅ COSIP cobrada indevidamente\n'
                f'   ✅ Simples Nacional com ISS em duplicidade\n'
                f'   ✅ Transparência tributária não cumprida\n'
            )
        ) 