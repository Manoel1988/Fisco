import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from bs4 import BeautifulSoup
import time
from auditoria.models import Legislacao


class Command(BaseCommand):
    help = 'Carrega legislações estaduais sobre tributação e recuperação fiscal'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📚 Carregando legislações estaduais tributárias...')
        )

        # Configurar sessão HTTP
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        legislacoes = [
            # ICMS - Legislações Estaduais Principais
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
                'palavras_chave': 'ICMS, circulação mercadorias, serviços transporte, comunicação, créditos ICMS, restituição estadual',
                'relevancia': 5,
                'resumo': 'Lei Kandir - Principal legislação do ICMS, estabelece regras de incidência, não incidência, créditos e oportunidades de recuperação fiscal estadual.'
            },
            # IPVA - Legislação Base
            {
                'titulo': 'Lei 8.383/1991 - IPVA Base Legal',
                'numero': '8383',
                'ano': 1991,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1991, 12, 30),
                'data_vigencia': date(1992, 1, 1),
                'ementa': 'Estabelece normas gerais sobre o Imposto sobre a Propriedade de Veículos Automotores - IPVA.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/l8383.htm',
                'palavras_chave': 'IPVA, veículos automotores, propriedade, restituição IPVA, isenções estaduais',
                'relevancia': 4,
                'resumo': 'Normas gerais do IPVA aplicáveis a todos os estados, incluindo regras de restituição e isenções que podem gerar oportunidades de recuperação.'
            },
            # ITCMD - Legislação Base
            {
                'titulo': 'Resolução Senado 9/1992 - ITCMD',
                'numero': '9',
                'ano': 1992,
                'tipo': 'RESOLUCAO',
                'area': 'TRIBUTARIO',
                'orgao': 'SENADO_FEDERAL',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1992, 5, 6),
                'data_vigencia': date(1992, 5, 6),
                'ementa': 'Estabelece alíquotas máximas do Imposto sobre Transmissão Causa Mortis e Doação de Bens e Direitos.',
                'url_oficial': 'https://legis.senado.leg.br/norma/531273',
                'palavras_chave': 'ITCMD, transmissão causa mortis, doação, alíquotas máximas, restituição estadual',
                'relevancia': 3,
                'resumo': 'Estabelece limites para ITCMD estadual, base para identificar cobranças acima dos limites legais e oportunidades de restituição.'
            },
            # Convênios ICMS - CONFAZ
            {
                'titulo': 'Convênio ICMS 57/1995 - Disciplina Geral CONFAZ',
                'numero': '57',
                'ano': 1995,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1995, 7, 7),
                'data_vigencia': date(1995, 8, 1),
                'ementa': 'Disciplina o tratamento tributário das operações e prestações interestaduais.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/1995/CV057_95',
                'palavras_chave': 'CONFAZ, operações interestaduais, ICMS, créditos, compensação interestadual',
                'relevancia': 5,
                'resumo': 'Convênio fundamental do CONFAZ que disciplina operações interestaduais, fonte de oportunidades de créditos e compensações de ICMS.'
            },
            # Substituição Tributária ICMS
            {
                'titulo': 'Convênio ICMS 81/1993 - Substituição Tributária',
                'numero': '81',
                'ano': 1993,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1993, 10, 8),
                'data_vigencia': date(1993, 11, 1),
                'ementa': 'Disciplina a substituição tributária do ICMS.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/1993/CV081_93',
                'palavras_chave': 'substituição tributária, ICMS-ST, restituição ST, diferencial alíquota, créditos presumidos',
                'relevancia': 5,
                'resumo': 'Convênio que regulamenta substituição tributária do ICMS, fundamental para identificar oportunidades de restituição de ST pago indevidamente.'
            },
            # ICMS Energia Elétrica
            {
                'titulo': 'Convênio ICMS 99/1999 - ICMS Energia Elétrica',
                'numero': '99',
                'ano': 1999,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1999, 8, 6),
                'data_vigencia': date(1999, 9, 1),
                'ementa': 'Disciplina o ICMS incidente sobre energia elétrica.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/1999/CV099_99',
                'palavras_chave': 'ICMS energia elétrica, consumo, demanda, restituição energia, créditos energia',
                'relevancia': 4,
                'resumo': 'Regulamenta ICMS sobre energia elétrica, importante para identificar oportunidades de restituição em consumo industrial e comercial.'
            },
            # ICMS Comunicações
            {
                'titulo': 'Convênio ICMS 126/1998 - ICMS Comunicações',
                'numero': '126',
                'ano': 1998,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1998, 9, 11),
                'data_vigencia': date(1998, 10, 1),
                'ementa': 'Disciplina o ICMS incidente sobre serviços de comunicação.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/1998/CV126_98',
                'palavras_chave': 'ICMS comunicação, telefonia, internet, restituição comunicação, créditos comunicação',
                'relevancia': 4,
                'resumo': 'Regulamenta ICMS sobre comunicações, base para identificar oportunidades de restituição em serviços de telefonia e internet.'
            },
            # ICMS Transporte
            {
                'titulo': 'Convênio ICMS 106/1996 - ICMS Transporte',
                'numero': '106',
                'ano': 1996,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(1996, 9, 27),
                'data_vigencia': date(1996, 11, 1),
                'ementa': 'Disciplina o ICMS incidente sobre serviços de transporte.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/1996/CV106_96',
                'palavras_chave': 'ICMS transporte, frete, restituição transporte, créditos transporte, prestação serviços',
                'relevancia': 4,
                'resumo': 'Regulamenta ICMS sobre transporte, importante para empresas que utilizam serviços de frete e podem ter créditos não aproveitados.'
            },
            # DIFAL - Diferencial de Alíquotas
            {
                'titulo': 'Emenda Constitucional 87/2015 - DIFAL',
                'numero': '87',
                'ano': 2015,
                'tipo': 'CONSTITUICAO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(2015, 4, 16),
                'data_vigencia': date(2016, 1, 1),
                'ementa': 'Altera o Sistema Tributário Nacional e dá outras providências - DIFAL.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc87.htm',
                'palavras_chave': 'DIFAL, diferencial alíquotas, comércio eletrônico, restituição DIFAL, partilha ICMS',
                'relevancia': 5,
                'resumo': 'Emenda que criou o DIFAL, fundamental para identificar oportunidades de restituição em operações interestaduais e comércio eletrônico.'
            },
            # Protocolo ICMS - Medicamentos
            {
                'titulo': 'Protocolo ICMS 3/2007 - Medicamentos',
                'numero': '3',
                'ano': 2007,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(2007, 4, 6),
                'data_vigencia': date(2007, 5, 1),
                'ementa': 'Estabelece disciplina relacionada ao ICMS incidente sobre medicamentos.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/protocolos/2007/PT003_07',
                'palavras_chave': 'ICMS medicamentos, produtos farmacêuticos, restituição medicamentos, substituição tributária medicamentos',
                'relevancia': 4,
                'resumo': 'Protocolo que disciplina ICMS sobre medicamentos, importante para farmácias e distribuidoras identificarem oportunidades de recuperação.'
            },
            # Regime Especial - Microempresas
            {
                'titulo': 'Convênio ICMS 87/2002 - Simples Nacional ICMS',
                'numero': '87',
                'ano': 2002,
                'tipo': 'DECRETO',
                'area': 'TRIBUTARIO',
                'orgao': 'CONFAZ',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(2002, 7, 5),
                'data_vigencia': date(2002, 8, 1),
                'ementa': 'Disciplina o ICMS no âmbito do Simples Nacional.',
                'url_oficial': 'https://www.confaz.fazenda.gov.br/legislacao/convenios/2002/CV087_02',
                'palavras_chave': 'Simples Nacional, ICMS, microempresas, pequenas empresas, restituição Simples, regime especial',
                'relevancia': 4,
                'resumo': 'Convênio que regulamenta ICMS no Simples Nacional, base para identificar oportunidades de restituição para micro e pequenas empresas.'
            },
            # FECP - Fundo Estadual de Combate à Pobreza
            {
                'titulo': 'Lei Complementar 111/2001 - FECP',
                'numero': '111',
                'ano': 2001,
                'tipo': 'LEI',
                'area': 'TRIBUTARIO',
                'orgao': 'CONGRESSO_NACIONAL',
                'esfera': 'ESTADUAL',
                'data_publicacao': date(2001, 7, 6),
                'data_vigencia': date(2001, 7, 6),
                'ementa': 'Dispõe sobre o Fundo de Combate e Erradicação da Pobreza.',
                'url_oficial': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp111.htm',
                'palavras_chave': 'FECP, adicional ICMS, combate pobreza, restituição FECP, adicional estadual',
                'relevancia': 3,
                'resumo': 'Lei que autoriza adicional de ICMS para FECP, importante para identificar cobranças indevidas do adicional estadual.'
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

                    # Para legislações estaduais, adicionar conteúdo explicativo específico
                    if not legislacao.texto_completo:
                        legislacao.texto_completo = f"""
{leg_data['tipo']} Nº {leg_data['numero']}/{leg_data['ano']} - LEGISLAÇÃO ESTADUAL

{leg_data['ementa']}

RESUMO:
{leg_data.get('resumo', '')}

APLICAÇÃO ESTADUAL:
Esta legislação estabelece regras para tributos estaduais com foco em:
- Identificação de oportunidades de recuperação fiscal estadual
- Análise de créditos de ICMS não aproveitados
- Verificação de substituição tributária indevida
- Restituição de tributos estaduais pagos indevidamente
- Compensação de créditos entre estados

TRIBUTOS ESTADUAIS ABRANGIDOS:
1. ICMS - Imposto sobre Circulação de Mercadorias e Serviços
2. IPVA - Imposto sobre Propriedade de Veículos Automotores
3. ITCMD - Imposto sobre Transmissão Causa Mortis e Doação
4. FECP - Fundo Estadual de Combate à Pobreza (adicional ICMS)

OPORTUNIDADES DE RECUPERAÇÃO ESTADUAL:
- Créditos de ICMS não aproveitados em operações interestaduais
- Substituição tributária paga indevidamente
- DIFAL cobrado incorretamente
- Energia elétrica e comunicação com tributação excessiva
- Medicamentos com regime especial não aplicado
- Transporte com créditos não considerados
- Simples Nacional com ICMS cobrado indevidamente

PROCEDIMENTOS ESTADUAIS:
- Pedidos de restituição nas Secretarias de Fazenda Estaduais
- Processos administrativos estaduais
- Compensação de créditos interestaduais
- Recursos ao Tribunal de Impostos e Taxas (TIT)
- Ações judiciais na Justiça Estadual

PRAZOS ESTADUAIS:
- Prescrição: 5 anos (regra geral)
- Decadência: 5 anos para lançamento
- Defesa: 30 dias em processo administrativo
- Recurso: 30 dias da decisão de primeira instância

CONTROLES NECESSÁRIOS:
- Escrituração fiscal estadual (SPED Fiscal)
- Declarações estaduais (GIA, DMA, etc.)
- Documentos fiscais (notas fiscais)
- Comprovantes de pagamento de ICMS
- Controle de créditos e débitos

COORDENAÇÃO FEDERATIVA:
- Convênios CONFAZ (Conselho Nacional de Política Fazendária)
- Protocolos interestaduais
- Acordos de cooperação
- Harmonização tributária
- Partilha de receitas

Para informações específicas de cada estado, consulte:
- Secretaria de Fazenda Estadual
- Código Tributário Estadual
- Regulamento do ICMS (RICMS)
- Tribunal de Impostos e Taxas
- Procuradoria Geral do Estado

URL Oficial: {leg_data['url_oficial']}
"""
                        legislacao.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Conteúdo explicativo adicionado: {len(legislacao.texto_completo)} caracteres')
                        )

                    # Pausa entre requisições
                    time.sleep(0.5)

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao processar {leg_data["titulo"]}: {str(e)}')
                    )
                    continue

        # Estatísticas finais
        total_legislacoes = Legislacao.objects.count()
        estaduais = Legislacao.objects.filter(esfera='ESTADUAL').count()
        icms = Legislacao.objects.filter(palavras_chave__icontains='ICMS').count()
        com_conteudo = Legislacao.objects.exclude(texto_completo='').count()
        chars_total = sum(len(leg.texto_completo) for leg in Legislacao.objects.all() if leg.texto_completo)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Estatísticas Finais:\n'
                f'   📚 Total de legislações: {total_legislacoes}\n'
                f'   🏛️  Legislações estaduais: {estaduais}\n'
                f'   💰 Legislações ICMS: {icms}\n'
                f'   📝 Com conteúdo completo: {com_conteudo}\n'
                f'   📄 Total de caracteres: {chars_total:,}\n'
            )
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Legislações estaduais carregadas com sucesso!')
        )

        # Mostrar resumo das funcionalidades estaduais
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🏛️ OPORTUNIDADES DE RECUPERAÇÃO FISCAL ESTADUAL:\n'
                f'   ✅ Créditos de ICMS não aproveitados\n'
                f'   ✅ Substituição tributária paga indevidamente\n'
                f'   ✅ DIFAL cobrado incorretamente\n'
                f'   ✅ ICMS sobre energia elétrica excessivo\n'
                f'   ✅ ICMS sobre comunicação indevido\n'
                f'   ✅ ICMS sobre transporte com créditos\n'
                f'   ✅ Medicamentos com regime especial\n'
                f'   ✅ Simples Nacional com ICMS indevido\n'
                f'   ✅ FECP cobrado sem base legal\n'
                f'   ✅ IPVA e ITCMD com restituições\n'
            )
        ) 