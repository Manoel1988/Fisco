from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import json

from .models import Empresa, DocumentoFiscal, Legislacao, TabelaTIPI


class EmpresaModelTest(TestCase):
    """Testes para o modelo Empresa"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            razao_social='Empresa Teste Ltda',
            cnpj='12.345.678/0001-90',
            regime_tributario='SIMPLES'
        )
    
    def test_str_representation(self):
        """Testa a representação string da empresa"""
        expected = 'Empresa Teste Ltda (12.345.678/0001-90)'
        self.assertEqual(str(self.empresa), expected)
    
    def test_cnpj_unique(self):
        """Testa se CNPJ é único"""
        with self.assertRaises(Exception):
            Empresa.objects.create(
                razao_social='Outra Empresa',
                cnpj='12.345.678/0001-90',  # CNPJ duplicado
                regime_tributario='PRESUMIDO'
            )


class DocumentoFiscalModelTest(TestCase):
    """Testes para o modelo DocumentoFiscal"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            razao_social='Empresa Teste Ltda',
            cnpj='12.345.678/0001-90',
            regime_tributario='SIMPLES'
        )
        
        # Criar arquivo de teste
        self.test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_documento_creation(self):
        """Testa criação de documento fiscal"""
        documento = DocumentoFiscal.objects.create(
            empresa=self.empresa,
            tipo_documento='NFE',
            mes=1,
            ano=2024,
            arquivo=self.test_file
        )
        
        self.assertEqual(documento.empresa, self.empresa)
        self.assertEqual(documento.tipo_documento, 'NFE')
        self.assertEqual(documento.mes, 1)
        self.assertEqual(documento.ano, 2024)
    
    def test_unique_constraint(self):
        """Testa constraint de unicidade"""
        DocumentoFiscal.objects.create(
            empresa=self.empresa,
            tipo_documento='NFE',
            mes=1,
            ano=2024,
            arquivo=self.test_file
        )
        
        # Tentar criar documento duplicado
        with self.assertRaises(Exception):
            DocumentoFiscal.objects.create(
                empresa=self.empresa,
                tipo_documento='NFE',
                mes=1,
                ano=2024,
                arquivo=SimpleUploadedFile("test2.pdf", b"content", content_type="application/pdf")
            )


class LegislacaoModelTest(TestCase):
    """Testes para o modelo Legislacao"""
    
    def setUp(self):
        self.legislacao = Legislacao.objects.create(
            titulo='Lei Teste',
            numero='123',
            ano=2024,
            tipo='LEI',
            area='TRIBUTARIO',
            orgao='CONGRESSO',
            esfera='FEDERAL',
            data_publicacao='2024-01-01',
            ementa='Ementa de teste'
        )
    
    def test_get_identificacao(self):
        """Testa método get_identificacao"""
        expected = 'Lei nº 123/2024'
        self.assertEqual(self.legislacao.get_identificacao(), expected)
    
    def test_legislacao_ativa_por_padrao(self):
        """Testa se legislação é ativa por padrão"""
        self.assertTrue(self.legislacao.ativo)


class ViewsTest(TestCase):
    """Testes para as views"""
    
    def setUp(self):
        self.client = Client()
        self.empresa = Empresa.objects.create(
            razao_social='Empresa Teste Ltda',
            cnpj='12.345.678/0001-90',
            regime_tributario='SIMPLES'
        )
    
    def test_lista_empresas_view(self):
        """Testa view de lista de empresas"""
        response = self.client.get(reverse('auditoria:lista_empresas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empresa Teste Ltda')
    
    def test_detalhes_auditoria_view(self):
        """Testa view de detalhes da auditoria"""
        response = self.client.get(
            reverse('auditoria:detalhes_auditoria', args=[self.empresa.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empresa Teste Ltda')
    
    def test_legislacoes_view(self):
        """Testa view de legislações"""
        # Criar legislação de teste
        Legislacao.objects.create(
            titulo='Lei Teste',
            numero='123',
            ano=2024,
            tipo='LEI',
            area='TRIBUTARIO',
            orgao='CONGRESSO',
            esfera='FEDERAL',
            data_publicacao='2024-01-01',
            ementa='Ementa de teste'
        )
        
        response = self.client.get(reverse('auditoria:legislacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lei Teste')
    
    def test_upload_documentos_view(self):
        """Testa view de upload de documentos"""
        response = self.client.get(
            reverse('auditoria:upload_documentos', args=[self.empresa.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload de Documentos')


class TabelaTIPIModelTest(TestCase):
    """Testes para o modelo TabelaTIPI"""
    
    def setUp(self):
        self.tipi = TabelaTIPI.objects.create(
            codigo_ncm='12345678',
            descricao='Produto de teste',
            aliquota_ipi=15.0,
            observacoes='Observação de teste'
        )
    
    def test_tipi_creation(self):
        """Testa criação de item TIPI"""
        self.assertEqual(self.tipi.codigo_ncm, '12345678')
        self.assertEqual(self.tipi.descricao, 'Produto de teste')
        self.assertEqual(self.tipi.aliquota_ipi, 15.0)
        self.assertTrue(self.tipi.ativo)
    
    def test_tipi_str_representation(self):
        """Testa representação string do TIPI"""
        expected = '12345678 - 15.0% IPI'
        self.assertEqual(str(self.tipi), expected)


class IntegrationTest(TestCase):
    """Testes de integração"""
    
    def setUp(self):
        self.client = Client()
        self.empresa = Empresa.objects.create(
            razao_social='Empresa Teste Ltda',
            cnpj='12.345.678/0001-90',
            regime_tributario='SIMPLES'
        )
        
        # Criar arquivo de teste
        self.test_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_upload_documento_integration(self):
        """Testa integração completa de upload de documento"""
        # Fazer upload via POST
        response = self.client.post(
            reverse('auditoria:upload_documentos', args=[self.empresa.id]),
            {
                'tipo_documento': 'NFE',
                'mes': 1,
                'ano': 2024,
                'arquivo': self.test_file
            }
        )
        
        # Verificar redirecionamento
        self.assertEqual(response.status_code, 302)
        
        # Verificar se documento foi criado
        documento = DocumentoFiscal.objects.get(
            empresa=self.empresa,
            tipo_documento='NFE',
            mes=1,
            ano=2024
        )
        self.assertIsNotNone(documento)
        self.assertEqual(documento.empresa, self.empresa)


class SecurityTest(TestCase):
    """Testes de segurança"""
    
    def setUp(self):
        self.client = Client()
        self.empresa = Empresa.objects.create(
            razao_social='Empresa Teste Ltda',
            cnpj='12.345.678/0001-90',
            regime_tributario='SIMPLES'
        )
    
    def test_file_extension_validation(self):
        """Testa validação de extensões de arquivo"""
        # Arquivo com extensão inválida
        invalid_file = SimpleUploadedFile(
            "test.exe",
            b"malicious_content",
            content_type="application/x-executable"
        )
        
        response = self.client.post(
            reverse('auditoria:upload_documentos', args=[self.empresa.id]),
            {
                'tipo_documento': 'NFE',
                'mes': 1,
                'ano': 2024,
                'arquivo': invalid_file
            }
        )
        
        # Verificar se upload foi rejeitado
        self.assertFalse(
            DocumentoFiscal.objects.filter(
                empresa=self.empresa,
                tipo_documento='NFE',
                mes=1,
                ano=2024
            ).exists()
        )


class PerformanceTest(TestCase):
    """Testes de performance"""
    
    def setUp(self):
        # Criar múltiplas empresas para teste
        for i in range(100):
            Empresa.objects.create(
                razao_social=f'Empresa {i}',
                cnpj=f'12.345.678/000{i:01d}-90',
                regime_tributario='SIMPLES'
            )
    
    def test_lista_empresas_performance(self):
        """Testa performance da lista de empresas"""
        with self.assertNumQueries(1):  # Deve fazer apenas 1 query
            response = self.client.get(reverse('auditoria:lista_empresas'))
            self.assertEqual(response.status_code, 200)
    
    def test_legislacoes_pagination(self):
        """Testa paginação de legislações"""
        # Criar múltiplas legislações
        for i in range(50):
            Legislacao.objects.create(
                titulo=f'Lei {i}',
                numero=str(i),
                ano=2024,
                tipo='LEI',
                area='TRIBUTARIO',
                orgao='CONGRESSO',
                esfera='FEDERAL',
                data_publicacao='2024-01-01',
                ementa=f'Ementa {i}'
            )
        
        response = self.client.get(reverse('auditoria:legislacoes'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar se há paginação (verificar presença de links de página)
        self.assertContains(response, 'pagination')
