import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações sobre benefícios fiscais e incentivos tributários'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações sobre benefícios fiscais...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # Lei 8.661/93 - Incentivos Fiscais
            {
                'titulo': 'Lei 8.661/1993 - Incentivos Fiscais P&D',
                'numero': '8661',
                'ano': 1993,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1993, 6, 2),
                'data_vigencia': date(1993, 6, 2),
                'ementa': 'Dispõe sobre os incentivos fiscais para a capacitação tecnológica da indústria e da agropecuária e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8661.htm',
                'palavras_chave': 'incentivos fiscais, P&D, pesquisa, desenvolvimento, capacitação tecnológica, dedução fiscal',
                'relevancia': 4,
                'resumo': 'Estabelece incentivos fiscais para pesquisa e desenvolvimento tecnológico, permitindo dedução de despesas e redução do IRPJ.'
            },
            # Lei 11.196/05 - Lei do Bem
            {
                'titulo': 'Lei 11.196/2005 - Lei do Bem (Incentivos P&D)',
                'numero': '11196',
                'ano': 2005,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2005, 11, 21),
                'data_vigencia': date(2006, 1, 1),
                'ementa': 'Institui o Regime Especial de Tributação para a Plataforma de Exportação de Serviços de Tecnologia da Informação - REPES, o Regime Especial de Aquisição de Bens de Capital para Empresas Exportadoras - RECAP e o Programa de Inclusão Digital.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11196.htm',
                'palavras_chave': 'Lei do Bem, incentivos fiscais, P&D, inovação, dedução fiscal, IRPJ, CSLL',
                'relevancia': 5,
                'resumo': 'Lei do Bem - Principal legislação de incentivos fiscais para inovação tecnológica, permite dedução de até 200% das despesas com P&D.'
            },
            # Lei 8.313/91 - Lei Rouanet
            {
                'titulo': 'Lei 8.313/1991 - Lei Rouanet (Incentivos Culturais)',
                'numero': '8313',
                'ano': 1991,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1991, 12, 23),
                'data_vigencia': date(1991, 12, 23),
                'ementa': 'Restabelece princípios da Lei n° 7.505, de 2 de julho de 1986, institui o Programa Nacional de Apoio à Cultura (Pronac) e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8313.htm',
                'palavras_chave': 'Lei Rouanet, incentivos culturais, dedução fiscal, IRPJ, IRPF, patrocínio cultural',
                'relevancia': 4,
                'resumo': 'Lei Rouanet - Permite dedução fiscal de até 4% do IRPJ e 6% do IRPF para investimentos em projetos culturais aprovados.'
            },
            # Lei 9.249/95 - Dedutibilidade
            {
                'titulo': 'Lei 9.249/1995 - Dedutibilidade e Benefícios IRPJ',
                'numero': '9249',
                'ano': 1995,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1995, 12, 26),
                'data_vigencia': date(1996, 1, 1),
                'ementa': 'Altera a legislação do imposto de renda das pessoas jurídicas, bem como da contribuição social sobre o lucro líquido, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9249.htm',
                'palavras_chave': 'IRPJ, dedutibilidade, benefícios fiscais, despesas dedutíveis, base de cálculo',
                'relevancia': 5,
                'resumo': 'Estabelece regras de dedutibilidade no IRPJ, fundamental para identificar despesas que podem reduzir a base de cálculo do imposto.'
            },
            # Lei 8.069/90 - ECA (Incentivos)
            {
                'titulo': 'Lei 8.069/1990 - ECA Incentivos Fiscais',
                'numero': '8069',
                'ano': 1990,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1990, 7, 13),
                'data_vigencia': date(1990, 10, 13),
                'ementa': 'Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras providências - Aspectos de incentivos fiscais.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8069.htm',
                'palavras_chave': 'ECA, incentivos fiscais, criança, adolescente, dedução fiscal, IRPJ, IRPF',
                'relevancia': 3,
                'resumo': 'Permite dedução fiscal de doações aos Fundos da Criança e do Adolescente, até 1% do IRPJ e IRPF devido.'
            },
            # Lei 9.991/00 - P&D Energia Elétrica
            {
                'titulo': 'Lei 9.991/2000 - P&D Energia Elétrica',
                'numero': '9991',
                'ano': 2000,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2000, 7, 24),
                'data_vigencia': date(2000, 7, 24),
                'ementa': 'Dispõe sobre realização de investimentos em pesquisa e desenvolvimento e em eficiência energética por parte das empresas concessionárias, permissionárias e autorizadas do setor de energia elétrica.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l9991.htm',
                'palavras_chave': 'P&D, energia elétrica, eficiência energética, investimentos obrigatórios, dedução fiscal',
                'relevancia': 3,
                'resumo': 'Obriga concessionárias de energia elétrica a investir em P&D, com possibilidade de dedução fiscal desses investimentos.'
            },
            # Lei 11.077/04 - Incentivos Zona Franca
            {
                'titulo': 'Lei 11.077/2004 - Incentivos Zona Franca de Manaus',
                'numero': '11077',
                'ano': 2004,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2004, 12, 30),
                'data_vigencia': date(2005, 1, 1),
                'ementa': 'Altera a Lei no 8.387, de 30 de dezembro de 1991, para estender os benefícios tributários previstos para a Zona Franca de Manaus.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11077.htm',
                'palavras_chave': 'Zona Franca, Manaus, incentivos fiscais, IPI, IRPJ, benefícios tributários',
                'relevancia': 3,
                'resumo': 'Estende benefícios tributários da Zona Franca de Manaus, incluindo redução de IPI e IRPJ para empresas instaladas na região.'
            },
            # Lei 12.715/12 - PRONATEC
            {
                'titulo': 'Lei 12.715/2012 - PRONATEC Incentivos Fiscais',
                'numero': '12715',
                'ano': 2012,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2012, 9, 17),
                'data_vigencia': date(2012, 9, 17),
                'ementa': 'Altera a Lei no 8.212, de 24 de julho de 1991, a Lei no 8.213, de 24 de julho de 1991, a Lei no 10.260, de 12 de julho de 2001, e a Lei no 8.742, de 7 de dezembro de 1993, para adequar o Programa Nacional de Acesso ao Ensino Técnico e Emprego - PRONATEC.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12715.htm',
                'palavras_chave': 'PRONATEC, educação profissional, incentivos fiscais, capacitação, dedução fiscal',
                'relevancia': 3,
                'resumo': 'Estabelece incentivos fiscais para empresas que investem em educação profissional e capacitação de trabalhadores.'
            },
            # Lei 8.685/93 - Incentivos Audiovisual
            {
                'titulo': 'Lei 8.685/1993 - Incentivos Fiscais Audiovisual',
                'numero': '8685',
                'ano': 1993,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1993, 7, 20),
                'data_vigencia': date(1993, 7, 20),
                'ementa': 'Cria mecanismos de fomento à atividade audiovisual e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8685.htm',
                'palavras_chave': 'audiovisual, cinema, incentivos fiscais, dedução fiscal, IRPJ, produção cultural',
                'relevancia': 3,
                'resumo': 'Permite dedução fiscal de investimentos em produção audiovisual, até 3% do IRPJ devido.'
            },
            # Lei 11.774/08 - Incentivos Desporto
            {
                'titulo': 'Lei 11.774/2008 - Incentivos Fiscais ao Desporto',
                'numero': '11774',
                'ano': 2008,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2008, 9, 17),
                'data_vigencia': date(2008, 9, 17),
                'ementa': 'Altera a Lei no 9.615, de 24 de março de 1998, e dá outras providências.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11774.htm',
                'palavras_chave': 'desporto, esporte, incentivos fiscais, dedução fiscal, IRPJ, IRPF',
                'relevancia': 3,
                'resumo': 'Permite dedução fiscal de patrocínios e doações ao desporto, até 1% do IRPJ e 6% do IRPF devido.'
            },
            # Lei 12.101/09 - Entidades Beneficentes
            {
                'titulo': 'Lei 12.101/2009 - Certificação Entidades Beneficentes',
                'numero': '12101',
                'ano': 2009,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(2009, 11, 27),
                'data_vigencia': date(2009, 11, 27),
                'ementa': 'Dispõe sobre a certificação das entidades beneficentes de assistência social; regula os procedimentos de isenção de contribuições para a seguridade social.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12101.htm',
                'palavras_chave': 'entidades beneficentes, isenção, contribuições sociais, CEBAS, assistência social',
                'relevancia': 4,
                'resumo': 'Regulamenta a certificação de entidades beneficentes e suas isenções de contribuições sociais, importante para terceiro setor.'
            },
            # IN RFB 1.515/14 - Lei do Bem
            {
                'titulo': 'Instrução Normativa RFB 1.515/2014 - Lei do Bem',
                'numero': '1515',
                'ano': 2014,
                'tipo': 'INSTRUCAO_NORMATIVA',
                'area': 'TRIBUTARIO',
                'orgao': 'RECEITA_FEDERAL',
                'data_publicacao': date(2014, 12, 19),
                'data_vigencia': date(2015, 1, 1),
                'ementa': 'Dispõe sobre os incentivos fiscais para inovação tecnológica de que tratam os arts. 17 a 26 da Lei nº 11.196, de 21 de novembro de 2005.',
                'url_oficial': 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/normas-de-tributacao/instrucoes-normativas/2014/in-rfb-no-1-515-de-19-de-dezembro-de-2014',
                'palavras_chave': 'Lei do Bem, P&D, inovação, dedução fiscal, procedimentos operacionais',
                'relevancia': 5,
                'resumo': 'Regulamenta operacionalmente os incentivos da Lei do Bem, detalhando procedimentos para aproveitamento dos benefícios fiscais.'
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
- Aproveitamento de incentivos fiscais
- Dedução de despesas com P&D e inovação
- Aplicação de benefícios tributários
- Documentação necessária para comprovação
- Controles e obrigações acessórias

BENEFÍCIOS FISCAIS DISPONÍVEIS:
1. LEI DO BEM: Dedução de até 200% das despesas com P&D
2. INCENTIVOS CULTURAIS: Dedução de até 4% do IRPJ
3. INCENTIVOS DESPORTIVOS: Dedução de até 1% do IRPJ
4. DOAÇÕES ECA: Dedução de até 1% do IRPJ
5. AUDIOVISUAL: Dedução de até 3% do IRPJ
6. CAPACITAÇÃO TECNOLÓGICA: Dedução de despesas com P&D

REQUISITOS PARA APROVEITAMENTO:
- Empresa tributada pelo lucro real
- Apresentação de lucro fiscal
- Documentação comprobatória adequada
- Cumprimento de obrigações acessórias
- Relatórios de atividades

CONTROLES NECESSÁRIOS:
- Segregação contábil das despesas
- Documentação de projetos
- Relatórios técnicos
- Controle de gastos elegíveis
- Arquivo de comprovantes

OPORTUNIDADES DE RECUPERAÇÃO:
- Benefícios não aplicados em anos anteriores
- Despesas não consideradas adequadamente
- Incentivos não conhecidos pela empresa
- Documentação inadequada corrigida
- Revisão de cálculos de anos anteriores

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
        incentivos = Legislacao.objects.filter(palavras_chave__icontains='incentivos fiscais').count()
        deducao = Legislacao.objects.filter(palavras_chave__icontains='dedução fiscal').count()
        beneficios = Legislacao.objects.filter(palavras_chave__icontains='benefícios fiscais').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   🎯 Legislações de incentivos: {incentivos}\n'
                f'   💰 Legislações de dedução: {deducao}\n'
                f'   🏆 Legislações de benefícios: {beneficios}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações sobre benefícios fiscais carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🏆 OPORTUNIDADES DE BENEFÍCIOS FISCAIS:\n'
                f'   ✅ Lei do Bem - Dedução de até 200% em P&D\n'
                f'   ✅ Lei Rouanet - Dedução de até 4% em cultura\n'
                f'   ✅ Incentivos Desportivos - Dedução de até 1%\n'
                f'   ✅ Doações ECA - Dedução de até 1%\n'
                f'   ✅ Audiovisual - Dedução de até 3%\n'
                f'   ✅ Capacitação Tecnológica - Dedução P&D\n'
                f'   ✅ Zona Franca - Redução IPI e IRPJ\n'
                f'   ✅ Entidades Beneficentes - Isenção contribuições\n'
                f'   ✅ Dedutibilidade - Despesas operacionais\n'
                f'   ✅ Análise de benefícios não aplicados\n'
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