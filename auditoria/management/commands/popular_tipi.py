from django.core.management.base import BaseCommand
from auditoria.services.tipi_service import TIPIService

class Command(BaseCommand):
    help = 'Popula a tabela TIPI com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população da tabela TIPI...'))
        
        try:
            service = TIPIService()
            resultado = service.atualizar_tabela_tipi('sistema')
            
            if resultado['sucesso']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Tabela TIPI populada com sucesso!\n'
                        f'Novos registros: {resultado["novos"]}\n'
                        f'Registros alterados: {resultado["alterados"]}\n'
                        f'Total: {resultado["total"]}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao popular tabela TIPI: {resultado["erro"]}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro inesperado: {str(e)}')
            ) 