from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import json

class Command(BaseCommand):
    help = 'Importa dados do banco local para o Railway'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--usuarios',
            action='store_true',
            help='Importar apenas usuários',
        )
        parser.add_argument(
            '--auditoria',
            action='store_true',
            help='Importar apenas dados de auditoria',
        )
        parser.add_argument(
            '--tudo',
            action='store_true',
            help='Importar todos os dados',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando importação de dados para o Railway...')
        )
        
        # Verificar se os arquivos existem
        arquivos_dados = {
            'usuarios.json': 'Usuários',
            'dados_auditoria.json': 'Dados de Auditoria'
        }
        
        for arquivo, descricao in arquivos_dados.items():
            if not os.path.exists(arquivo):
                self.stdout.write(
                    self.style.ERROR(f'❌ Arquivo {arquivo} não encontrado!')
                )
                return
        
        try:
            # Importar usuários
            if options['usuarios'] or options['tudo']:
                self.stdout.write('📥 Importando usuários...')
                call_command('loaddata', 'usuarios.json')
                self.stdout.write(
                    self.style.SUCCESS('✅ Usuários importados com sucesso!')
                )
            
            # Importar dados de auditoria
            if options['auditoria'] or options['tudo']:
                self.stdout.write('📥 Importando dados de auditoria...')
                call_command('loaddata', 'dados_auditoria.json')
                self.stdout.write(
                    self.style.SUCCESS('✅ Dados de auditoria importados com sucesso!')
                )
            
            # Se nenhuma opção específica foi escolhida, importar tudo
            if not any([options['usuarios'], options['auditoria'], options['tudo']]):
                self.stdout.write('📥 Importando todos os dados...')
                call_command('loaddata', 'usuarios.json')
                call_command('loaddata', 'dados_auditoria.json')
                self.stdout.write(
                    self.style.SUCCESS('✅ Todos os dados importados com sucesso!')
                )
            
            self.stdout.write(
                self.style.SUCCESS('🎉 Importação concluída com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro durante a importação: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('💡 Dica: Verifique se as migrações foram executadas corretamente')
            ) 