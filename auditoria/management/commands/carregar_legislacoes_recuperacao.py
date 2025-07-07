import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações sobre recuperação de impostos pagos indevidamente'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações sobre recuperação de impostos...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Lei 8.383/91 - Restituição e Compensação
            {
                'titulo': 'Lei 8.383/1991 - Restituição e Compensação Tributária',
                'numero': '8383',
                'ano': 1991,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1991, 12, 30),
                'data_vigencia': date(1992, 1, 1),
                'ementa': 'Institui a Taxa Referencial Diária - TRD, estabelece regras para a restituição e compensação de tributos federais.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8383.htm',
                'palavras_chave': 'restituição, compensação, tributos federais, TRD, pagamento indevido',
                'relevancia': 5,
                'resumo': 'Lei fundamental que estabelece as regras para restituição e compensação de tributos federais pagos indevidamente, base legal para recuperação fiscal.'
            },
            # Lei 9.430/96 - Restituição IRPJ e CSLL
            {
                'titulo': 'Lei 9.430/1996 - Restituição IRPJ e CSLL',
                'numero': '9430',
                'ano': 1996,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1996, 12, 27),
                'data_vigencia': date(1997, 1, 1),
                'ementa': 'Dispõe sobre a legislação tributária federal, as contribuições para a seguridade social, o processo administrativo de consulta e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9430.htm',
                'palavras_chave': 'IRPJ, CSLL, restituição, compensação, pagamento indevido, consulta fiscal',
                'relevancia': 5,
                'resumo': 'Estabelece procedimentos específicos para restituição de IRPJ e CSLL pagos indevidamente, incluindo juros e correção monetária.'
            },
            # Lei 10.637/02 - Créditos PIS
            {
                'titulo': 'Lei 10.637/2002 - Créditos e Restituição PIS',
                'numero': '10637',
                'ano': 2002,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2002, 12, 30),
                'data_vigencia': date(2003, 1, 1),
                'ementa': 'Dispõe sobre a não-cumulatividade na cobrança da contribuição para os Programas de Integração Social (PIS) e de Formação do Patrimônio do Servidor Público (Pasep).',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2002/l10637.htm',
                'palavras_chave': 'PIS, créditos, não cumulatividade, restituição, compensação, pagamento indevido',
                'relevancia': 5,
                'resumo': 'Estabelece o regime não cumulativo do PIS e os direitos a créditos, fundamental para identificar oportunidades de recuperação fiscal.'
            },
            # Lei 10.833/03 - Créditos COFINS
            {
                'titulo': 'Lei 10.833/2003 - Créditos e Restituição COFINS',
                'numero': '10833',
                'ano': 2003,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2003, 12, 29),
                'data_vigencia': date(2004, 2, 1),
                'ementa': 'Altera a Legislação Tributária Federal e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2003/l10.833.htm',
                'palavras_chave': 'COFINS, créditos, não cumulatividade, restituição, compensação, pagamento indevido',
                'relevancia': 5,
                'resumo': 'Estabelece o regime não cumulativo da COFINS e os direitos a créditos, essencial para recuperação de valores pagos indevidamente.'
            },
            # Lei 11.457/07 - Receita Federal (Restituição)
            {
                'titulo': 'Lei 11.457/2007 - Administração Tributária e Restituição',
                'numero': '11457',
                'ano': 2007,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2007, 3, 16),
                'data_vigencia': date(2007, 3, 16),
                'ementa': 'Dispõe sobre a Administração Tributária Federal; altera as Leis nos 10.593, de 6 de dezembro de 2002, 10.683, de 28 de maio de 2003, 8.212, de 24 de julho de 1991, 9.317, de 5 de dezembro de 1996.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11457.htm',
                'palavras_chave': 'administração tributária, restituição, compensação, Receita Federal, processo administrativo',
                'relevancia': 4,
                'resumo': 'Define competências da Receita Federal em processos de restituição e compensação, estabelecendo procedimentos administrativos.'
            },
            # Lei 11.941/09 - REFIS e Restituição
            {
                'titulo': 'Lei 11.941/2009 - REFIS e Restituição de Tributos',
                'numero': '11941',
                'ano': 2009,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2009, 5, 27),
                'data_vigencia': date(2009, 5, 27),
                'ementa': 'Altera a legislação tributária federal relativa ao parcelamento ordinário de débitos tributários; concede remissão nos casos em que especifica.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l11941.htm',
                'palavras_chave': 'REFIS, parcelamento, restituição, compensação, débitos tributários, remissão',
                'relevancia': 4,
                'resumo': 'Estabelece regras para parcelamento e compensação de débitos, incluindo oportunidades de restituição em programas especiais.'
            },
            # Lei 13.670/18 - Restituição Especial
            {
                'titulo': 'Lei 13.670/2018 - Restituição Especial de Tributos',
                'numero': '13670',
                'ano': 2018,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2018, 5, 30),
                'data_vigencia': date(2018, 5, 30),
                'ementa': 'Altera as Leis nos 9.430, de 27 de dezembro de 1996, 9.249, de 26 de dezembro de 1995, 8.383, de 30 de dezembro de 1991, e 8.212, de 24 de julho de 1991.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13670.htm',
                'palavras_chave': 'restituição especial, tributos, compensação, juros, correção monetária',
                'relevancia': 4,
                'resumo': 'Atualiza regras de restituição de tributos, incluindo novos procedimentos para recuperação de valores pagos indevidamente.'
            },
            # Decreto 70.235/72 - Processo Administrativo
            {
                'titulo': 'Decreto 70.235/1972 - Processo Administrativo Tributário',
                'numero': '70235',
                'ano': 1972,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(1972, 3, 6),
                'data_vigencia': date(1972, 3, 6),
                'ementa': 'Dispõe sobre o processo administrativo fiscal, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/decreto/d70235.htm',
                'palavras_chave': 'processo administrativo, fiscalização, defesa, restituição, impugnação',
                'relevancia': 5,
                'resumo': 'Regulamenta o processo administrativo fiscal, essencial para defesa de autuações e pedidos de restituição.'
            },
            # IN RFB 1.717/17 - Restituição e Compensação
            {
                'titulo': 'Instrução Normativa RFB 1.717/2017 - Restituição e Compensação',
                'numero': '1717',
                'ano': 2017,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2017, 7, 17),
                'data_vigencia': date(2017, 8, 1),
                'ementa': 'Dispõe sobre a restituição e a compensação de quantias recolhidas a título de tributos administrados pela Secretaria da Receita Federal do Brasil.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2017/in-rfb-no-1-717-de-17-de-julho-de-2017',
                'palavras_chave': 'restituição, compensação, tributos federais, procedimentos operacionais, Receita Federal',
                'relevancia': 5,
                'resumo': 'Instrução normativa atual que detalha todos os procedimentos para restituição e compensação de tributos federais.'
            },
            # IN RFB 1.300/12 - Créditos PIS/COFINS
            {
                'titulo': 'Instrução Normativa RFB 1.300/2012 - Créditos PIS/COFINS',
                'numero': '1300',
                'ano': 2012,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2012, 11, 21),
                'data_vigencia': date(2013, 1, 1),
                'ementa': 'Dispõe sobre o aproveitamento de créditos apurados na sistemática não cumulativa da Contribuição para o PIS/Pasep e da Cofins.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2012/in-rfb-no-1-300-de-21-de-novembro-de-2012',
                'palavras_chave': 'créditos, PIS, COFINS, não cumulatividade, aproveitamento, compensação',
                'relevancia': 5,
                'resumo': 'Regulamenta o aproveitamento de créditos de PIS/COFINS, fundamental para identificar oportunidades de recuperação fiscal.'
            },
            # Lei 9.532/97 - Dedutibilidade e Restituição
            {
                'titulo': 'Lei 9.532/1997 - Dedutibilidade e Restituição IRPJ',
                'numero': '9532',
                'ano': 1997,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1997, 12, 10),
                'data_vigencia': date(1998, 1, 1),
                'ementa': 'Altera a legislação tributária federal e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9532.htm',
                'palavras_chave': 'IRPJ, dedutibilidade, restituição, despesas, base de cálculo, pagamento indevido',
                'relevancia': 4,
                'resumo': 'Estabelece regras de dedutibilidade no IRPJ, permitindo identificar oportunidades de redução da base de cálculo e restituição.'
            },
            # Lei 12.844/13 - Ressarcimento PIS/COFINS
            {
                'titulo': 'Lei 12.844/2013 - Ressarcimento PIS/COFINS Exportação',
                'numero': '12844',
                'ano': 2013,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2013, 7, 19),
                'data_vigencia': date(2013, 7, 19),
                'ementa': 'Altera as Leis nos 10.637, de 30 de dezembro de 2002, e 10.833, de 29 de dezembro de 2003, para dispor sobre o ressarcimento de PIS/Pasep e Cofins.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12844.htm',
                'palavras_chave': 'ressarcimento, PIS, COFINS, exportação, créditos, não cumulatividade',
                'relevancia': 4,
                'resumo': 'Estabelece regras para ressarcimento de PIS/COFINS em operações de exportação, importante para empresas exportadoras.'
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
Esta Instrução Normativa estabelece procedimentos para:
- Restituição de tributos pagos indevidamente
- Compensação de créditos tributários
- Aproveitamento de créditos de PIS/COFINS
- Procedimentos administrativos para recuperação fiscal
- Documentação necessária para pedidos de restituição

OPORTUNIDADES DE RECUPERAÇÃO FISCAL:
1. TRIBUTOS PAGOS INDEVIDAMENTE: Identificação de pagamentos sem base legal
2. CRÉDITOS NÃO APROVEITADOS: PIS/COFINS não cumulativo, IPI, ICMS
3. DUPLA TRIBUTAÇÃO: Regimes monofásicos e substituição tributária
4. DEDUTIBILIDADE: Despesas não consideradas na base de cálculo
5. BENEFÍCIOS FISCAIS: Incentivos não aplicados corretamente

TIPOS DE RESTITUIÇÃO:
- Restituição em espécie (dinheiro)
- Compensação com outros tributos
- Utilização em parcelamentos
- Transferência para terceiros
- Conversão em investimentos

PRAZOS IMPORTANTES:
- Prescrição: 5 anos para solicitar restituição
- Análise: até 180 dias para manifestação da RFB
- Pagamento: até 30 dias após homologação
- Juros: SELIC desde o pagamento indevido

DOCUMENTAÇÃO NECESSÁRIA:
- Comprovantes de pagamento
- Demonstrativos de cálculo
- Documentos fiscais
- Contratos e notas fiscais
- Pareceres técnicos

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
        recuperacao = Legislacao.objects.filter(palavras_chave__icontains='restituição').count()
        creditos = Legislacao.objects.filter(palavras_chave__icontains='créditos').count()
        compensacao = Legislacao.objects.filter(palavras_chave__icontains='compensação').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   💰 Legislações de restituição: {recuperacao}\n'
                f'   🎯 Legislações de créditos: {creditos}\n'
                f'   🔄 Legislações de compensação: {compensacao}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações sobre recuperação fiscal carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades
        self.stdout.write(
            self.style.SUCCESS(
                f'\n💰 OPORTUNIDADES DE RECUPERAÇÃO FISCAL:\n'
                f'   ✅ Restituição de tributos pagos indevidamente\n'
                f'   ✅ Compensação de créditos tributários\n'
                f'   ✅ Aproveitamento de créditos PIS/COFINS\n'
                f'   ✅ Recuperação por dupla tributação\n'
                f'   ✅ Dedutibilidade de despesas não consideradas\n'
                f'   ✅ Aplicação de benefícios fiscais\n'
                f'   ✅ Ressarcimento em operações de exportação\n'
                f'   ✅ Análise de prescrição e prazos\n'
                f'   ✅ Orientação sobre procedimentos administrativos\n'
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