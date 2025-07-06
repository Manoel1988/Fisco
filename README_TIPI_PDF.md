# 📄 Sistema de Upload de PDF da TIPI

## Visão Geral

O sistema agora possui uma funcionalidade completa para upload e processamento automático de PDFs da TIPI (Tabela de Incidência do Imposto sobre Produtos Industrializados). Esta funcionalidade permite:

- **Upload de PDFs oficiais** da Receita Federal
- **Extração automática** de códigos NCM, descrições e alíquotas
- **Importação em lote** para o banco de dados
- **Atualização inteligente** dos registros existentes

## 🚀 Como Usar

### 1. Acessar a Interface

Existem duas formas de acessar:

**Via Admin Django:**
1. Acesse: `http://localhost:8000/admin/`
2. Vá para **Auditoria > Tabela TIPIs**
3. Clique em **"📄 Upload PDF da TIPI"**

**Via URL Direta:**
- Acesse: `http://localhost:8000/auditoria/upload-tipi-pdf/`

### 2. Fazer Upload do PDF

1. **Selecione o arquivo PDF** da TIPI oficial
2. **Arraste e solte** ou clique para selecionar
3. **Clique em "🚀 Processar e Importar TIPI"**
4. **Aguarde o processamento** (pode levar alguns minutos)

### 3. Verificar Resultados

O sistema mostrará:
- ✅ **Registros importados** (novos)
- 🔄 **Registros atualizados** (existentes)
- 📊 **Estatísticas** do processamento

## 📋 Requisitos do PDF

Para melhor extração, o PDF deve:

- ✅ **Formato:** PDF oficial da Receita Federal
- ✅ **Tamanho:** Máximo 50 MB
- ✅ **Conteúdo:** Texto pesquisável (não apenas imagem)
- ✅ **Estrutura:** Tabela com códigos NCM e alíquotas
- ✅ **Versões suportadas:** TIPI 2022, ADE 008/2024, futuras atualizações

## 🔧 Funcionalidades Técnicas

### Extração Inteligente

O sistema utiliza múltiplas estratégias:

1. **Extração de Tabelas:** Identifica automaticamente tabelas estruturadas
2. **Análise de Texto:** Processa texto livre quando não há tabelas
3. **Padrões Regex:** Reconhece códigos NCM em diversos formatos
4. **Limpeza de Dados:** Remove duplicatas e valida informações

### Formatos NCM Suportados

- `12.34.56.78` (formato padrão)
- `1234.56.78` (formato alternativo)
- `12345678` (formato numérico)

### Alíquotas Reconhecidas

- `15%`, `15,5%`, `15.5%` (percentuais)
- `NT`, `Isento`, `0%` (isenções)
- `330%` (alíquotas especiais)

## 📊 Monitoramento

### Histórico de Atualizações

Acesse: **Admin > Auditoria > Histórico Atualização TIPIs**

Informações registradas:
- 📅 **Data/hora** da importação
- 👤 **Usuário** responsável
- 📈 **Estatísticas** (novos/atualizados)
- 📄 **Fonte** do arquivo
- ✅ **Status** do processamento

### Estatísticas em Tempo Real

Na interface principal:
- **Total de registros** na base
- **Produtos isentos** (alíquota 0%)
- **Produtos tributados** (alíquota > 0%)
- **Última atualização**

## 🧪 Teste do Sistema

### PDF de Exemplo

Foi criado um PDF de teste com 46 registros da TIPI:

```bash
python test_tipi_pdf.py
```

Isso gera `tipi_exemplo_teste.pdf` para testar a funcionalidade.

### Dados de Teste

O PDF inclui:
- **Animais vivos** (0% IPI)
- **Bebidas alcoólicas** (20% IPI)
- **Produtos de tabaco** (150-330% IPI)
- **Automóveis** (7-25% IPI)
- **Eletrônicos** (12-15% IPI)
- **Cosméticos** (20% IPI)

## 🔄 Integração com IA

Os dados importados são automaticamente utilizados pelo sistema de IA para:

- **Análise de conformidade** IPI
- **Sugestões de classificação** NCM
- **Identificação de inconsistências** fiscais
- **Relatórios automáticos** de auditoria

## 🛠️ Tecnologias Utilizadas

- **pdfplumber:** Extração de dados de PDF
- **tabula-py:** Processamento de tabelas
- **Django:** Framework web
- **Regex:** Reconhecimento de padrões
- **Bootstrap:** Interface responsiva

## 📝 Logs e Debugging

O sistema registra detalhadamente:

```python
# Logs disponíveis
logger.info("Processando PDF com X páginas")
logger.info("Extraídos X registros únicos da TIPI")
logger.error("Erro ao processar PDF: {erro}")
```

## 🔒 Segurança

- ✅ **Autenticação** obrigatória
- ✅ **Validação** de tipo de arquivo
- ✅ **Limite** de tamanho (50MB)
- ✅ **Transações** atômicas no banco
- ✅ **Logs** de auditoria

## 🚨 Solução de Problemas

### PDF não processado
- Verifique se é um PDF com texto pesquisável
- Confirme se contém tabelas estruturadas
- Teste com o PDF de exemplo

### Dados não extraídos
- Verifique os logs no admin Django
- Confirme formato dos códigos NCM
- Teste com diferentes PDFs

### Erro de importação
- Verifique permissões do banco
- Confirme se há espaço em disco
- Teste com arquivo menor

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs no admin
2. Teste com o PDF de exemplo
3. Consulte a documentação técnica
4. Contate o suporte técnico

---

**Versão:** 1.0  
**Data:** Janeiro 2025  
**Compatibilidade:** Django 5.2.4, Python 3.13+ 