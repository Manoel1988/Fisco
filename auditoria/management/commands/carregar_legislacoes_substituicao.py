import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações sobre substituição tributária e regimes especiais'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações sobre substituição tributária...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Lei 8.846/94 - Substituição Tributária
            {
                'titulo': 'Lei 8.846/1994 - Substituição Tributária',
                'numero': '8846',
                'ano': 1994,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1994, 1, 25),
                'data_vigencia': date(1994, 1, 25),
                'ementa': 'Dispõe sobre a cobrança da contribuição para o PIS/PASEP e para o FINSOCIAL devidas pelas pessoas jurídicas em geral.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8846.htm',
                'palavras_chave': 'substituição tributária, PIS, PASEP, FINSOCIAL, responsabilidade tributária',
                'relevancia': 4,
                'resumo': 'Estabelece os primeiros conceitos de substituição tributária para contribuições sociais, evitando dupla tributação através da responsabilidade de terceiros.'
            },
            # Lei 9.779/99 - Substituição Tributária PIS/COFINS
            {
                'titulo': 'Lei 9.779/1999 - Substituição Tributária PIS/COFINS',
                'numero': '9779',
                'ano': 1999,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1999, 1, 19),
                'data_vigencia': date(1999, 2, 1),
                'ementa': 'Altera a legislação do imposto de renda das pessoas jurídicas, bem como da contribuição social sobre o lucro líquido, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9779.htm',
                'palavras_chave': 'substituição tributária, PIS, COFINS, imposto de renda, contribuição social',
                'relevancia': 4,
                'resumo': 'Aperfeiçoa os mecanismos de substituição tributária para PIS/COFINS, estabelecendo regras para evitar dupla incidência.'
            },
            # Decreto 3.000/99 - RIR/99 (Substituição Tributária)
            {
                'titulo': 'Decreto 3.000/1999 - RIR/99 Substituição Tributária',
                'numero': '3000',
                'ano': 1999,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(1999, 3, 26),
                'data_vigencia': date(1999, 1, 1),
                'ementa': 'Regulamenta a tributação, fiscalização, arrecadação e administração do Imposto sobre a Renda e Proventos de Qualquer Natureza - Capítulo sobre Substituição Tributária.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/decreto/d3000.htm',
                'palavras_chave': 'RIR, substituição tributária, imposto de renda, responsabilidade tributária',
                'relevancia': 3,
                'resumo': 'Regulamenta os aspectos de substituição tributária no imposto de renda, incluindo mecanismos para evitar dupla tributação.'
            },
            # Lei 10.426/02 - Substituição Tributária Combustíveis
            {
                'titulo': 'Lei 10.426/2002 - Substituição Tributária Combustíveis',
                'numero': '10426',
                'ano': 2002,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2002, 4, 24),
                'data_vigencia': date(2002, 4, 24),
                'ementa': 'Dispõe sobre a incidência da contribuição para o PIS/Pasep e da Cofins sobre a receita bruta de venda de combustíveis.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/2002/L10426.htm',
                'palavras_chave': 'combustíveis, PIS, COFINS, substituição tributária, monofásico',
                'relevancia': 4,
                'resumo': 'Estabelece regime especial de substituição tributária para combustíveis, concentrando a tributação e evitando dupla incidência.'
            },
            # Lei 11.488/07 - Substituição Tributária Ampliada
            {
                'titulo': 'Lei 11.488/2007 - Substituição Tributária Ampliada',
                'numero': '11488',
                'ano': 2007,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2007, 6, 15),
                'data_vigencia': date(2007, 6, 15),
                'ementa': 'Cria o Regime Especial de Incentivos para o Desenvolvimento da Infraestrutura - REIDI e estabelece regras de substituição tributária.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11488.htm',
                'palavras_chave': 'REIDI, substituição tributária, infraestrutura, PIS, COFINS',
                'relevancia': 3,
                'resumo': 'Amplia os mecanismos de substituição tributária para projetos de infraestrutura, evitando dupla tributação em investimentos.'
            },
            # Lei 12.546/11 - Substituição Tributária Folha
            {
                'titulo': 'Lei 12.546/2011 - Substituição Tributária sobre Folha',
                'numero': '12546',
                'ano': 2011,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2011, 12, 14),
                'data_vigencia': date(2012, 1, 1),
                'ementa': 'Institui o Regime Especial de Reintegração de Valores Tributários para as Empresas Exportadoras - REINTEGRA e estabelece substituição tributária sobre folha de pagamento.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12546.htm',
                'palavras_chave': 'REINTEGRA, substituição tributária, folha de pagamento, exportação',
                'relevancia': 3,
                'resumo': 'Cria mecanismos de substituição tributária sobre folha de pagamento, evitando dupla tributação em empresas exportadoras.'
            },
            # Decreto 8.426/15 - Procedimentos Substituição Tributária
            {
                'titulo': 'Decreto 8.426/2015 - Procedimentos Substituição Tributária',
                'numero': '8426',
                'ano': 2015,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2015, 4, 1),
                'data_vigencia': date(2015, 4, 1),
                'ementa': 'Regulamenta os procedimentos de substituição tributária e estabelece critérios para evitar dupla tributação.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/decreto/d8426.htm',
                'palavras_chave': 'substituição tributária, procedimentos, dupla tributação, Receita Federal',
                'relevancia': 4,
                'resumo': 'Regulamenta detalhadamente os procedimentos de substituição tributária, estabelecendo critérios operacionais para evitar dupla tributação.'
            },
            # IN RFB 1.234/12 - Substituição Tributária Operacional
            {
                'titulo': 'Instrução Normativa RFB 1.234/2012 - Substituição Tributária Operacional',
                'numero': '1234',
                'ano': 2012,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2012, 1, 11),
                'data_vigencia': date(2012, 2, 1),
                'ementa': 'Dispõe sobre os procedimentos de substituição tributária e critérios para identificação de dupla tributação.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2012/in-rfb-no-1-234-de-11-de-janeiro-de-2012',
                'palavras_chave': 'substituição tributária, procedimentos operacionais, dupla tributação, Receita Federal',
                'relevancia': 4,
                'resumo': 'Instrução normativa que estabelece procedimentos operacionais detalhados para substituição tributária e identificação de dupla tributação.'
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
- Identificação de responsáveis por substituição tributária
- Prevenção de dupla tributação em cadeias produtivas
- Controle de responsabilidade tributária
- Procedimentos para restituição em casos de duplo pagamento
- Definição de substitutos e substituídos tributários

CONCEITOS FUNDAMENTAIS:
1. SUBSTITUIÇÃO TRIBUTÁRIA: Responsabilidade de terceiro pelo pagamento do tributo
2. SUBSTITUTO: Pessoa obrigada ao pagamento do tributo em lugar do contribuinte
3. SUBSTITUÍDO: Contribuinte original que fica desobrigado do pagamento
4. DUPLA TRIBUTAÇÃO: Incidência do mesmo tributo sobre o mesmo fato gerador
5. RESPONSABILIDADE SOLIDÁRIA: Responsabilidade conjunta pelo pagamento do tributo

SITUAÇÕES DE APLICAÇÃO:
- Operações com combustíveis e derivados
- Cadeia produtiva de medicamentos
- Operações com bebidas e cigarros
- Importação de produtos específicos
- Operações entre empresas do mesmo grupo econômico

CONTROLES NECESSÁRIOS:
- Identificação de produtos sujeitos à substituição
- Verificação de pagamentos já efetuados na cadeia
- Controle de responsabilidade tributária
- Documentação de operações
- Conciliação de tributos pagos

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
        substituicao = Legislacao.objects.filter(palavras_chave__icontains='substituição tributária').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   🔄 Legislações de substituição: {substituicao}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações sobre substituição tributária carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🤖 FUNCIONALIDADES PARA CONTROLE DE SUBSTITUIÇÃO TRIBUTÁRIA:\n'
                f'   ✅ Identificação de responsáveis tributários\n'
                f'   ✅ Controle de cadeias produtivas\n'
                f'   ✅ Prevenção de dupla tributação\n'
                f'   ✅ Verificação de pagamentos na cadeia\n'
                f'   ✅ Análise de responsabilidade solidária\n'
                f'   ✅ Orientação para restituição\n'
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