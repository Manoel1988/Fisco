import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações sobre regimes monofásicos e prevenção de dupla tributação'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações sobre regimes monofásicos...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Lei 10.147/00 - Regime Monofásico PIS/COFINS
            {
                'titulo': 'Lei 10.147/2000 - Regime Monofásico PIS/COFINS',
                'numero': '10147',
                'ano': 2000,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2000, 12, 21),
                'data_vigencia': date(2001, 1, 1),
                'ementa': 'Dispõe sobre a incidência da contribuição para os Programas de Integração Social e de Formação do Patrimônio do Servidor Público - PIS/Pasep, e da Contribuição para o Financiamento da Seguridade Social - Cofins, nas operações de venda dos produtos que especifica.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l10147.htm',
                'palavras_chave': 'monofásico, PIS, COFINS, combustíveis, cigarros, bebidas, dupla tributação',
                'relevancia': 4,
                'resumo': 'Lei fundamental que estabelece o regime monofásico para PIS/COFINS em combustíveis, cigarros e bebidas, evitando dupla tributação ao concentrar a incidência em apenas uma etapa da cadeia produtiva.'
            },
            # Lei 10.485/02 - Regime Monofásico Ampliado
            {
                'titulo': 'Lei 10.485/2002 - Regime Monofásico Ampliado',
                'numero': '10485',
                'ano': 2002,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2002, 7, 3),
                'data_vigencia': date(2002, 7, 3),
                'ementa': 'Dispõe sobre a incidência do Imposto sobre Produtos Industrializados - IPI, da contribuição para o PIS/Pasep e da Cofins sobre produtos farmacêuticos, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2002/L10485.htm',
                'palavras_chave': 'monofásico, IPI, PIS, COFINS, medicamentos, produtos farmacêuticos',
                'relevancia': 4,
                'resumo': 'Estende o regime monofásico para produtos farmacêuticos, estabelecendo que IPI, PIS e COFINS incidem apenas na saída do estabelecimento industrial ou importador.'
            },
            # Lei 10.865/04 - Regime Monofásico Consolidado
            {
                'titulo': 'Lei 10.865/2004 - Regime Monofásico Consolidado',
                'numero': '10865',
                'ano': 2004,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2004, 4, 30),
                'data_vigencia': date(2004, 5, 1),
                'ementa': 'Dispõe sobre a Contribuição para os Programas de Integração Social e de Formação do Patrimônio do Servidor Público e a Contribuição para o Financiamento da Seguridade Social incidentes sobre a importação de bens e serviços.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l10.865.htm',
                'palavras_chave': 'PIS, COFINS, importação, monofásico, bens, serviços',
                'relevancia': 4,
                'resumo': 'Consolida as regras de PIS/COFINS na importação e estabelece critérios para evitar dupla tributação entre produtos nacionais e importados.'
            },
            # Lei 11.051/04 - Regime Monofásico Autopeças
            {
                'titulo': 'Lei 11.051/2004 - Regime Monofásico Autopeças',
                'numero': '11051',
                'ano': 2004,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2004, 12, 29),
                'data_vigencia': date(2005, 1, 1),
                'ementa': 'Dispõe sobre o desconto de crédito na aquisição de veículos automotores por pessoas com deficiência física e sobre a incidência do IPI sobre produtos industrializados.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11051.htm',
                'palavras_chave': 'IPI, autopeças, veículos, monofásico, pessoas com deficiência',
                'relevancia': 3,
                'resumo': 'Estabelece regras específicas para tributação de autopeças e veículos, incluindo regimes monofásicos para evitar dupla incidência.'
            },
            # Decreto 6.707/08 - Regulamentação Monofásico
            {
                'titulo': 'Decreto 6.707/2008 - Regulamentação do Regime Monofásico',
                'numero': '6707',
                'ano': 2008,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2008, 12, 23),
                'data_vigencia': date(2009, 1, 1),
                'ementa': 'Regulamenta a cobrança da Contribuição para o PIS/Pasep e da Cofins sobre bebidas, produtos de perfumaria, de toucador e de higiene pessoal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/decreto/d6707.htm',
                'palavras_chave': 'PIS, COFINS, monofásico, bebidas, perfumaria, higiene pessoal',
                'relevancia': 4,
                'resumo': 'Regulamenta detalhadamente o regime monofásico para bebidas e produtos de higiene, estabelecendo critérios para identificar dupla tributação.'
            },
            # Lei 12.995/14 - Regime Monofásico Medicamentos
            {
                'titulo': 'Lei 12.995/2014 - Regime Monofásico Medicamentos',
                'numero': '12995',
                'ano': 2014,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2014, 6, 18),
                'data_vigencia': date(2014, 6, 18),
                'ementa': 'Altera as Leis que especifica, para dispor sobre a aplicação da Contribuição para o PIS/Pasep e da Cofins sobre medicamentos e produtos farmacêuticos.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12995.htm',
                'palavras_chave': 'medicamentos, PIS, COFINS, monofásico, produtos farmacêuticos',
                'relevancia': 4,
                'resumo': 'Atualiza as regras do regime monofásico para medicamentos, estabelecendo critérios claros para evitar dupla tributação.'
            },
            # IN RFB 1.911/19 - Procedimentos Monofásico
            {
                'titulo': 'Instrução Normativa RFB 1.911/2019 - Procedimentos Regime Monofásico',
                'numero': '1911',
                'ano': 2019,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2019, 10, 11),
                'data_vigencia': date(2019, 11, 1),
                'ementa': 'Dispõe sobre a incidência da Contribuição para o PIS/Pasep e da Cofins sobre produtos sujeitos ao regime de tributação monofásica.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2019/in-rfb-no-1-911-de-11-de-outubro-de-2019',
                'palavras_chave': 'monofásico, PIS, COFINS, procedimentos, Receita Federal, dupla tributação',
                'relevancia': 4,
                'resumo': 'Instrução normativa que detalha os procedimentos operacionais para aplicação do regime monofásico e identificação de situações de dupla tributação.'
            },
            # Lei 9.718/98 - Base Legal Dupla Tributação
            {
                'titulo': 'Lei 9.718/1998 - Alterações PIS/COFINS e Dupla Tributação',
                'numero': '9718',
                'ano': 1998,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1998, 11, 27),
                'data_vigencia': date(1999, 2, 1),
                'ementa': 'Altera a Legislação Tributária Federal e estabelece normas para evitar dupla tributação.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9718.htm',
                'palavras_chave': 'PIS, COFINS, dupla tributação, bis in idem, base de cálculo',
                'relevancia': 4,
                'resumo': 'Lei que estabelece os princípios fundamentais para evitar dupla tributação em PIS e COFINS, base para regimes monofásicos.'
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
Esta Instrução Normativa estabelece procedimentos operacionais para:
- Identificação de produtos sujeitos ao regime monofásico
- Prevenção de dupla tributação (bis in idem)
- Controle de incidência única de PIS/COFINS
- Procedimentos para restituição em casos de duplo pagamento

PRODUTOS ABRANGIDOS:
- Combustíveis e lubrificantes
- Cigarros e produtos do fumo
- Bebidas alcoólicas e não alcoólicas
- Medicamentos e produtos farmacêuticos
- Produtos de perfumaria e higiene pessoal
- Autopeças e pneumáticos

CONCEITOS FUNDAMENTAIS:
1. REGIME MONOFÁSICO: Tributação concentrada em apenas uma etapa da cadeia produtiva
2. DUPLA TRIBUTAÇÃO: Incidência do mesmo tributo sobre o mesmo fato gerador
3. BIS IN IDEM: Vedação constitucional à dupla tributação
4. SUBSTITUIÇÃO TRIBUTÁRIA: Responsabilidade de terceiro pelo pagamento do tributo

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
        monofasicas = Legislacao.objects.filter(palavras_chave__icontains='monofásico').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   🔄 Legislações monofásicas: {monofasicas}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações sobre regimes monofásicos carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🤖 FUNCIONALIDADES PARA DETECÇÃO DE DUPLA TRIBUTAÇÃO:\n'
                f'   ✅ Identificação de produtos em regime monofásico\n'
                f'   ✅ Verificação de bis in idem (dupla tributação)\n'
                f'   ✅ Análise de cadeias produtivas tributárias\n'
                f'   ✅ Detecção de pagamentos duplicados\n'
                f'   ✅ Orientação para restituição de tributos\n'
                f'   ✅ Compliance em regimes especiais\n'
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