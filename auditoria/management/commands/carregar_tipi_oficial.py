"""
Comando Django para baixar e processar automaticamente o PDF oficial da TIPI
da Receita Federal e importar todos os dados para o sistema.

Uso: python manage.py carregar_tipi_oficial
"""

import os
import requests
import tempfile
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth.models import User

from auditoria.models import TabelaTIPI
from auditoria.services.tipi_pdf_extractor import TIPIPDFExtractor


class Command(BaseCommand):
    help = 'Baixa e processa o PDF oficial da TIPI da Receita Federal'
    
    # URL oficial do PDF da TIPI
    TIPI_URL = 'https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao/documentos-e-arquivos/tipi.pdf'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            default=self.TIPI_URL,
            help='URL do PDF da TIPI (padrão: URL oficial da Receita Federal)'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a reimportação mesmo se já existirem dados'
        )
        
        parser.add_argument(
            '--usuario',
            type=str,
            default='sistema',
            help='Nome do usuário para registrar no histórico'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando download e processamento da TIPI oficial...')
        )
        
        url = options['url']
        force = options['force']
        usuario_nome = options['usuario']
        
        try:
            # Verificar se já existem dados
            if not force and TabelaTIPI.objects.exists():
                count = TabelaTIPI.objects.count()
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Já existem {count} registros na tabela TIPI. '
                        f'Use --force para reimportar.'
                    )
                )
                return
            
            # Baixar PDF
            self.stdout.write('📥 Baixando PDF da TIPI...')
            pdf_content = self._download_pdf(url)
            
            # Processar PDF
            self.stdout.write('🔍 Extraindo dados do PDF...')
            extractor = TIPIPDFExtractor()
            extracted_data = extractor._process_pdf_content(pdf_content)
            
            if not extracted_data:
                raise CommandError('❌ Nenhum dado foi extraído do PDF')
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Extraídos {len(extracted_data)} registros do PDF')
            )
            
            # Importar dados
            self.stdout.write('💾 Importando dados para o banco...')
            imported_count, updated_count = self._import_data(extracted_data, force)
            
            # Registrar histórico
            self._registrar_historico(
                usuario_nome, imported_count, updated_count, len(extracted_data), url
            )
            
            # Resultado final
            self.stdout.write(
                self.style.SUCCESS(
                    f'🎉 Importação concluída!\n'
                    f'   📊 Registros importados: {imported_count}\n'
                    f'   🔄 Registros atualizados: {updated_count}\n'
                    f'   📄 Total extraído: {len(extracted_data)}\n'
                    f'   🌐 Fonte: {url}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro durante o processamento: {str(e)}')
            )
            raise CommandError(f'Falha na importação: {str(e)}')
    
    def _download_pdf(self, url):
        """Baixa o PDF da URL especificada"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            
            # Verificar se é realmente um PDF
            content_type = response.headers.get('content-type', '')
            if 'pdf' not in content_type.lower():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Content-Type: {content_type} - pode não ser PDF')
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ PDF baixado com sucesso ({len(response.content)} bytes)'
                )
            )
            
            return response.content
            
        except requests.RequestException as e:
            raise CommandError(f'Erro ao baixar PDF: {str(e)}')
    
    def _import_data(self, extracted_data, force=False):
        """Importa os dados extraídos para o banco"""
        imported_count = 0
        updated_count = 0
        
        with transaction.atomic():
            # Se force=True, limpar dados existentes
            if force:
                deleted_count = TabelaTIPI.objects.count()
                TabelaTIPI.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'🗑️  Removidos {deleted_count} registros existentes')
                )
            
            for idx, item in enumerate(extracted_data, 1):
                try:
                    codigo_ncm = item.get('codigo_ncm')
                    if not codigo_ncm:
                        continue
                    
                    # Verificar se já existe
                    existing = TabelaTIPI.objects.filter(codigo_ncm=codigo_ncm).first()
                    
                    if existing:
                        # Atualizar registro existente
                        existing.descricao = item.get('descricao', existing.descricao)
                        existing.aliquota_ipi = item.get('aliquota_ipi', existing.aliquota_ipi)
                        existing.observacoes = item.get('observacoes', existing.observacoes)
                        existing.decreto_origem = 'PDF Oficial Receita Federal'
                        existing.data_atualizacao = datetime.now()
                        existing.ativo = True
                        existing.save()
                        updated_count += 1
                    else:
                        # Criar novo registro
                        TabelaTIPI.objects.create(
                            codigo_ncm=codigo_ncm,
                            descricao=item.get('descricao', ''),
                            aliquota_ipi=item.get('aliquota_ipi', 0),
                            observacoes=item.get('observacoes', ''),
                            decreto_origem='PDF Oficial Receita Federal',
                            vigencia_inicio=datetime.now().date(),
                            ativo=True
                        )
                        imported_count += 1
                    
                    # Mostrar progresso a cada 100 registros
                    if idx % 100 == 0:
                        self.stdout.write(f'   📊 Processados {idx}/{len(extracted_data)} registros...')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Erro ao processar item {item.get("codigo_ncm", "N/A")}: {str(e)}'
                        )
                    )
                    continue
        
        return imported_count, updated_count
    
    def _registrar_historico(self, usuario_nome, imported, updated, total_extracted, url):
        """Registra o histórico da atualização (removido - apenas log)"""
        self.stdout.write(
            self.style.SUCCESS(
                f'📋 Histórico de importação:\n'
                f'   👤 Usuário: {usuario_nome}\n'
                f'   📄 Fonte: PDF Oficial Receita Federal\n'
                f'   ➕ Registros importados: {imported}\n'
                f'   🔄 Registros atualizados: {updated}\n'
                f'   📊 Total extraído: {total_extracted}\n'
                f'   🌐 URL: {url}'
            )
        ) 