import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega o conteúdo completo da Constituição Federal'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📜 Carregando conteúdo completo da Constituição Federal...')
        )

        # URL alternativa da Constituição no Planalto
        url_constituicao = 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm'
        
        try:
            # Buscar a Constituição no banco
            constituicao = Legislacao.objects.filter(
                tipo='CONSTITUICAO',
                numero='1988',
                ano=1988
            ).first()

            if not constituicao:
                self.stdout.write(
                    self.style.ERROR('❌ Constituição não encontrada no banco de dados')
                )
                return

            # Extrair conteúdo
            self.stdout.write(f'🌐 Baixando conteúdo de: {url_constituicao}')
            conteudo = self._extrair_constituicao(url_constituicao)
            
            if conteudo and len(conteudo) > 1000:  # Verificar se extraiu conteúdo significativo
                # Atualizar com conteúdo completo
                constituicao.texto_completo = conteudo
                constituicao.url_oficial = url_constituicao  # Atualizar URL também
                constituicao.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Constituição atualizada: {len(conteudo)} caracteres'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  Não foi possível extrair conteúdo significativo')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao processar Constituição: {str(e)}')
            )

        # Estatísticas finais
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        total = Legislacao.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas:\n'
                f'   📚 Total de legislações: {total}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
            )
        )

    def _extrair_constituicao(self, url):
        """Extrai conteúdo específico da Constituição do Planalto"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
                elemento.decompose()
            
            # Remover divs de navegação e menu
            for elemento in soup.find_all('div', {'class': ['menu', 'nav', 'navegacao', 'rodape', 'header']}):
                elemento.decompose()
            
            # Tentar encontrar o conteúdo principal
            conteudo_div = None
            
            # Seletores específicos para a Constituição
            selectors = [
                'div.texto',
                'div.conteudo',
                'div#conteudo',
                'main',
                'article',
                'div.lei-texto',
                'div.norma-texto'
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
                
                # Limpeza mais rigorosa
                linhas = []
                for linha in texto.split('\n'):
                    linha = linha.strip()
                    if linha and len(linha) > 3:  # Filtrar linhas muito curtas
                        # Filtrar linhas que são claramente navegação/menu
                        if not any(palavra in linha.lower() for palavra in [
                            'javascript', 'menu', 'navegação', 'voltar', 'imprimir',
                            'compartilhar', 'facebook', 'twitter', 'whatsapp'
                        ]):
                            linhas.append(linha)
                
                texto_limpo = '\n'.join(linhas)
                
                # Verificar se parece ser conteúdo da Constituição
                if 'constituição' in texto_limpo.lower() and 'artigo' in texto_limpo.lower():
                    return texto_limpo
            
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao extrair Constituição: {str(e)}')
            )
            return None 