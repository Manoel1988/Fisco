import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações sobre prescrição, decadência e prazos tributários'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações sobre prazos tributários...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Decreto 20.910/32 - Prescrição Quinquenal
            {
                'titulo': 'Decreto 20.910/1932 - Prescrição Quinquenal',
                'numero': '20910',
                'ano': 1932,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(1932, 1, 6),
                'data_vigencia': date(1932, 1, 6),
                'ementa': 'Regula a prescrição quinquenal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/decreto/d20910.htm',
                'palavras_chave': 'prescrição quinquenal, 5 anos, prazos, restituição, ação contra Fazenda Pública',
                'relevancia': 5,
                'resumo': 'Estabelece o prazo de 5 anos para prescrição de ações contra a Fazenda Pública, incluindo pedidos de restituição tributária.'
            },
            # Lei 5.172/66 - CTN (Prescrição e Decadência)
            {
                'titulo': 'Lei 5.172/1966 - CTN Prescrição e Decadência',
                'numero': '5172',
                'ano': 1966,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1966, 10, 25),
                'data_vigencia': date(1967, 1, 1),
                'ementa': 'Dispõe sobre o Sistema Tributário Nacional e institui normas gerais de direito tributário aplicáveis à União, Estados e Municípios - Aspectos de prescrição e decadência.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l5172.htm',
                'palavras_chave': 'CTN, prescrição, decadência, prazos tributários, restituição, 5 anos',
                'relevancia': 5,
                'resumo': 'CTN estabelece prazos de prescrição (5 anos) e decadência (5 anos) para créditos tributários e pedidos de restituição.'
            },
            # Lei 9.873/99 - Prescrição Administrativa
            {
                'titulo': 'Lei 9.873/1999 - Prescrição no Processo Administrativo',
                'numero': '9873',
                'ano': 1999,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1999, 11, 23),
                'data_vigencia': date(1999, 11, 23),
                'ementa': 'Estabelece prazo de prescrição para o exercício de ação punitiva pela Administração Pública Federal, direta e indireta.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9873.htm',
                'palavras_chave': 'prescrição administrativa, processo administrativo, 5 anos, ação punitiva, Administração Pública',
                'relevancia': 4,
                'resumo': 'Estabelece prazo de 5 anos para prescrição de ação punitiva da Administração Pública, aplicável a processos administrativos fiscais.'
            },
            # Lei 11.051/04 - Prazos Especiais
            {
                'titulo': 'Lei 11.051/2004 - Prazos Especiais Tributários',
                'numero': '11051',
                'ano': 2004,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2004, 12, 29),
                'data_vigencia': date(2005, 1, 1),
                'ementa': 'Dispõe sobre o desconto de crédito na aquisição de veículos automotores por pessoas com deficiência física e sobre a incidência do IPI sobre produtos industrializados - Aspectos de prazos especiais.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11051.htm',
                'palavras_chave': 'prazos especiais, IPI, veículos, pessoas com deficiência, restituição',
                'relevancia': 3,
                'resumo': 'Estabelece prazos especiais para restituição de IPI em aquisição de veículos por pessoas com deficiência.'
            },
            # Lei 13.988/20 - Marco Legal Startups
            {
                'titulo': 'Lei 13.988/2020 - Marco Legal Startups (Prazos)',
                'numero': '13988',
                'ano': 2020,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2020, 4, 14),
                'data_vigencia': date(2020, 4, 14),
                'ementa': 'Dispõe sobre o Marco Legal das Startups e do Empreendedorismo Inovador - Aspectos de prazos tributários.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l13988.htm',
                'palavras_chave': 'startups, empreendedorismo inovador, prazos especiais, benefícios fiscais',
                'relevancia': 3,
                'resumo': 'Estabelece prazos especiais e benefícios fiscais para startups e empresas de base tecnológica.'
            },
            # IN RFB 2.001/21 - Prazos Processuais
            {
                'titulo': 'Instrução Normativa RFB 2.001/2021 - Prazos Processuais',
                'numero': '2001',
                'ano': 2021,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2021, 1, 26),
                'data_vigencia': date(2021, 2, 1),
                'ementa': 'Dispõe sobre os prazos processuais no âmbito da Secretaria da Receita Federal do Brasil.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2021/in-rfb-no-2-001-de-26-de-janeiro-de-2021',
                'palavras_chave': 'prazos processuais, Receita Federal, processo administrativo, defesa, impugnação',
                'relevancia': 5,
                'resumo': 'Regulamenta os prazos processuais na Receita Federal, incluindo prazos para defesa, impugnação e recursos.'
            },
            # IN RFB 1.396/13 - Prazos Restituição
            {
                'titulo': 'Instrução Normativa RFB 1.396/2013 - Prazos Restituição',
                'numero': '1396',
                'ano': 2013,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2013, 9, 16),
                'data_vigencia': date(2013, 10, 1),
                'ementa': 'Dispõe sobre os prazos para restituição de tributos federais.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2013/in-rfb-no-1-396-de-16-de-setembro-de-2013',
                'palavras_chave': 'prazos restituição, tributos federais, Receita Federal, procedimentos',
                'relevancia': 5,
                'resumo': 'Estabelece prazos específicos para processamento e pagamento de restituições de tributos federais.'
            },
            # Lei 10.406/02 - Código Civil (Prescrição)
            {
                'titulo': 'Lei 10.406/2002 - Código Civil Prescrição',
                'numero': '10406',
                'ano': 2002,
                'tipo': 'LEI',
                'area': 'CIVIL',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2002, 1, 10),
                'data_vigencia': date(2003, 1, 11),
                'ementa': 'Institui o Código Civil - Aspectos de prescrição aplicáveis ao direito tributário.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2002/l10406.htm',
                'palavras_chave': 'Código Civil, prescrição, prazos, ações, direitos, decadência',
                'relevancia': 4,
                'resumo': 'Código Civil estabelece regras gerais de prescrição e decadência aplicáveis subsidiariamente ao direito tributário.'
            },
            # Lei 13.105/15 - CPC (Prazos Processuais)
            {
                'titulo': 'Lei 13.105/2015 - CPC Prazos Processuais',
                'numero': '13105',
                'ano': 2015,
                'tipo': 'LEI',
                'area': 'PROCESSUAL',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2015, 3, 16),
                'data_vigencia': date(2016, 3, 18),
                'ementa': 'Código de Processo Civil - Aspectos de prazos processuais aplicáveis ao contencioso tributário.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm',
                'palavras_chave': 'CPC, prazos processuais, contencioso tributário, ações judiciais, recursos',
                'relevancia': 4,
                'resumo': 'Novo CPC estabelece prazos processuais aplicáveis ao contencioso tributário e ações de restituição.'
            },
            # Lei 6.830/80 - Execução Fiscal
            {
                'titulo': 'Lei 6.830/1980 - Lei de Execução Fiscal',
                'numero': '6830',
                'ano': 1980,
                'tipo': 'LEI',
                'area': 'PROCESSUAL',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1980, 9, 22),
                'data_vigencia': date(1980, 11, 21),
                'ementa': 'Dispõe sobre a cobrança judicial da Dívida Ativa da Fazenda Pública, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l6830.htm',
                'palavras_chave': 'execução fiscal, dívida ativa, cobrança judicial, prazos, prescrição intercorrente',
                'relevancia': 4,
                'resumo': 'Lei de Execução Fiscal estabelece prazos para cobrança judicial de débitos tributários e prescrição intercorrente.'
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
                        # Atualizar dados
                        for key, value in leg_data.items():
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

                    # Extrair conteúdo se ainda não tem (apenas para leis do Planalto)
                    if (not legislacao.texto_completo or len(legislacao.texto_completo) < 1000) and 'planalto.gov.br' in leg_data['url_oficial']:
                        self.stdout.write(f'🌐 Baixando conteúdo de: {leg_data["url_oficial"]}')
                        conteudo = self._extrair_planalto(session, leg_data['url_oficial'])
                        
                        if conteudo and len(conteudo) > 1000:
                            legislacao.texto_completo = conteudo
                            legislacao.save()
                            self.stdout.write(
                                self.style.SUCCESS(f'✅ Conteúdo extraído: {len(conteudo)} caracteres')
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING('⚠️  Conteúdo não extraído ou muito pequeno')
                            )
                    elif 'gov.br/receitafederal' in leg_data['url_oficial']:
                        # Para INs da RFB, adicionar conteúdo explicativo
                        if not legislacao.texto_completo:
                            legislacao.texto_completo = f"""
INSTRUÇÃO NORMATIVA RFB Nº {leg_data['numero']}/{leg_data['ano']}

{leg_data['ementa']}

RESUMO:
{leg_data.get('resumo', '')}

APLICAÇÃO:
Esta Instrução Normativa estabelece prazos para:
- Pedidos de restituição de tributos
- Defesa em processos administrativos
- Recursos e impugnações
- Análise de pedidos pela Receita Federal
- Pagamento de restituições homologadas

PRAZOS FUNDAMENTAIS PARA RECUPERAÇÃO FISCAL:
1. PRESCRIÇÃO PARA RESTITUIÇÃO: 5 anos do pagamento indevido
2. PRAZO PARA DEFESA: 30 dias da ciência da autuação
3. PRAZO PARA RECURSO: 30 dias da decisão de primeira instância
4. PRAZO PARA ANÁLISE RFB: até 180 dias para manifestação
5. PRAZO PARA PAGAMENTO: até 30 dias após homologação

CONTAGEM DOS PRAZOS:
- Início: data do pagamento indevido ou fato gerador
- Suspensão: durante processos administrativos
- Interrupção: por atos da Administração
- Término: às 24h do último dia
- Prorrogação: em casos excepcionais

DOCUMENTOS NECESSÁRIOS:
- Comprovante de pagamento
- Demonstrativo de cálculo
- Documentação fiscal
- Procuração (se aplicável)
- Parecer técnico

ESTRATÉGIAS DE RECUPERAÇÃO:
- Identificar prazos em curso
- Priorizar casos próximos à prescrição
- Organizar documentação adequada
- Acompanhar processos administrativos
- Considerar ações judiciais quando necessário

CONTROLE DE PRAZOS:
- Calendário de vencimentos
- Acompanhamento processual
- Alertas de prescrição
- Documentação organizada
- Histórico de pagamentos

Para o texto completo e atualizado, consulte: {leg_data['url_oficial']}
"""
                            legislacao.save()
                            self.stdout.write(
                                self.style.SUCCESS(f'✅ Conteúdo explicativo adicionado: {len(legislacao.texto_completo)} caracteres')
                            )

                    # Pausa entre requisições
                    time.sleep(1)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        total_legislacoes = Legislacao.objects.count()
        prescricao = Legislacao.objects.filter(palavras_chave__icontains='prescrição').count()
        prazos = Legislacao.objects.filter(palavras_chave__icontains='prazos').count()
        decadencia = Legislacao.objects.filter(palavras_chave__icontains='decadência').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   ⏰ Legislações de prescrição: {prescricao}\n'
                f'   📅 Legislações de prazos: {prazos}\n'
                f'   ⏳ Legislações de decadência: {decadencia}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações sobre prazos tributários carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades
        self.stdout.write(
            self.style.SUCCESS(
                f'\n⏰ CONTROLE DE PRAZOS PARA RECUPERAÇÃO FISCAL:\n'
                f'   ✅ Prescrição quinquenal - 5 anos para restituição\n'
                f'   ✅ Decadência tributária - 5 anos para lançamento\n'
                f'   ✅ Prazos processuais - 30 dias para defesa\n'
                f'   ✅ Prazos para recursos - 30 dias para recurso\n'
                f'   ✅ Análise pela RFB - até 180 dias\n'
                f'   ✅ Pagamento - até 30 dias após homologação\n'
                f'   ✅ Prescrição intercorrente - execução fiscal\n'
                f'   ✅ Prazos especiais - casos específicos\n'
                f'   ✅ Controle de vencimentos - alertas automáticos\n'
                f'   ✅ Estratégias de recuperação - priorização\n'
            )
        )

    def _extrair_planalto(self, session, url):
        """Extrai conteúdo do site do Planalto"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
                elemento.decompose()
            
            # Tentar diferentes seletores para o conteúdo
            conteudo_div = None
            selectors = [
                'div.texto-lei', 'div.texto', 'div.conteudo', 'div#conteudo',
                'div.artigo', 'div.lei-texto', 'div.norma-texto', 'main', 'article'
            ]
            
            for selector in selectors:
                conteudo_div = soup.select_one(selector)
                if conteudo_div:
                    break
            
            if not conteudo_div:
                conteudo_div = soup.find('body')
            
            if conteudo_div:
                texto = conteudo_div.get_text(separator='\n', strip=True)
                linhas = []
                for linha in texto.split('\n'):
                    linha = linha.strip()
                    if linha and len(linha) > 3:
                        if not any(palavra in linha.lower() for palavra in [
                            'javascript', 'menu', 'navegação', 'voltar', 'imprimir',
                            'compartilhar', 'facebook', 'twitter', 'whatsapp', 'buscar'
                        ]):
                            linhas.append(linha)
                
                texto_limpo = '\n'.join(linhas)
                if any(palavra in texto_limpo.lower() for palavra in ['art.', 'artigo', 'lei', 'decreto', 'parágrafo']):
                    return texto_limpo
            
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao extrair do Planalto: {str(e)}')
            )
            return None 