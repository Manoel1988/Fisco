import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações complementares importantes para tributação'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações complementares...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Lei 9.430/96 - Fiscalização e IRPJ
            {
                'titulo': 'Lei 9.430/1996 - Fiscalização e Imposto de Renda Pessoa Jurídica',
                'numero': '9430',
                'ano': 1996,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1996, 12, 27),
                'data_vigencia': date(1997, 1, 1),
                'ementa': 'Dispõe sobre a legislação tributária federal, as contribuições para a seguridade social, o processo administrativo de consulta e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9430.htm',
                'palavras_chave': 'fiscalização, IRPJ, legislação tributária federal, consulta administrativa',
                'relevancia': 4,
            },
            # Lei 10.637/02 - PIS não cumulativo
            {
                'titulo': 'Lei 10.637/2002 - PIS Não Cumulativo',
                'numero': '10637',
                'ano': 2002,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2002, 12, 30),
                'data_vigencia': date(2003, 2, 1),
                'ementa': 'Dispõe sobre a não-cumulatividade na cobrança da contribuição para os Programas de Integração Social (PIS) e de Formação do Patrimônio do Servidor Público (Pasep).',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2002/L10637.htm',
                'palavras_chave': 'PIS, não cumulativo, contribuição social, créditos',
                'relevancia': 4,
            },
            # Lei 10.833/03 - COFINS não cumulativo
            {
                'titulo': 'Lei 10.833/2003 - COFINS Não Cumulativo',
                'numero': '10833',
                'ano': 2003,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2003, 12, 29),
                'data_vigencia': date(2004, 2, 1),
                'ementa': 'Altera a Legislação Tributária Federal e dá outras providências sobre a não-cumulatividade da COFINS.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2003/L10.833.htm',
                'palavras_chave': 'COFINS, não cumulativo, contribuição social, créditos',
                'relevancia': 4,
            },
            # Lei 12.973/14 - Tributação de pessoas jurídicas
            {
                'titulo': 'Lei 12.973/2014 - Tributação de Pessoas Jurídicas',
                'numero': '12973',
                'ano': 2014,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2014, 5, 13),
                'data_vigencia': date(2015, 1, 1),
                'ementa': 'Altera a legislação tributária federal relativa ao Imposto sobre a Renda das Pessoas Jurídicas - IRPJ, à Contribuição Social sobre o Lucro Líquido - CSLL.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12973.htm',
                'palavras_chave': 'IRPJ, CSLL, pessoas jurídicas, tributação, lucro',
                'relevancia': 4,
            },
            # Decreto 9.580/18 - RIR 2018
            {
                'titulo': 'Decreto 9.580/2018 - Regulamento do Imposto de Renda (RIR/2018)',
                'numero': '9580',
                'ano': 2018,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2018, 11, 22),
                'data_vigencia': date(2019, 1, 1),
                'ementa': 'Regulamenta a tributação, a fiscalização, a arrecadação e a administração do Imposto sobre a Renda e Proventos de Qualquer Natureza.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/decreto/D9580.htm',
                'palavras_chave': 'RIR, imposto de renda, regulamento, tributação, fiscalização',
                'relevancia': 4,
            },
            # Decreto 7.212/10 - Regulamento do IPI
            {
                'titulo': 'Decreto 7.212/2010 - Regulamento do IPI (RIPI/2010)',
                'numero': '7212',
                'ano': 2010,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2010, 6, 15),
                'data_vigencia': date(2010, 7, 1),
                'ementa': 'Regulamenta a cobrança, a fiscalização, a arrecadação e a administração do Imposto sobre Produtos Industrializados - IPI.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/decreto/d7212.htm',
                'palavras_chave': 'IPI, RIPI, produtos industrializados, regulamento, fiscalização',
                'relevancia': 4,
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
                        legislacao = Legislacao.objects.create(
                            titulo=leg_data['titulo'],
                            numero=leg_data['numero'],
                            ano=leg_data['ano'],
                            tipo=leg_data['tipo'],
                            area=leg_data['area'],
                            orgao=leg_data['orgao'],
                            data_publicacao=leg_data['data_publicacao'],
                            data_vigencia=leg_data['data_vigencia'],
                            ementa=leg_data['ementa'],
                            url_oficial=leg_data['url_oficial'],
                            palavras_chave=leg_data['palavras_chave'],
                            ativo=True,
                            relevancia=leg_data['relevancia']
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Criada: {leg_data["titulo"]}')
                        )

                    # Extrair conteúdo se ainda não tem
                    if not legislacao.texto_completo or len(legislacao.texto_completo) < 1000:
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

                    # Pausa entre requisições
                    time.sleep(2)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        total_legislacoes = Legislacao.objects.count()
        ativas = Legislacao.objects.filter(ativo=True).count()
        criticas = Legislacao.objects.filter(relevancia=4).count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   ✅ Legislações ativas: {ativas}\n'
                f'   🔥 Relevância crítica: {criticas}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações complementares carregadas com sucesso!')
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
            
            # Remover divs de navegação e menu
            for elemento in soup.find_all('div', {'class': ['menu', 'nav', 'navegacao', 'rodape', 'header', 'topo']}):
                elemento.decompose()
            
            # Tentar diferentes seletores para o conteúdo
            conteudo_div = None
            
            # Seletores comuns do Planalto
            selectors = [
                'div.texto-lei',
                'div.texto',
                'div.conteudo',
                'div#conteudo',
                'div.artigo',
                'div.lei-texto',
                'div.norma-texto',
                'main',
                'article'
            ]
            
            for selector in selectors:
                conteudo_div = soup.select_one(selector)
                if conteudo_div:
                    break
            
            # Se não encontrou, pegar o body
            if not conteudo_div:
                conteudo_div = soup.find('body')
            
            if conteudo_div:
                # Extrair texto
                texto = conteudo_div.get_text(separator='\n', strip=True)
                
                # Limpeza básica
                linhas = []
                for linha in texto.split('\n'):
                    linha = linha.strip()
                    if linha and len(linha) > 3:
                        # Filtrar linhas que são claramente navegação/menu
                        if not any(palavra in linha.lower() for palavra in [
                            'javascript', 'menu', 'navegação', 'voltar', 'imprimir',
                            'compartilhar', 'facebook', 'twitter', 'whatsapp', 'buscar'
                        ]):
                            linhas.append(linha)
                
                texto_limpo = '\n'.join(linhas)
                
                # Verificar se parece ser conteúdo legal
                if any(palavra in texto_limpo.lower() for palavra in ['art.', 'artigo', 'lei', 'decreto', 'parágrafo']):
                    return texto_limpo
            
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao extrair do Planalto: {str(e)}')
            )
            return None 