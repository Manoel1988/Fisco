from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações de exemplo para demonstração do sistema'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações de exemplo...')
        )

        legislacoes_exemplo = [
            # Exemplo Federal
            {
                'titulo': 'Código Tributário Nacional',
                'numero': '5172',
                'ano': 1966,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'FEDERAL',
                'data_publicacao': date(1966, 10, 25),
                'data_vigencia': date(1967, 1, 1),
                'ementa': 'Dispõe sobre o Sistema Tributário Nacional e institui normas gerais de direito tributário aplicáveis à União, Estados e Municípios.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/Leis/L5172.htm',
                'palavras_chave': 'código tributário, tributo, imposto, taxa, contribuição, lançamento, crédito tributário',
                'relevancia': 5,
                'resumo': 'O Código Tributário Nacional estabelece as normas gerais de direito tributário, definindo conceitos fundamentais como tributo, imposto, taxa, contribuição de melhoria, além de regular a relação jurídica tributária, lançamento, crédito tributário, administração tributária e processo administrativo fiscal.',
                'texto_completo': '''CÓDIGO TRIBUTÁRIO NACIONAL

DISPOSIÇÕES GERAIS

Art. 1º Esta Lei regula, com fundamento na Emenda Constitucional nº 18, de 1º de dezembro de 1965, o sistema tributário nacional e estabelece, com fundamento no artigo 5º, inciso XV, alínea b, da Constituição Federal, as normas gerais de direito tributário aplicáveis à União, aos Estados, ao Distrito Federal e aos Municípios, sem prejuízo da respectiva legislação complementar, supletiva ou regulamentar.

TÍTULO I - SISTEMA TRIBUTÁRIO NACIONAL

CAPÍTULO I - DISPOSIÇÕES GERAIS

Art. 2º O sistema tributário nacional é regido pelo disposto na Emenda Constitucional nº 18, de 1º de dezembro de 1965, em leis complementares, em resoluções do Senado Federal e, nos limites das respectivas competências, em leis federais, nas Constituições e em leis estaduais, e em leis municipais.

Art. 3º Tributo é toda prestação pecuniária compulsória, em moeda ou cujo valor nela se possa exprimir, que não constitua sanção de ato ilícito, instituída em lei e cobrada mediante atividade administrativa plenamente vinculada.

Art. 4º A natureza jurídica específica do tributo é determinada pelo fato gerador da respectiva obrigação, sendo irrelevantes para qualificá-la:
I - a denominação e demais características formais adotadas pela lei;
II - a destinação legal do produto da sua arrecadação.

Art. 5º Os tributos são impostos, taxas e contribuições de melhoria.'''
            },
            # Exemplo Estadual
            {
                'titulo': 'Lei Complementar 87/1996 - Lei Kandir (ICMS)',
                'numero': '87',
                'ano': 1996,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1996, 9, 13),
                'data_vigencia': date(1996, 9, 13),
                'ementa': 'Dispõe sobre o imposto dos Estados e do Distrito Federal sobre operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte interestadual e intermunicipal e de comunicação.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp87.htm',
                'palavras_chave': 'ICMS, circulação mercadorias, transporte, comunicação, lei kandir, créditos ICMS',
                'relevancia': 5,
                'resumo': 'Lei Kandir - Principal legislação do ICMS, estabelece regras de incidência, não incidência, créditos e oportunidades de recuperação fiscal estadual.',
                'texto_completo': '''LEI COMPLEMENTAR Nº 87, DE 13 DE SETEMBRO DE 1996

Dispõe sobre o imposto dos Estados e do Distrito Federal sobre operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte interestadual e intermunicipal e de comunicação, e dá outras providências.

CAPÍTULO I - DO IMPOSTO

Art. 1º Compete aos Estados e ao Distrito Federal instituir o imposto sobre operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte interestadual e intermunicipal e de comunicação, ainda que as operações e as prestações se iniciem no exterior.

Art. 2º O imposto incide sobre:
I - operações relativas à circulação de mercadorias, inclusive o fornecimento de alimentação e bebidas em bares, restaurantes e estabelecimentos similares;
II - prestações de serviços de transporte interestadual e intermunicipal, por qualquer via, de pessoas, bens, mercadorias ou valores;
III - prestações onerosas de serviços de comunicação, por qualquer meio, inclusive a geração, a emissão, a recepção, a transmissão, a retransmissão, a repetição e a ampliação de comunicação de qualquer natureza;
IV - fornecimento de mercadorias com prestação de serviços não compreendidos na competência tributária dos Municípios;
V - fornecimento de mercadorias com prestação de serviços sujeitos ao imposto sobre serviços, de competência dos Municípios, quando a lei complementar aplicável expressamente o sujeitar à incidência do imposto estadual.

OPORTUNIDADES DE RECUPERAÇÃO FISCAL:
- Créditos de ICMS não aproveitados
- Substituição tributária paga indevidamente
- Operações com não incidência
- Energia elétrica e comunicação
- Exportações com direito a crédito'''
            },
            # Exemplo Municipal
            {
                'titulo': 'Lei Complementar 116/2003 - Lei do ISS',
                'numero': '116',
                'ano': 2003,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'MUNICIPAL',
                'data_publicacao': date(2003, 7, 31),
                'data_vigencia': date(2003, 7, 31),
                'ementa': 'Dispõe sobre o Imposto Sobre Serviços de Qualquer Natureza, de competência dos Municípios e do Distrito Federal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm',
                'palavras_chave': 'ISS, imposto sobre serviços, municípios, prestação de serviços, lista serviços',
                'relevancia': 5,
                'resumo': 'Lei nacional do ISS que estabelece regras gerais para todos os municípios, incluindo lista de serviços e limites de alíquotas.',
                'texto_completo': '''LEI COMPLEMENTAR Nº 116, DE 31 DE JULHO DE 2003

Dispõe sobre o Imposto Sobre Serviços de Qualquer Natureza, de competência dos Municípios e do Distrito Federal, e dá outras providências.

Art. 1º O Imposto Sobre Serviços de Qualquer Natureza, de competência dos Municípios e do Distrito Federal, tem como fato gerador a prestação de serviços constantes da lista anexa, ainda que esses não se constituam como atividade preponderante do prestador.

§ 1º O imposto incide também sobre o serviço proveniente do exterior do País ou cuja prestação se tenha iniciado no exterior do País.

§ 2º Ressalvadas as exceções expressas na lista anexa, os serviços nela mencionados não ficam sujeitos ao Imposto Sobre Operações Relativas à Circulação de Mercadorias e Prestações de Serviços de Transporte Interestadual e Intermunicipal e de Comunicação – ICMS, ainda que sua prestação envolva fornecimento de mercadorias.

§ 3º O imposto de que trata esta Lei Complementar aplica-se também aos serviços prestados mediante a utilização de bens e serviços públicos explorados economicamente mediante autorização, permissão ou concessão, com o pagamento de tarifa, preço ou pedágio pelo usuário final do serviço.

§ 4º A incidência do imposto não depende da denominação dada ao serviço prestado.

OPORTUNIDADES DE RECUPERAÇÃO MUNICIPAL:
- ISS cobrado sobre serviços não tributáveis
- Alíquotas superiores aos limites legais
- Serviços prestados fora do município
- Bitributação ISS/ICMS
- Serviços sem contraprestação'''
            }
        ]

        with transaction.atomic():
            for leg_data in legislacoes_exemplo:
                legislacao, created = Legislacao.objects.get_or_create(
                    tipo=leg_data['tipo'],
                    numero=leg_data['numero'],
                    ano=leg_data['ano'],
                    orgao=leg_data['orgao'],
                    defaults=leg_data
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Criada: {legislacao.get_identificacao()}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Já existe: {legislacao.get_identificacao()}')
                    )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Legislações de exemplo carregadas com sucesso!')
        )
        self.stdout.write(
            self.style.SUCCESS('Acesse /legislacoes/ para ver o resultado.')
        ) 