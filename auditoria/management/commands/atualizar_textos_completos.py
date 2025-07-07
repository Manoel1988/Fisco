import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Atualiza todas as legislações no banco com texto completo real das leis'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Atualizando todas as legislações com texto completo...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Buscar todas as legislações
        legislacoes = Legislacao.objects.all().order_by('id')
        total = legislacoes.count()
        
        self.stdout.write(f'📊 Encontradas {total} legislações para atualizar')

        contador = 0
        for legislacao in legislacoes:
            contador += 1
            self.stdout.write(f'[{contador}/{total}] Processando: {legislacao.get_identificacao()}')
            
            try:
                # Determinar a URL base e método de extração
                texto_completo = self._extrair_texto_completo(legislacao, session)
                
                if texto_completo and len(texto_completo) > 500:  # Só atualizar se tiver conteúdo substancial
                    legislacao.texto_completo = texto_completo
                    legislacao.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Atualizada: {len(texto_completo)} caracteres')
                    )
                else:
                    # Se não conseguir extrair, criar texto estruturado baseado nos dados existentes
                    texto_estruturado = self._criar_texto_estruturado(legislacao)
                    legislacao.texto_completo = texto_estruturado
                    legislacao.save()
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Criado texto estruturado: {len(texto_estruturado)} caracteres')
                    )
                
                # Pausa para não sobrecarregar os servidores
                time.sleep(0.5)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro: {str(e)}')
                )
                # Criar texto estruturado em caso de erro
                texto_estruturado = self._criar_texto_estruturado(legislacao)
                legislacao.texto_completo = texto_estruturado
                legislacao.save()
                continue

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Processo concluído! {total} legislações processadas.')
        )

    def _extrair_texto_completo(self, legislacao, session):
        """Extrai o texto completo da legislação de fontes oficiais"""
        
        if not legislacao.url_oficial:
            return None
            
        try:
            # Tentar extrair do Planalto
            if 'planalto.gov.br' in legislacao.url_oficial:
                return self._extrair_planalto(legislacao.url_oficial, session)
            
            # Tentar extrair do Senado
            elif 'senado.leg.br' in legislacao.url_oficial or 'legis.senado.leg.br' in legislacao.url_oficial:
                return self._extrair_senado(legislacao.url_oficial, session)
            
            # Tentar extrair da Receita Federal
            elif 'receita.fazenda.gov.br' in legislacao.url_oficial:
                return self._extrair_receita(legislacao.url_oficial, session)
            
            # Outras fontes
            else:
                return self._extrair_generico(legislacao.url_oficial, session)
                
        except Exception as e:
            self.stdout.write(f'Erro ao extrair de {legislacao.url_oficial}: {e}')
            return None

    def _extrair_planalto(self, url, session):
        """Extrai texto do site do Planalto"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
                elemento.decompose()
            
            # Buscar o conteúdo principal
            conteudo = soup.find('div', class_='texto-norma') or soup.find('div', class_='conteudo') or soup.find('body')
            
            if conteudo:
                texto = conteudo.get_text(separator='\n', strip=True)
                # Limpar texto
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                return '\n'.join(linhas)
            
            return None
            
        except Exception as e:
            self.stdout.write(f'Erro Planalto: {e}')
            return None

    def _extrair_senado(self, url, session):
        """Extrai texto do site do Senado"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
                elemento.decompose()
            
            # Buscar o conteúdo principal
            conteudo = soup.find('div', class_='texto') or soup.find('div', class_='conteudo') or soup.find('body')
            
            if conteudo:
                texto = conteudo.get_text(separator='\n', strip=True)
                # Limpar texto
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                return '\n'.join(linhas)
            
            return None
            
        except Exception as e:
            self.stdout.write(f'Erro Senado: {e}')
            return None

    def _extrair_receita(self, url, session):
        """Extrai texto do site da Receita Federal"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
                elemento.decompose()
            
            # Buscar o conteúdo principal
            conteudo = soup.find('div', class_='conteudo') or soup.find('div', class_='texto') or soup.find('body')
            
            if conteudo:
                texto = conteudo.get_text(separator='\n', strip=True)
                # Limpar texto
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                return '\n'.join(linhas)
            
            return None
            
        except Exception as e:
            self.stdout.write(f'Erro Receita: {e}')
            return None

    def _extrair_generico(self, url, session):
        """Extrai texto de forma genérica"""
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover elementos desnecessários
            for elemento in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
                elemento.decompose()
            
            # Buscar o conteúdo principal
            texto = soup.get_text(separator='\n', strip=True)
            # Limpar texto
            linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
            return '\n'.join(linhas)
            
        except Exception as e:
            self.stdout.write(f'Erro genérico: {e}')
            return None

    def _criar_texto_estruturado(self, legislacao):
        """Cria um texto estruturado baseado nos dados da legislação"""
        
        texto = f"""{legislacao.get_tipo_display().upper()} Nº {legislacao.numero}/{legislacao.ano}

{legislacao.titulo}

EMENTA:
{legislacao.ementa}

DADOS DA LEGISLAÇÃO:
- Tipo: {legislacao.get_tipo_display()}
- Número: {legislacao.numero}
- Ano: {legislacao.ano}
- Órgão Emissor: {legislacao.get_orgao_display()}
- Esfera: {legislacao.get_esfera_display()}
- Área: {legislacao.get_area_display()}
- Data de Publicação: {legislacao.data_publicacao.strftime('%d/%m/%Y')}"""

        if legislacao.data_vigencia:
            texto += f"\n- Data de Vigência: {legislacao.data_vigencia.strftime('%d/%m/%Y')}"
        
        if legislacao.data_revogacao:
            texto += f"\n- Data de Revogação: {legislacao.data_revogacao.strftime('%d/%m/%Y')}"
        
        if legislacao.diario_oficial:
            texto += f"\n- Diário Oficial: {legislacao.diario_oficial}"
        
        if legislacao.resumo:
            texto += f"""

RESUMO EXECUTIVO:
{legislacao.resumo}"""

        if legislacao.palavras_chave:
            texto += f"""

PALAVRAS-CHAVE:
{legislacao.palavras_chave}"""

        # Adicionar informações específicas por esfera
        if legislacao.esfera == 'FEDERAL':
            texto += """

APLICAÇÃO FEDERAL:
Esta legislação federal estabelece regras aplicáveis em todo o território nacional, com foco em:
- Tributos federais (IR, IPI, PIS, COFINS, CSLL, etc.)
- Normas gerais de direito tributário
- Procedimentos administrativos federais
- Competência da Receita Federal do Brasil
- Relacionamento com contribuintes federais

OPORTUNIDADES DE RECUPERAÇÃO FEDERAL:
- Análise de recolhimentos indevidos de tributos federais
- Verificação de regimes especiais não aplicados
- Créditos de PIS/COFINS não aproveitados
- Benefícios fiscais não utilizados
- Compensação de débitos e créditos federais"""

        elif legislacao.esfera == 'ESTADUAL':
            texto += """

APLICAÇÃO ESTADUAL:
Esta legislação estadual estabelece regras para tributos estaduais, com foco em:
- ICMS - Imposto sobre Circulação de Mercadorias e Serviços
- IPVA - Imposto sobre Propriedade de Veículos Automotores
- ITCMD - Imposto sobre Transmissão Causa Mortis e Doação
- Taxas estaduais
- Procedimentos administrativos estaduais

OPORTUNIDADES DE RECUPERAÇÃO ESTADUAL:
- Créditos de ICMS não aproveitados
- Substituição tributária paga indevidamente
- DIFAL cobrado incorretamente
- Energia elétrica e comunicação com tributação excessiva
- Benefícios estaduais não aplicados"""

        elif legislacao.esfera == 'MUNICIPAL':
            texto += """

APLICAÇÃO MUNICIPAL:
Esta legislação municipal estabelece regras para tributos municipais, com foco em:
- ISS - Imposto sobre Serviços de Qualquer Natureza
- IPTU - Imposto sobre Propriedade Predial e Territorial Urbana
- ITBI - Imposto sobre Transmissão de Bens Imóveis
- Taxas municipais
- Contribuições municipais

OPORTUNIDADES DE RECUPERAÇÃO MUNICIPAL:
- ISS cobrado sobre serviços não tributáveis
- Alíquotas superiores aos limites legais
- Serviços prestados fora do município
- IPTU com base de cálculo incorreta
- Taxas sem contraprestação de serviços"""

        if legislacao.url_oficial:
            texto += f"""

TEXTO OFICIAL:
Para consultar o texto oficial completo desta legislação, acesse:
{legislacao.url_oficial}

OBSERVAÇÃO:
Este é um texto estruturado baseado nos dados disponíveis da legislação. 
Para análises jurídicas detalhadas, consulte sempre o texto oficial na fonte indicada acima."""

        return texto 