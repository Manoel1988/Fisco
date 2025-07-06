import re
import logging
import pdfplumber
import pandas as pd
from io import BytesIO
from typing import List, Dict, Tuple, Optional
from decimal import Decimal, InvalidOperation

logger = logging.getLogger(__name__)

class TIPIPDFExtractor:
    """
    Extrator de dados da TIPI a partir de arquivos PDF
    Suporta diferentes formatos de PDF da Receita Federal
    """
    
    def __init__(self):
        # Padrões regex para identificar códigos NCM e alíquotas
        self.ncm_patterns = [
            r'(\d{2}\.\d{2}\.\d{2}\.\d{2})',  # Formato: 12.34.56.78
            r'(\d{4}\.\d{2}\.\d{2})',        # Formato: 1234.56.78
            r'(\d{8})',                      # Formato: 12345678
        ]
        
        # Padrões para alíquotas IPI
        self.aliquota_patterns = [
            r'(\d{1,3}(?:,\d{1,2})?)\s*%',   # Formato: 15,5% ou 15%
            r'(\d{1,3}(?:\.\d{1,2})?)\s*%',   # Formato: 15.5% ou 15%
            r'NT\s*(?:\(.*?\))?',             # Não tributado
            r'ISENTO?',                       # Isento
            r'(\d{1,3}(?:,\d{1,2})?)',       # Apenas número
        ]
        
        # Palavras-chave para identificar isenções
        self.isencao_keywords = [
            'isento', 'isenta', 'nt', 'não tributado', 'não tributada',
            'zero', '0%', 'sem tributação'
        ]
    
    def extract_from_pdf(self, pdf_file) -> List[Dict]:
        """
        Extrai dados da TIPI de um arquivo PDF
        
        Args:
            pdf_file: Arquivo PDF (pode ser file object ou bytes)
            
        Returns:
            Lista de dicionários com os dados extraídos
        """
        try:
            if hasattr(pdf_file, 'read'):
                pdf_content = pdf_file.read()
            else:
                pdf_content = pdf_file
                
            return self._process_pdf_content(pdf_content)
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do PDF: {str(e)}")
            raise
    
    def _process_pdf_content(self, pdf_content: bytes) -> List[Dict]:
        """Processa o conteúdo do PDF e extrai os dados"""
        extracted_data = []
        
        with pdfplumber.open(BytesIO(pdf_content)) as pdf:
            logger.info(f"Processando PDF com {len(pdf.pages)} páginas")
            
            for page_num, page in enumerate(pdf.pages, 1):
                logger.info(f"Processando página {page_num}")
                
                # Tentar extrair tabelas primeiro
                tables = page.extract_tables()
                if tables:
                    page_data = self._extract_from_tables(tables, page_num)
                    extracted_data.extend(page_data)
                
                # Se não encontrou tabelas, tentar extrair do texto
                if not tables:
                    text = page.extract_text()
                    if text:
                        page_data = self._extract_from_text(text, page_num)
                        extracted_data.extend(page_data)
        
        # Remover duplicatas e limpar dados
        cleaned_data = self._clean_and_deduplicate(extracted_data)
        
        logger.info(f"Extraídos {len(cleaned_data)} registros únicos da TIPI")
        return cleaned_data
    
    def _extract_from_tables(self, tables: List, page_num: int) -> List[Dict]:
        """Extrai dados de tabelas identificadas no PDF"""
        extracted_data = []
        
        for table_idx, table in enumerate(tables):
            logger.info(f"Processando tabela {table_idx + 1} da página {page_num}")
            
            if not table or len(table) < 2:
                continue
                
            # Identificar colunas
            header = table[0] if table[0] else []
            data_rows = table[1:]
            
            # Tentar identificar as colunas automaticamente
            ncm_col, desc_col, aliq_col = self._identify_columns(header)
            
            for row_idx, row in enumerate(data_rows):
                if not row or len(row) < 2:
                    continue
                    
                try:
                    # Extrair dados da linha
                    ncm_code = self._extract_ncm_from_cell(row, ncm_col)
                    description = self._extract_description_from_cell(row, desc_col)
                    aliquota = self._extract_aliquota_from_cell(row, aliq_col)
                    
                    if ncm_code and description:
                        extracted_data.append({
                            'codigo_ncm': ncm_code,
                            'descricao': description,
                            'aliquota_ipi': aliquota,
                            'observacoes': self._determine_observacoes(aliquota),
                            'source': f'Página {page_num}, Tabela {table_idx + 1}, Linha {row_idx + 1}'
                        })
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar linha {row_idx + 1}: {str(e)}")
                    continue
        
        return extracted_data
    
    def _extract_from_text(self, text: str, page_num: int) -> List[Dict]:
        """Extrai dados do texto quando não há tabelas"""
        extracted_data = []
        lines = text.split('\n')
        
        for line_idx, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 10:
                continue
                
            try:
                # Tentar extrair NCM, descrição e alíquota da linha
                ncm_match = self._find_ncm_in_text(line)
                if ncm_match:
                    ncm_code = ncm_match
                    
                    # Extrair descrição (geralmente após o código NCM)
                    description = self._extract_description_from_line(line, ncm_code)
                    
                    # Extrair alíquota (geralmente no final da linha)
                    aliquota = self._extract_aliquota_from_line(line)
                    
                    if description:
                        extracted_data.append({
                            'codigo_ncm': ncm_code,
                            'descricao': description,
                            'aliquota_ipi': aliquota,
                            'observacoes': self._determine_observacoes(aliquota),
                            'source': f'Página {page_num}, Linha {line_idx + 1}'
                        })
                        
            except Exception as e:
                logger.warning(f"Erro ao processar linha de texto: {str(e)}")
                continue
        
        return extracted_data
    
    def _identify_columns(self, header: List) -> Tuple[int, int, int]:
        """Identifica as colunas de NCM, descrição e alíquota"""
        ncm_col = desc_col = aliq_col = 0
        
        if not header:
            return ncm_col, desc_col, aliq_col
            
        for idx, cell in enumerate(header):
            if not cell:
                continue
                
            cell_lower = str(cell).lower()
            
            # Identificar coluna NCM
            if any(keyword in cell_lower for keyword in ['ncm', 'código', 'codigo']):
                ncm_col = idx
            
            # Identificar coluna descrição
            elif any(keyword in cell_lower for keyword in ['descrição', 'descricao', 'produto', 'mercadoria']):
                desc_col = idx
            
            # Identificar coluna alíquota
            elif any(keyword in cell_lower for keyword in ['alíquota', 'aliquota', 'ipi', '%', 'taxa']):
                aliq_col = idx
        
        return ncm_col, desc_col, aliq_col
    
    def _extract_ncm_from_cell(self, row: List, col_idx: int) -> Optional[str]:
        """Extrai código NCM de uma célula"""
        if col_idx >= len(row) or not row[col_idx]:
            # Tentar encontrar NCM em qualquer célula da linha
            for cell in row:
                if cell:
                    ncm = self._find_ncm_in_text(str(cell))
                    if ncm:
                        return ncm
            return None
            
        cell_content = str(row[col_idx]).strip()
        return self._find_ncm_in_text(cell_content)
    
    def _extract_description_from_cell(self, row: List, col_idx: int) -> Optional[str]:
        """Extrai descrição de uma célula"""
        if col_idx >= len(row) or not row[col_idx]:
            # Tentar encontrar descrição na linha inteira
            full_text = ' '.join([str(cell) for cell in row if cell])
            return self._clean_description(full_text)
            
        description = str(row[col_idx]).strip()
        return self._clean_description(description)
    
    def _extract_aliquota_from_cell(self, row: List, col_idx: int) -> Decimal:
        """Extrai alíquota de uma célula"""
        if col_idx >= len(row) or not row[col_idx]:
            # Tentar encontrar alíquota em qualquer célula da linha
            for cell in row:
                if cell:
                    aliquota = self._parse_aliquota(str(cell))
                    if aliquota is not None:
                        return aliquota
            return Decimal('0.00')
            
        cell_content = str(row[col_idx]).strip()
        aliquota = self._parse_aliquota(cell_content)
        return aliquota if aliquota is not None else Decimal('0.00')
    
    def _find_ncm_in_text(self, text: str) -> Optional[str]:
        """Encontra código NCM no texto"""
        for pattern in self.ncm_patterns:
            match = re.search(pattern, text)
            if match:
                ncm = match.group(1)
                # Normalizar formato NCM
                if '.' not in ncm and len(ncm) == 8:
                    # Converter 12345678 para 12.34.56.78
                    ncm = f"{ncm[:2]}.{ncm[2:4]}.{ncm[4:6]}.{ncm[6:8]}"
                return ncm
        return None
    
    def _extract_description_from_line(self, line: str, ncm_code: str) -> Optional[str]:
        """Extrai descrição de uma linha de texto"""
        # Remover o código NCM da linha
        line_without_ncm = re.sub(r'\d{2}\.\d{2}\.\d{2}\.\d{2}|\d{4}\.\d{2}\.\d{2}|\d{8}', '', line)
        
        # Remover alíquotas da linha
        for pattern in self.aliquota_patterns:
            line_without_ncm = re.sub(pattern, '', line_without_ncm)
        
        description = line_without_ncm.strip()
        return self._clean_description(description)
    
    def _extract_aliquota_from_line(self, line: str) -> Decimal:
        """Extrai alíquota de uma linha de texto"""
        aliquota = self._parse_aliquota(line)
        return aliquota if aliquota is not None else Decimal('0.00')
    
    def _parse_aliquota(self, text: str) -> Optional[Decimal]:
        """Converte texto de alíquota para Decimal"""
        if not text:
            return None
            
        text_lower = text.lower().strip()
        
        # Verificar se é isento
        if any(keyword in text_lower for keyword in self.isencao_keywords):
            return Decimal('0.00')
        
        # Tentar extrair número com %
        for pattern in self.aliquota_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    # Pegar o primeiro grupo que contém número
                    aliq_str = match.group(1)
                    # Substituir vírgula por ponto
                    aliq_str = aliq_str.replace(',', '.')
                    return Decimal(aliq_str)
                except (InvalidOperation, AttributeError, IndexError):
                    continue
        
        return None
    
    def _clean_description(self, description: str) -> Optional[str]:
        """Limpa e valida descrição"""
        if not description:
            return None
            
        # Remover caracteres especiais e múltiplos espaços
        description = re.sub(r'[^\w\s\-\(\)\.,]', ' ', description)
        description = re.sub(r'\s+', ' ', description)
        description = description.strip()
        
        # Validar tamanho mínimo
        if len(description) < 3:
            return None
            
        # Remover números isolados no início
        description = re.sub(r'^\d+\s+', '', description)
        
        return description[:500]  # Limitar tamanho
    
    def _determine_observacoes(self, aliquota: Decimal) -> str:
        """Determina observações baseadas na alíquota"""
        if aliquota == Decimal('0.00'):
            return 'Isento'
        elif aliquota > Decimal('50.00'):
            return 'Alíquota específica'
        else:
            return 'Tributação normal'
    
    def _clean_and_deduplicate(self, data: List[Dict]) -> List[Dict]:
        """Remove duplicatas e limpa dados"""
        seen_ncm = set()
        cleaned_data = []
        
        for item in data:
            ncm = item.get('codigo_ncm')
            if not ncm or ncm in seen_ncm:
                continue
                
            # Validar dados mínimos
            if not item.get('descricao') or len(item.get('descricao', '')) < 3:
                continue
                
            seen_ncm.add(ncm)
            cleaned_data.append(item)
        
        # Ordenar por código NCM
        cleaned_data.sort(key=lambda x: x.get('codigo_ncm', ''))
        
        return cleaned_data 