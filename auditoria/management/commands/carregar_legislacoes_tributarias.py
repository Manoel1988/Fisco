import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega as principais legislações tributárias brasileiras com conteúdo completo'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações tributárias brasileiras...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # ICMS
            {
                'titulo': 'Lei Complementar 87/1996 - Lei Kandir (ICMS)',
                'numero': '87',
                'ano': 1996,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1996, 9, 13),
                'data_vigencia': date(1996, 9, 13),
                'ementa': 'Dispõe sobre o imposto dos Estados e do Distrito Federal sobre operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte interestadual e intermunicipal e de comunicação.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp87.htm',
                'palavras_chave': 'ICMS, circulação mercadorias, transporte, comunicação, lei kandir',
                'relevancia': 4,
            },
            # ISS
            {
                'titulo': 'Lei Complementar 116/2003 - Lei do ISS',
                'numero': '116',
                'ano': 2003,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2003, 7, 31),
                'data_vigencia': date(2003, 7, 31),
                'ementa': 'Dispõe sobre o Imposto Sobre Serviços de Qualquer Natureza, de competência dos Municípios e do Distrito Federal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm',
                'palavras_chave': 'ISS, imposto sobre serviços, municípios, prestação de serviços',
                'relevancia': 4,
            },
            # Imposto de Renda
            {
                'titulo': 'Lei 8.981/1995 - Alterações no Imposto de Renda',
                'numero': '8981',
                'ano': 1995,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1995, 1, 20),
                'data_vigencia': date(1995, 1, 1),
                'ementa': 'Altera a legislação tributária federal e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8981.htm',
                'palavras_chave': 'imposto de renda, tributação federal, alterações tributárias',
                'relevancia': 3,
            },
            # COFINS
            {
                'titulo': 'Lei Complementar 70/1991 - COFINS',
                'numero': '70',
                'ano': 1991,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1991, 12, 30),
                'data_vigencia': date(1991, 12, 30),
                'ementa': 'Institui contribuição para financiamento da Seguridade Social, eleva a alíquota da contribuição social sobre o lucro das instituições financeiras.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp70.htm',
                'palavras_chave': 'COFINS, contribuição, seguridade social, financiamento',
                'relevancia': 4,
            },
            # PIS
            {
                'titulo': 'Lei Complementar 7/1970 - PIS',
                'numero': '7',
                'ano': 1970,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1970, 9, 7),
                'data_vigencia': date(1970, 9, 7),
                'ementa': 'Institui o Programa de Integração Social, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp07.htm',
                'palavras_chave': 'PIS, programa integração social, contribuição social',
                'relevancia': 4,
            },
            # CSLL
            {
                'titulo': 'Lei 7.689/1988 - Contribuição Social sobre o Lucro Líquido',
                'numero': '7689',
                'ano': 1988,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1988, 12, 15),
                'data_vigencia': date(1989, 1, 1),
                'ementa': 'Institui contribuição social sobre o lucro das pessoas jurídicas e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l7689.htm',
                'palavras_chave': 'CSLL, contribuição social, lucro líquido, pessoas jurídicas',
                'relevancia': 4,
            },
            # SIMPLES Nacional
            {
                'titulo': 'Lei Complementar 123/2006 - Simples Nacional',
                'numero': '123',
                'ano': 2006,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2006, 12, 14),
                'data_vigencia': date(2007, 7, 1),
                'ementa': 'Institui o Estatuto Nacional da Microempresa e da Empresa de Pequeno Porte; altera dispositivos das Leis e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm',
                'palavras_chave': 'simples nacional, microempresa, pequeno porte, estatuto nacional',
                'relevancia': 4,
            },
            # ITCMD
            {
                'titulo': 'Lei 8.383/1991 - Imposto sobre Transmissão Causa Mortis',
                'numero': '8383',
                'ano': 1991,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1991, 12, 30),
                'data_vigencia': date(1991, 12, 30),
                'ementa': 'Institui a cobrança do imposto sobre a transmissão causa mortis e doação de quaisquer bens ou direitos.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8383.htm',
                'palavras_chave': 'ITCMD, transmissão causa mortis, doação, herança',
                'relevancia': 3,
            },
            # Lei de Responsabilidade Fiscal
            {
                'titulo': 'Lei Complementar 101/2000 - Lei de Responsabilidade Fiscal',
                'numero': '101',
                'ano': 2000,
                'tipo': 'LEI',
                'area': 'FISCAL',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2000, 5, 4),
                'data_vigencia': date(2000, 5, 4),
                'ementa': 'Estabelece normas de finanças públicas voltadas para a responsabilidade na gestão fiscal e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm',
                'palavras_chave': 'responsabilidade fiscal, finanças públicas, gestão fiscal, transparência',
                'relevancia': 4,
            },
            # SPED
            {
                'titulo': 'Decreto 6.022/2007 - Sistema Público de Escrituração Digital',
                'numero': '6022',
                'ano': 2007,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2007, 1, 22),
                'data_vigencia': date(2007, 1, 22),
                'ementa': 'Institui o Sistema Público de Escrituração Digital - Sped.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/decreto/d6022.htm',
                'palavras_chave': 'SPED, escrituração digital, sistema público, fiscal',
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
                    time.sleep(1)

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
            self.style.SUCCESS('🎉 Legislações tributárias carregadas com sucesso!')
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