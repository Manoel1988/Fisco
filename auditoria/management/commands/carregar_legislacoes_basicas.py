import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações básicas importantes no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações básicas importantes...')
        )

        legislacoes = [
            {
                'titulo': 'Código Tributário Nacional',
                'numero': '5172',
                'ano': 1966,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1966, 10, 25),
                'data_vigencia': date(1967, 1, 1),
                'ementa': 'Dispõe sobre o Sistema Tributário Nacional e institui normas gerais de direito tributário aplicáveis à União, Estados e Municípios.',
                'resumo': 'O Código Tributário Nacional estabelece as normas gerais de direito tributário, definindo conceitos fundamentais como tributo, imposto, taxa, contribuição de melhoria, além de regular a relação jurídica tributária, lançamento, crédito tributário, administração tributária e processo administrativo fiscal.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/Leis/L5172.htm',
                'diario_oficial': 'DOU de 27/10/1966',
                'palavras_chave': 'código tributário, tributo, imposto, taxa, contribuição, lançamento, crédito tributário, administração tributária',
                'ativo': True,
                'relevancia': 4,
            },
            {
                'titulo': 'Regulamento do Imposto sobre Produtos Industrializados - RIPI',
                'numero': '7574',
                'ano': 2011,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'PRESIDENCIA',
                'data_publicacao': date(2011, 9, 29),
                'data_vigencia': date(2011, 11, 1),
                'ementa': 'Regulamenta a Lei nº 4.502, de 30 de novembro de 1964, que dispõe sobre o Imposto sobre Produtos Industrializados - IPI.',
                'resumo': 'O RIPI estabelece as normas para aplicação do IPI, definindo fato gerador, base de cálculo, alíquotas, isenções, não incidência, contribuintes, responsáveis, obrigações acessórias, fiscalização e penalidades. Inclui a TIPI (Tabela de Incidência do IPI) como anexo.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/decreto/d7574.htm',
                'diario_oficial': 'DOU de 30/09/2011',
                'palavras_chave': 'IPI, produtos industrializados, RIPI, TIPI, imposto, industrialização, fato gerador',
                'ativo': True,
                'relevancia': 4,
            },
            {
                'titulo': 'Constituição da República Federativa do Brasil',
                'numero': '1988',
                'ano': 1988,
                'tipo': 'CONSTITUICAO',
                'area': 'CONSTITUCIONAL',
                'orgao': 'CONGRESSO_NACIONAL',
                'data_publicacao': date(1988, 10, 5),
                'data_vigencia': date(1988, 10, 5),
                'ementa': 'Constituição da República Federativa do Brasil de 1988.',
                'resumo': 'A Constituição Federal de 1988 estabelece os princípios fundamentais do Estado brasileiro, incluindo o Sistema Tributário Nacional (Título VI, Capítulo I), competências tributárias da União, Estados e Municípios, princípios constitucionais tributários, imunidades e limitações ao poder de tributar.',
                'url_oficial': 'https://normas.leg.br/?urn=urn:lex:br:federal:constituicao:1988-10-05;1988',
                'diario_oficial': 'DOU de 05/10/1988',
                'palavras_chave': 'constituição, sistema tributário nacional, competência tributária, princípios tributários, imunidades, limitações ao poder de tributar',
                'ativo': True,
                'relevancia': 4,
            },
        ]

        with transaction.atomic():
            for leg_data in legislacoes:
                try:
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
                    else:
                        # Criar nova
                        Legislacao.objects.create(**leg_data)
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Criada: {leg_data["titulo"]}')
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        total_legislacoes = Legislacao.objects.count()
        ativas = Legislacao.objects.filter(ativo=True).count()
        criticas = Legislacao.objects.filter(relevancia=4).count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   ✅ Legislações ativas: {ativas}\n'
                f'   🔥 Relevância crítica: {criticas}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações básicas carregadas com sucesso!')
        ) 