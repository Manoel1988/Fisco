import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega o conteúdo completo das legislações básicas importantes'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando conteúdo completo das legislações...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            {
                'titulo': 'Código Tributário Nacional',
                'numero': '5172',
                'ano': 1966,
                'tipo': 'LEI',
                'url': 'https://www.planalto.gov.br/ccivil_03/Leis/L5172.htm',
                'extrator': self._extrair_planalto
            },
            {
                'titulo': 'Regulamento do Imposto sobre Produtos Industrializados - RIPI',
                'numero': '7574',
                'ano': 2011,
                'tipo': 'DECRETO',
                'url': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/decreto/d7574.htm',
                'extrator': self._extrair_planalto
            },
            {
                'titulo': 'Constituição da República Federativa do Brasil',
                'numero': '1988',
                'ano': 1988,
                'tipo': 'CONSTITUICAO',
                'url': 'https://normas.leg.br/?urn=urn:lex:br:federal:constituicao:1988-10-05;1988',
                'extrator': self._extrair_normas_leg
            }
        ]

        with transaction.atomic():
            for leg_data in legislacoes:
                try:
                    self.stdout.write(f'📖 Processando: {leg_data["titulo"]}')
                    
                    # Buscar legislação existente
                    legislacao = Legislacao.objects.filter(
                        tipo=leg_data['tipo'],
                        numero=leg_data['numero'],
                        ano=leg_data['ano']
                    ).first()

                    if not legislacao:
                        self.stdout.write(
                            self.style.WARNING(f'⚠️  Legislação não encontrada no banco: {leg_data["titulo"]}')
                        )
                        continue

                    # Extrair conteúdo
                    self.stdout.write(f'🌐 Baixando conteúdo de: {leg_data["url"]}')
                    conteudo = leg_data['extrator'](session, leg_data['url'])
                    
                    if conteudo:
                        # Atualizar com conteúdo completo
                        legislacao.texto_completo = conteudo
                        legislacao.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Conteúdo extraído: {len(conteudo)} caracteres'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'⚠️  Não foi possível extrair conteúdo')
                        )

                    # Pausa entre requisições
                    time.sleep(2)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        total = Legislacao.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas:\n'
                f'   📚 Total de legislações: {total}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Sem conteúdo: {total - com_conteudo}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Conteúdo das legislações carregado!')
        )

    def _extrair_planalto(self, session, url):
        """Extrai conteúdo do site do Planalto"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
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
                # Remover scripts, estilos e navegação
                for elemento in conteudo_div.find_all(['script', 'style', 'nav', 'header', 'footer']):
                    elemento.decompose()
                
                # Extrair texto
                texto = conteudo_div.get_text(separator='\n', strip=True)
                
                # Limpeza básica
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                texto_limpo = '\n'.join(linhas)
                
                return texto_limpo
            
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao extrair do Planalto: {str(e)}')
            )
            return None

    def _extrair_normas_leg(self, session, url):
        """Extrai conteúdo do site normas.leg.br"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Seletores específicos para normas.leg.br
            selectors = [
                'div.texto-norma',
                'div.conteudo-norma',
                'div.artigo-texto',
                'div.lei-completa',
                'main',
                'div.content'
            ]
            
            conteudo_div = None
            for selector in selectors:
                conteudo_div = soup.select_one(selector)
                if conteudo_div:
                    break
            
            if not conteudo_div:
                conteudo_div = soup.find('body')
            
            if conteudo_div:
                # Remover elementos desnecessários
                for elemento in conteudo_div.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    elemento.decompose()
                
                # Extrair texto
                texto = conteudo_div.get_text(separator='\n', strip=True)
                
                # Limpeza
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                texto_limpo = '\n'.join(linhas)
                
                return texto_limpo
            
            return None
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao extrair de normas.leg.br: {str(e)}')
            )
            return None 